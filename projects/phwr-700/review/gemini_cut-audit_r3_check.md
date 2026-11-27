# Gemini cut audit of review cut r3: our check (27 NOV 2026, about 11:15 AM IST)

Two replies, both FIXES_REQUIRED, both "visuals locked, audio-only remix": `gemini_cut-audit_r3b.md` (9:58 AM IST,
10 edits) and `gemini_cut-audit_r3.md` (10:15 AM IST, the full spec). Checked against the r3 stems rebuilt here
(`scripts/score_mix.py` reproduced r3's `mix.wav` to −166 dB, so every measure below is of the real r3 mix), in
100 ms RMS windows on the master's scale. Gemini's file names for our recordings are guesses (no "metro s3039" or
"steel barrier" file exists in `sfx.json`); its times and levels match our cues to about 0.3 s and a few dB.

## Verdict on the picture
**CONFIRMED, and the owner said "render in 4k" (27 NOV):** the picture of r3 is the approved cut. The 4K master was
started from `main` (run 45945459762, 15 runners) with the r4 mix laid at the join.

## Music
| Lead | Our check | Fix (r4) |
|---|---|---|
| The bed is too deep under the voice; swells jump in the gaps | **CONFIRMED**: r3 bed under speech −39.6 dB median against voice −17.4 (22 dB under); gaps up to −10 dB (a 20 dB duck pumping) | Music bus: high-pass 90 Hz, −2.5 dB at 1.8 kHz (the voice's pocket), 3:1 leveller; −29.5 dB on the bus, duck −7 dB. r4: −28.8 under speech (11 dB under the voice), gaps −26.8, every 1 s swell under −22 dB during the film |
| Abrupt joins | **PARTLY**: slots already overlapped with 1.5 s fades, but squared (not equal-power) curves dip at the cross | Equal-power sine/cosine fades, 2.0 s at every join; the two dry windows (4:15.6–4:22, after 6:31) stay dry |
| Warm "A Way Forward" under Pokhran and Canada's walk-out (reply 2) | **CONFIRMED** by the text: it entered on "So Canada stopped its nuclear help" | The Mechanism ends on the Pokhran hit; The Boardroom (track 1:50, unused elsewhere) carries 1:54–2:23; A Way Forward enters on "Indian engineers finished it on their own" |
| Outro enters early (reply 2) | **CONFIRMED**: Stay Practical came in under the next-film line | A Family's Story carries the next-film line; the outro enters on "Subscribe" |
| Level trims on three beds (reply 2) | **PARTLY**: the leveller evens them | Counter-offensive −2 dB, A Way Forward (ch.5) −1.5 dB |

## Sound effects
| Lead | Our check | Fix (r4) |
|---|---|---|
| 5:17–5:23 a rail roar over the tube-draw diagram, a bang at 5:26 | **CONFIRMED**: `trolley.mp3` (6 s) on "carries" plus the full 5.2 s vault door (its second hit at +3 s) | Trolley removed; winch low-passed at 1 kHz, 3.6 s, −10 dB; only the first latch (0.6 s, low-passed) |
| 1:30 heavy crash on the 1 kg weight | **CONFIRMED** (synth impact at −10) | A 0.3 s tap, low-passed at 500 Hz |
| 3:59 crash on the cut to the diagram | **CONFIRMED** | A soft relay click |
| 4:18 slam on "doctor" | **CONFIRMED** | Removed; 4:15.6–4:22 is dry voice |
| 2:45 fuelling-machine noise wall | **CONFIRMED** (winch motor at −19, full band) | Low-passed at 1.2 kHz, 0.6 s fades, −7 dB: felt, not heard |
| 3:09 metal slam on "broke" | **CONFIRMED** | A dry low thump, low-passed |
| 3:54 steam hiss on the sibilants | **CONFIRMED** | 0.9 s, low-passed at 1.1 kHz, ends before S73 |
| 6:53 rod drop as a door slam | **CONFIRMED** | Low-passed at 800 Hz, 0.7 s |
| 1:26 cooker whistle is hiss, on the word | **CONFIRMED** | Band-passed 1.2–3.2 kHz, 0.65 s, 0.12 s later |
| 8:09 alarm buzz | **CONFIRMED** | Low-passed at 1.8 kHz, 0.5 s |
| 0:26 hero clunk, 1:54 Pokhran, 2:06 folder slam | **CONFIRMED** (loud) | Clunk low-passed, −7.5 dB; Pokhran low-passed, −6.5 dB (still the loudest cue, by design); 2:06 is now the CLOSED stamp the picture shows |
| Glassy chimes over diagrams (reply 2) | **CONFIRMED** | 14 chimes and ticks −6 dB |

**Our own rule added:** after those changes every cue was fitted to sit at least 4 dB under the voice's local level
(100 ms RMS; stamps and the clunk 1 dB, Pokhran −3 dB): 22 cues took a further 1.5–6.5 dB. No cue now passes it.

## Not taken
- Gemini's absolute targets ("−26 dB integrated music bus") as numbers: they are on its own stem scale; we kept its
  intent (music always audible, about 11 dB under the voice) and measured on ours.
- Deleting the 2:45 motor outright (reply 1): reply 2's low-passed version keeps a sound on a real machine (§12).

## r4 mix
`sound/sfx.json`, `sound/score.json`, `scripts/score_mix.py` (cue EQ and length, the bus filter, equal-power fades).
−14.2 LUFS, −2.2 dBTP, LRA 2.9 LU. Drive `mix/mix.wav` (r3's is `mix/mix_r3.wav`); the r4 720p review copy is r3's
picture with this mix (`renders/phwr_review_r4_720p.mp4`, stream copy, no re-render).
