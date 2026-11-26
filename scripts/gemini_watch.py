#!/usr/bin/env python3
"""Have Gemini watch a downloaded clip and list its usable spans (footage vetting, PLAYBOOK §11).

  python3 scripts/gemini_watch.py CLIP.mp4 [CLIP2.mp4 ...] --needs projects/<slug>/footage_needs.md --out DIR

For each clip: timecoded frame sheets (one frame every --every seconds, 6x5 tiles) and the audio (mono 16 kHz MP3)
go to Gemini through its OpenAI-compatible endpoint; it returns JSON spans (start, end, what is shown, who and where,
on-screen text, speech, which beat it fits, problems). Gemini's spans are LEADS: every span we use is checked on
our own contact sheet before it enters the EDL (Gemini can misread a timecode or a sign).
The key is a network secret on the environment: the proxy injects it as a Bearer token for
generativelanguage.googleapis.com, so this script sends a placeholder (never put a real key here).
Free tier: inputs may be used by Google to improve its products, so send only footage we fetched from public pages.
"""
import argparse
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PROMPT = """You are vetting footage for an English documentary about India's pressurised heavy-water reactors
(Rawatbhata, Rajasthan; Kakrapar, Gujarat; the 1990s tube replacement at Rawatbhata unit 2). The images are frame
sheets: each tile has its timecode (HH:MM:SS) burned in its top-left corner; the audio is the clip's soundtrack.
The film's picture needs are:
{needs}
Return ONLY JSON: {{"summary": "...", "language": "...", "spans": [{{"start": "MM:SS", "end": "MM:SS",
"shows": "what is literally on screen", "place_people": "where / who, only if shown or said", "onscreen_text":
"captions, signs, logos", "speech": "what is said, short, in English", "fits": "which need above, or none",
"problems": "logo bug, burned-in subtitles, CGI, foreign place, talking head, etc."}}]}}
Cover the whole clip in spans of one continuous shot or a few similar shots. Say "CGI/animation" whenever a shot is
not a real camera image. Never guess a place or a person's name that is not shown or said."""


def sheets(clip, every, tmp):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
                    f"fps=1/{every},scale=320:-2,drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=4:y=4:"
                    f"fontsize=16:fontcolor=yellow:box=1:boxcolor=black,tile=6x5", str(tmp / "s_%03d.jpg")],
                   check=True)
    return sorted(tmp.glob("s_*.jpg"))


def audio(clip, tmp):
    out = tmp / "a.mp3"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vn", "-ac", "1", "-ar", "16000", "-b:a",
                        "32k", str(out)])
    return out if r.returncode == 0 and out.exists() else None


def ask(model, content):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": content}],
                       "response_format": {"type": "json_object"}}).encode()
    for k in range(5):
        req = urllib.request.Request(URL, body, {"Content-Type": "application/json",
                                                 "Authorization": "Bearer proxy-injected"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=600))
            return r["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:   # 429 (free-tier rate) and 5xx (busy) are retried
            msg = e.read().decode(errors="replace")
            if e.code == 429 and "per day" in msg:   # the free tier's daily cap (20 a model): retrying wastes nothing
                raise SystemExit(f"daily free-tier limit reached for {model}; try another model or tomorrow")
            if e.code not in (429, 500, 502, 503, 504) or k == 4:
                raise
            time.sleep(30 * (k + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--needs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="gemini-3.6-flash")
    a = ap.parse_args()
    needs = Path(a.needs).read_text()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for clip in map(Path, a.clips):
        dest = out / (clip.stem + ".json")
        if dest.exists():
            print("have", dest)
            continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(clip)], capture_output=True, text=True).stdout)
        every = max(2, round(dur / 240))          # at most about 240 frames (8 sheets) a clip
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            content = [{"type": "text", "text": PROMPT.format(needs=needs)}]
            for s in sheets(clip, every, t):
                content.append({"type": "image_url", "image_url": {
                    "url": "data:image/jpeg;base64," + base64.b64encode(s.read_bytes()).decode()}})
            au = audio(clip, t)
            if au:
                content.append({"type": "input_audio", "input_audio": {
                    "data": base64.b64encode(au.read_bytes()).decode(), "format": "mp3"}})
            try:
                txt = ask(a.model, content)
                data = json.loads(txt)
            except Exception as e:  # noqa: BLE001 - one clip failing must not stop the rest
                print(f"FAILED {clip.name}: {e}", file=sys.stderr)
                continue
        data.update({"clip": clip.name, "duration_s": round(dur, 1), "frame_every_s": every, "model": a.model})
        dest.write_text(json.dumps(data, indent=1, ensure_ascii=False))
        print(f"ok {clip.name}: {len(data.get('spans', []))} spans")


if __name__ == "__main__":
    main()
