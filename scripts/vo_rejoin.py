#!/usr/bin/env python3
"""Join narration takes into one VO file without audible seams (PLAYBOOK §7; rebuilt 2026-11-25 after the old repo).

Never plain concatenation. For each take, in order:
  1. Trim the silence at each end, down to a short pad around the speech (--pad).
  2. Cut a late burst: ElevenLabs sends the next text as context, so a take can end with the first 50–70 ms of a word
     that belongs to the next take, clipped by the file end. A last speech run shorter than --burst seconds that
     ends within 20 ms of the file end, after a pause, is removed.
  3. Match loudness to the first take (speech-only RMS, so pauses don't skew it), capped at +/- 6 dB.
  4. Fade in 5 ms and out 10 ms, so no take starts or stops at full level.
Gaps between takes are filled with room tone made from the takes' own quietest pauses (shaped noise at their level,
about -72 dB for ElevenLabs), never digital zero. --gaps sets the seconds of silence between take i and take i+1
(from the end of one take's speech to the start of the next); a longer gap where the story turns.

Usage: scripts/vo_rejoin.py T1 T2 [T3 ...] --gaps 0.9 [0.9 ...] --out projects/<slug>/assets/vo/<prefix>_vo_full.wav
       [--mp3 out.mp3] [--sr 44100]
Prints each take's trims, gain and the join times (seconds into the output) so they can be listened to.
"""
import argparse
import subprocess
import sys

import numpy as np

FRAME = 0.010           # analysis frame, seconds
SPEECH_DB = -38.0       # a frame louder than this is speech (the take checks' silence threshold)


def load(path, sr):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def frame_db(x, sr):
    n = int(FRAME * sr)
    k = len(x) // n
    rms = np.sqrt(np.mean(x[:k * n].reshape(k, n) ** 2, axis=1) + 1e-20)
    return 20 * np.log10(rms), n


def runs(mask):
    """(start, end) frame indices of True runs"""
    out, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        elif not m and start is not None:
            out.append((start, i)); start = None
    if start is not None:
        out.append((start, len(mask)))
    return out


def room_tone(takes, sr, seconds, rng):
    """noise shaped like the takes' quietest pauses, at their level"""
    pieces = []
    for x in takes:
        db, n = frame_db(x, sr)
        quiet = np.where(db < np.percentile(db, 10))[0]
        for i in quiet[:400]:
            pieces.append(x[i * n:(i + 1) * n])
    if not pieces:
        return np.zeros(int(seconds * sr))
    ref = np.concatenate(pieces)
    level = np.sqrt(np.mean(ref ** 2))
    spec = np.abs(np.fft.rfft(ref[: 1 << int(np.log2(len(ref)))]))   # average spectrum shape of the pauses
    length = int(seconds * sr)
    noise = rng.standard_normal(length)
    nspec = np.fft.rfft(noise)
    shape = np.interp(np.linspace(0, 1, len(nspec)), np.linspace(0, 1, len(spec)), spec)
    tone = np.fft.irfft(nspec * shape / (shape.mean() + 1e-20), n=length)
    return tone * level / (np.sqrt(np.mean(tone ** 2)) + 1e-20)


def fade(x, sr, fin=0.005, fout=0.010):
    a, b = int(fin * sr), int(fout * sr)
    x = x.copy()
    x[:a] *= np.linspace(0, 1, a)
    x[-b:] *= np.linspace(1, 0, b)
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("takes", nargs="+")
    ap.add_argument("--gaps", nargs="*", type=float, default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--mp3", help="also write a 192 kbps MP3 for the owner's listen")
    ap.add_argument("--sr", type=int, default=44100)
    ap.add_argument("--pad", type=float, default=0.06, help="seconds kept around speech at a take's ends")
    ap.add_argument("--burst", type=float, default=0.12, help="longest late burst cut at a take's end")
    a = ap.parse_args()
    if len(a.gaps) != len(a.takes) - 1:
        sys.exit(f"--gaps needs {len(a.takes) - 1} value(s), one per join")
    sr, rng = a.sr, np.random.default_rng(7)

    raw = [load(p, sr) for p in a.takes]
    trimmed, ref_rms = [], None
    for path, x in zip(a.takes, raw):
        db, n = frame_db(x, sr)
        speech = runs(db > SPEECH_DB)
        if not speech:
            sys.exit(f"{path}: no speech found")
        last_s, last_e = speech[-1]
        note = ""
        if (len(speech) > 1 and (last_e - last_s) * FRAME < a.burst and len(db) - last_e <= 2
                and (last_s - speech[-2][1]) * FRAME > 0.08):
            note = f", cut a {(last_e - last_s) * FRAME * 1000:.0f} ms late burst"
            speech = speech[:-1]
        s0 = max(0, int((speech[0][0] * FRAME - a.pad) * sr))
        s1 = min(len(x), int((speech[-1][1] * FRAME + a.pad) * sr))
        y = x[s0:s1]
        ydb, yn = frame_db(y, sr)
        sp = np.repeat(ydb > SPEECH_DB, yn)[: len(y)]
        rms = np.sqrt(np.mean(y[: len(sp)][sp] ** 2))
        gain_db = 0.0
        if ref_rms is None:
            ref_rms = rms
        else:
            gain_db = float(np.clip(20 * np.log10(ref_rms / rms), -6, 6))
            y = y * 10 ** (gain_db / 20)
        trimmed.append(fade(y, sr))
        print(f"{path}: kept {s0 / sr:.2f}–{s1 / sr:.2f} s of {len(x) / sr:.2f} s, gain {gain_db:+.1f} dB{note}")

    out, t = [], 0.0
    for i, y in enumerate(trimmed):
        if i:
            gap = room_tone(raw, sr, max(0.0, a.gaps[i - 1] - 2 * a.pad), rng)
            out.append(gap); t += len(gap) / sr
            print(f"join {i}: take {i + 1} starts at {t:.2f} s (listen {max(0, t - 3):.1f}–{t + 3:.1f} s)")
        out.append(y); t += len(y) / sr
    full = np.concatenate(out)
    peak = np.max(np.abs(full))
    if peak > 0.98:
        full *= 0.98 / peak
        print(f"peak {20 * np.log10(peak):.1f} dBFS lowered to -0.2 dBFS")
    pcm = full.astype(np.float32).tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s24le", a.out], input=pcm, check=True)
    if a.mp3:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out, "-c:a", "libmp3lame", "-b:a", "192k", a.mp3],
                       check=True)
    print(f"wrote {a.out} ({len(full) / sr:.2f} s){' and ' + a.mp3 if a.mp3 else ''}")


if __name__ == "__main__":
    main()
