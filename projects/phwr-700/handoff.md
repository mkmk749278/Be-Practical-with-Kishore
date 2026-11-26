# Handoff · phwr-700 (session closed 23 NOV 2026, about 3:00 PM IST)

## Where it stands (updated 23 NOV 2026, about 5:30 PM IST)
- **Plan v2 APPROVED** by the owner with four locks (`plan.md` §0): title "Canada Walked Out of India's Nuclear
  Reactor"; Test & Compare "1974" vs "LEFT HALF-BUILT"; the Canadian restriction said precisely (export rules barred
  Canadian firms from the retubing tools and the job; COG contact existed); rupees in crores for the ch.3 cost; no
  prime ministers' names.
- **The owner's Section 10 facts checked (C42–C48):** confirmed Pickering G16 and the hydrogen-to-the-coldest-point
  physics (AECL report on NRC ADAMS), Kakrapar INES 2 final with no fuel failure and no radiological impact (IAEA),
  KAPP-3/4 first concrete, three 700s running, Cameco C$2.6 billion (C19's US$ was wrong, fixed). **Changed:** RAPS-1
  "last operated in 2004, never formally retired" (not "permanently shut down"); RAPS-2 "ran again by 1998" (the
  exact day is unverified; C41's May 1998 is cut).
- The channel became a YouTube Partner on 23 NOV (expanded tier); full ads need 1,000 subscribers (§15.6 plan).

## Audio (25 NOV 2026, about 11:00 AM IST)
- **Takes received** (in Drive `Creator/English/phwr-700/vo/raw/`): `phwr_t1_raw.mp3` (23 NOV, 600.27 s, the app's
  10-minute cap; cold open → "…point your phone's camera at the code on the screen.") and `phwr_t2_raw.mp3` (25 NOV,
  8.36 s; "And tell me in the comments…" → "Stay practical."). So two takes joined at a paragraph break (no splice).
  T1's last word tapers to silence at 600.0 s (not cut); T1 −23.2 LUFS, T2 −21.9 LUFS: match levels at the join.
- **Resemble Enhance on Modal** (owner, 25 NOV): `modal-enhance` workflow (T4, nfe 64, lambd 0.1, tau 0.5) writes
  `vo/enhanced/phwr_t1_enh.wav`, `phwr_t2_enh.wav`. Then: compare raw vs enhanced (artefacts, sibilance, loudness),
  `vo_take_check.py`, join (rebuild `scripts/vo_rejoin.py`), one MP3 to the owner for audio approval.
- **25 NOV, 11:30 AM IST:** Modal secrets added (owner, via Termux `gh secret set`); `modal-enhance` run 3 passed in
  8 min (first image build). Enhanced vs raw: same length, +1 dB, +7.5 dB above 14 kHz (air back), +2 dB 5–14 kHz,
  pause floor unchanged, no clicks. Joined (`vo_rejoin.py`, 0.7 s gap); `vo_take_check.py` OK on 191 sentences.
- **Problem found:** the 23 NOV take says the dropped line "A new film every Sunday, eleven thirty in the morning"
  (at 6:32; recorded 6:25 PM IST, ten minutes before the text changed). Owner chose to re-record, not cut.
  The app caps a take at 10:00 and the text runs ~10:09, so two blocks split at chapter 3: `vo_block1.txt`
  (4,111 chars, cold open → "What would you have done?") and `vo_block2.txt` (5,651 chars, "In nineteen ninety
  five…" → "Stay practical."). Block 1 of the 23 NOV take already matches the text, so only block 2 is needed.
  When it arrives: raw to Drive `vo/raw/`, `modal-enhance`, join at chapter 3 (gap ~1.0 s), take check, owner approval.
- **25 NOV, about 12:00 PM IST:** block 2 recorded (`phwr_b2_raw.mp3`, 5:49) and enhanced, then **retired before
  approval**: the owner dropped the QR/phone ask ("fatigue for the audience; make it even simple"). The mid-film ask
  is now "On the T-V? Just press Subscribe with your remote."; the landing keeps only "Subscribe, so you are there
  with me." (PLAYBOOK §15.6). `vo_block2.txt` rebuilt (5,535 chars): the owner records block 2 again; block 1
  (`phwr_b1_enh.wav`, cut at 262.72 s of the enhanced 23 NOV take) stands.

## Next, in order (session closed 23 NOV 2026, about 6:30 PM IST)
1. **Narration v2 APPROVED** (owner, 23 NOV). **The owner recorded the takes (see Audio above)** on Eleven v4 (Akash,
   Creative 0.0, similarity 50%). When the files arrive: `scripts/vo_take_check.py` on each, then the owner approves
   the audio (step 6).
2. C01 (RAPP-8 cleared 19 Nov) is still unverified: ask the owner for a PIB screenshot, else keep C31 wording.
3. From now: footage requests (NPCIL/DAE/PIB photos of Rawatbhata, the EMCCR, Kakrapar; Films Division archive), the
   Blender heroes with a 10-frame Modal bench first (free credit only, §14.1), the SRT with real spellings.
4. Copy this folder to Drive `Creator/English/phwr-700/` (not done on 23 NOV).

## Modal: inside the free credit (owner, 23 NOV: the US$20–40 estimate "won't work out")
Re-planned to PLAYBOOK §14.1 "Zero rupees a film": 4 heroes at 2560×1440 on an L4 with adaptive sampling and the
denoiser, benched on 10 frames first (expected about 8–15 s a frame × 2,160 frames = 5–9 GPU hours = US$4–7); the 4K
master on CPU about US$1–3. Together about US$5–10 of the US$30 monthly credit: no payment.

## Decisions made on 23 NOV (owner)
- Alternate rule: one bottleneck film, then one breakthrough or civilian film (PLAYBOOK §1.4).
- This film is the breakthrough film. **The next film is the 7 PM grid**, with the AI data-centre boom (US chip
  licence rule of 16 NOV 2026; "Ambani and Adani") as its hook (`projects/channel-research/2026-11-23/report.md`).
- Gemini Deep Research is used as a lead sweep, checked by us (PLAYBOOK §4).

## Backup
Text is in git. Copy this folder to Drive `Creator/English/phwr-700/` at the next session (no Drive upload was done
on 23 NOV).

## Audio for approval (25 NOV 2026, about 12:20 PM IST)
- Block 2 re-recorded with the remote ask (`phwr_b2v2_raw.mp3`, 5:47; earlier raws moved to Drive `vo/raw_done/`),
  enhanced on Modal (4 min), joined to block 1 (`phwr_b1_enh.wav`) with a 1.0 s room-tone gap at chapter 3:
  `phwr_vo_full_v2.mp3` / `phwr_vo_full.wav` in Drive `vo/`, 10:10, −22.5 LUFS, −1.1 dBTP.
- Checks: `vo_take_check.py` OK (190 sentences, 0.297 s a word); word-by-word transcript diff against `vo.txt`
  clean (only digit and name spellings); no artefacts added by the enhance (three flags were a raw mouth click
  and word tails). Alignment in `align/` (17 lines to check by ear before the lock).
- **Next:** the owner approves the audio → `vo_lock.py`, then footage and the build.
- **25 NOV, about 1:00 PM IST, outside audio review (owner's PDF):** CIRUS at 2:09 is said "Sig-rus" (our transcript
  agrees). Tested three spellings on Akash v4 (about 90 characters): "Cyrus" reads right; "Sigh rus" reads "Segrus".
  `config/pronunciation.csv`, `vo.txt`, `narration.md` and `vo_block1.txt` (4,108 chars) now say "Cyrus". The review
  suggested splicing one sentence; our rule is never to splice words into a take, so the owner re-records block 1.
  Block 2 (`phwr_b2v2`, enhanced) stands. Not taken from the review: "press Up" on screen (we never name an arrow) and
  "Sunday's drop" (no fixed day).
- **25 NOV, about 12:45 PM IST, final candidate `phwr_vo_full_v3.mp3`** (Drive `vo/`; `phwr_vo_full.wav` beside it):
  block 1 re-recorded with "Cyrus" (`phwr_b1v2`, 4:21) + block 2 (`phwr_b2v2`, remote ask), both enhanced on Modal,
  joined at chapter 3 with a 1.0 s gap at 4:22. 10:08, −22.3 LUFS, −0.9 dBTP. `vo_take_check.py` OK (190 sentences);
  word-by-word diff clean (CIRUS heard as "Cyrus"); no enhance artefacts. Waiting for the owner's audio approval, then
  `vo_lock.py`.

## AUDIO APPROVED AND LOCKED (owner, 25 NOV 2026, about 12:55 PM IST)
- `phwr_vo_full_v3.mp3` (Drive `vo/`), lock `ecbfc8f52df9`, 608.42 s voice + 15 s end card (YouTube end screen to
  the next film). `vo/timing.json` (190 sentences, 1,753 words, 60 fps), `vo/chapters.tsv` (7 chapters: 0:00 Canada
  walks out · 0:39 306 pressure cookers · 2:26 What breaks a tube · 4:21 India opens the heart itself · 6:37
  Kakrapar: the worst day · 7:45 From 306 to 392 · 9:29 What it means today), `vo/captions.en.srt` (voice spellings:
  the YouTube SRT is made at §15 with CIRUS, CANDU, NPCIL, TV and numerals), `vo/timing.md` (sentences to check).
- **Next:** footage requests (NPCIL/DAE/PIB photos of Rawatbhata, the retubing machine, Kakrapar; Films Division
  archive), the Blender hero bench on Modal (10 frames first, free credit only), then the word-by-word build.
- C01 (RAPP-8 cleared 19 NOV) is still unverified; the narration uses C31's wording ("began taking in its fuel"), so
  nothing waits on it.

## Footage and the build (26 NOV 2026, about 6:00 AM IST)
- Footage r1+r2 in Drive `footage/` (22 videos; 7 duplicated by two Termux runs, listed in `footage_log.md`).
  Gemini notes per clip in `footage_ai/`; best picks by chapter, checked on our own sheets, in `footage_log.md`.
  Key finds: NPCIL "Refurbishment of RAPS-3" (the real Rawatbhata face, yellow suits at the tubes), Films Division
  1980 "Nuclear Power: A National Achievement" (a 1980 PHWR face, tube making), 1983 Pickering TV news footage
  (**owner cleared 26 NOV**: 5–8 s, credited, never the anchor).
- Gemini API key saved as a network secret (Bearer, OpenAI-compatible endpoint); free tier = 20 requests a day per
  model (PLAYBOOK §11). `scripts/gemini_watch.py` vets downloaded clips.
- Blender hero 1 (`scripts/blender/phwr_hero.py`): the face reads; still to do: the flask's material, the lock seen
  from the side, an engineer for scale; then the 10-frame Modal bench.
- `word_map.md` part 1 (cold open + ch.1, S0–S44) written. Next: parts 2–3, then scenes and Remotion.

## The build begins (26 NOV 2026, about 6:45 PM IST)
- **Remotion project rebuilt** (`remotion/`, pinned 4.0.534; the old entry files were lost with `Creator`): `Film.tsx`
  (one shot list + overlays, 0.2 s dissolves, grain/vignette, the locked VO), `timing.ts` (`s0/s1/w0/w1` from
  `vo/timing.json`), `parts/kit.tsx` (the catapult film's proven kit + `Archive` print on the table + `ChapterCard`),
  `parts/drawings.tsx` (306 face, Rajasthan/Chambal and Kota maps from Natural Earth with India's official boundary,
  export file, design sheet, pot → tank → cooker, weights, tube wall vs pencil to scale, MAY 1974), `parts/geo.ts`.
  `public/assets/` links only `assets/media` and the VO wav (bundles stay small). `tsc --noEmit` clean.
- **Part 1 (cold open + ch.1, S0–S44)** written in `scenes/p1_open_ch1.tsx`; drawn shots checked on stills and fixed.
  Footage spans checked on our own sheets; clip list `media/clips.tsv` (`tools/prep_clips.py` now crops then keeps a
  4:3 shape with `,V`, and interpolates to 60 fps before upscaling). Two word-map spans were wrong and are replaced
  (`word_map.md` S12, S16–18): NP 00:50 is an NPCIL slideshow with burned-in years; FD80 25:20 is thorium beach sand.
- **Avoid in FDA (02/03_loy):** 00:08–00:14 and 03_loy 00:03–00:05, 00:12–00:13 show leaders (plan lock: no PMs).
- **Next footage request (r3):** a real Indian kitchen pressure cooker whistling (S24–25; Pixabay has none; drawn for now).
- **Hero 1 bench on Modal** started 26 NOV, 6:20 PM IST (`modal-blender` run 45823267785: `face`, frames 0–599 step 60,
  2560×1440, L4). Read its seconds per frame, write the cost here, look at the 10 frames (engineer placement), then the
  full 600-frame run if it fits the free credit. Part 1 needs `H1_face` (prepared 60 fps clip) before its 720p part.
- **Then:** parts 2–3 (ch.2–5, landing, end card), `cues.ts`, the 720p review cut on the runners.
