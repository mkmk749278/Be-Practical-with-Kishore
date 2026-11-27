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
- **Renders moved to the GitHub runners, at most 15 at once (owner, 26 NOV, 6:42 PM IST)** after the Modal bench failed
  twice (a launcher path bug, fixed; then OptiX's denoiser weights missing in the container). `blender-render.yml`:
  bpy 5.2.2, 15-shard cap, frames to Drive `renders/<shot>/`.
- **Hero 1 bench on the runners** (run 45827156257, 10 frames, 2560×1440, 64 samples, OIDN): **about 12.3 min a frame
  on one runner**. The full 600 frames at that setting would need about 8 h a runner on 15 runners: over the 340-min job
  limit. Plan: 1920×1080 (upscaled at the master), 32 samples, every 2nd frame interpolated to 60 fps, and only the
  frames the cut uses (render 0–200 and 240–590): about 4 min a frame, about 75 min a runner on 15.
- **The look fails the art direction (our check of frames 0, 60, 240, 480):** a flat, bright grey room and a matte
  orange flask that reads as plastic, not the dim vault with a warm key; the engineer is in none of the 10 frames
  (0–540); the flask path and the lock (360–540) read well. Before any full run:
  darken the world, a warm hard key with haze shafts, darker end shield, worn paint and grime on the flask, place the
  engineer; test 4 stills at 640 px locally (`pip install bpy==5.2.2` in `.venv-blender`).
- **Then:** parts 2–3 (ch.2–5, landing, end card), `cues.ts`, the 720p review cut on the runners.

## 26 NOV 2026, about 8:00 PM IST (owner: "Always merge and continue": merge each PR ourselves and keep going)
- **Hero 1 look pass** (PR #18): dim vault, hard warm key through haze, solid caution-yellow flask (a scanned plate
  read as rust), engineer as a silhouette on the fuelling bridge, console off the face. 640 px tests checked.
  **Full render running** on 15 runners (run 45835464493, frames 0–598 step 2, 1080p, 32 samples) → Drive
  `renders/face/`. Then: interpolate to 60 fps into `assets/media/clips/H1_face.mp4` (prep with minterpolate),
  stills of S0, S7, S8, S48, S78 in Remotion.
- **Chapter 2 built** (PR #19, composition `p2`): H3 is a drawn channel section (decided 26 NOV: the physics reads
  better in section, no render time); the Pickering news stays at S59 only (6.4 s in the film). Stills checked.
- **Footage request r3** (when the owner next runs Termux): an Indian kitchen pressure cooker whistling (S24–25), a
  steel tumbler sweating on a sunlit table (S66–67). Both are drawn until then.
- **Next:** chapter 3 (S80–, "India opens the heart itself"), chapters 4–5, the landing and end card; `cues.ts`;
  the 720p review cut on the runners (≤ 15 jobs).

## 26 NOV 2026, about 9:30 PM IST: the whole film is built (PRs #19–#21, merged)
- Compositions `p1` (S0–S44), `p2` (S45–S79), `p3` (S80–S121), `p4` (S122–S189 + 15 s end card), `phwr` (all).
  Every drawn shot checked on stills and fixed; every word cue checked against `vo/timing.json` (0 missing).
- **H3 and H4 are drawn** in one section language (decided 26 NOV); the plan's Blender list is now H1 only.
- **Footage decisions:** K06 unusable (text-covered slideshow); K05 1:16–1:18 (the PM) excluded; NP11 0:22 is Tarapur;
  Pickering news 6.4 s in all; unnamed plants carry ILLUSTRATIVE FOOTAGE; names (Chaturvedi, Arya) only over places.
- **Quotes:** the 1995 trade weekly and Business India lines are typed slips "AS QUOTED" (no facsimile pages); the
  heart-transplant line has no quotation marks ("AS REPORTED", C27 records a likening).
- **Waiting on:** hero 1 full render (run 45835464493, started 7:35 PM IST, 15 runners) → pull Drive `renders/face/`,
  interpolate the 30 fps frames to `assets/media/clips/H1_face.mp4` (60 fps), stills of S0, S7, S8, S48, S78, S87, S183.
- **Next, in order:** (1) H1 clip in, stills; (2) `cues.ts` (the clunk between S7 and S8, the cooker whistle after
  S25, the stamp, the alarm) and the music bed (§12; `config/music_library.csv`); (3) upload `assets/media` and the VO
  to Drive `English/phwr-700/render-media`, check `remotion-render.yml` against this project (it predates the rebuild),
  render the 720p review cut on ≤ 15 runners; (4) our own review (§13.1), then the Gemini `cut-audit` handoff.
- **Still open from before:** footage r3 (kitchen cooker whistling, a sweating steel tumbler); C01 (RAPP-8 cleared
  19 NOV) unverified, not used on screen.

## 27 NOV 2026, about 12:50 AM IST: review cut r2 rendered, our review passed, Gemini cut audit sent
- **H1 done:** the full runner render (300 frames, 15 runners) joined to `H1_face.mp4` (60 fps, 9.95 s); stills at all
  seven uses checked.
- **Sound:** 24 real CC0 recordings (Freesound, licence checked on each page; `media_manifest.csv`), 51 cues in
  `sound/sfx.json`; music from the library placed by Gemini's ear-checked map (`review/gemini_second_opinion_check.md`:
  The Boardroom in the cold open, The Verdict left out). Mix −14.1 LUFS, −2.5 dBTP (`scripts/score_mix.py`,
  oversampled limiter).
- **r1 → r2:** r1 had 28 single-frame jumps, mostly cuts inside source clips, plus KAPP-4 camera flashes. Every clip is
  now trimmed to one continuous shot (`media/clips.tsv`), with flash-free spans. **r2** (run 45879178046): 10:23, 720p
  60 fps, −14.2 LUFS, −2.2 dBTP, 0 flash frames, 5 jumps, all of them on purpose (the 1:54 Pokhran hard cut; the 962-day
  counter at 2:33–2:35). Drive: `renders/phwr_review_r2_720p.mp4`
  (https://drive.google.com/file/d/1i5DC82-fvYIOYdaqCczcrMaW8vgU9lJO/view).
- **Gemini `cut-audit` sent** at 12:45 AM IST (with a 360p proxy, 9.4 MB, in `handoff/`). Next: `gemini_handoff.sh pull
  phwr-700` → `review/gemini_cut-audit_check.md` (CONFIRMED / PARTLY / NOT CONFIRMED) → fixes → r3 if needed → the
  owner approves the cut → 4K master once → the package.
- **Open, optional:** hero 2 pot drawing is weak; a real Indian cooker whistle (owner asked for a 3 s phone recording);
  footage r3 (cooker, tumbler); C01 unverified (not on screen).

## 27 NOV 2026, about 8:20 AM IST: Gemini's cut audit of r2 checked, fixes made, r3 rendering
- Gemini's reply (`review/gemini_cut-audit.md`, FIXES_REQUIRED) checked lead by lead on r2 frames, the scene code and
  the mix: `review/gemini_cut-audit_check.md` (16 confirmed or partly, 4 not confirmed or not taken).
- **Worst find:** the 2:45 "Kakrapar · fuelling machine" shot was NPCIL's CMD talking (a typo span, 415 for 4:15).
  K05_fm re-cut to 261.75–264.20 s; tag "A FUELLING MACHINE · 700 MW".
- **Picture:** eight drawn shots no longer open empty (pot → row of pots, weight on a cord, year cursor, tool ghost,
  cost slip and rupee stack, blank calendar pages, 1ST IN INDIA → 2ND IN THE WORLD, warming bulbs, ghost domes);
  "HALF BUILT" blueprint on the 1970s photo; every counter on a dark pill; whole-India maps fit Ladakh to Kanyakumari.
- **Sound** (`sound/sfx.json`): whistle on its word (−14), vault door first slam only (the pause after S79 is dry),
  cutter trim was the recording's talking pre-roll (now the cut), alarm 0.8 s, steam hiss shorter. New mix in Drive
  `mix/mix.wav` (r2's is `mix/mix_r2.wav`), −14.1 LUFS, −2.5 dBTP.
- `scripts/gemini_handoff.sh pull` now reads front matter written on one heading line.
- **Next:** r3 (run 45930701547) → Drive `renders/phwr_review_r3_720p.mp4` → our review (§13.1) → Gemini `cut-audit`
  on r3 → the owner approves the cut → 4K master once.
- **27 NOV, about 8:50 AM IST: r3 rendered and passed our review** (run 45930701547): Drive
  `renders/phwr_review_r3_720p.mp4` (https://drive.google.com/open?id=16aJro5KYVRBKQUaDx5hw9aLj8Qb4w01l), 10:23,
  720p 60 fps, −14.1 LUFS, −2.2 dBTP, 0 flash frames, one hard cut (1:54, designed); the two "single-frame jumps" are
  0.2 s dissolves to bright footage (also in r2). Every r3 fix checked on frames of the render itself.
- **Gemini `cut-audit` on r3 sent** at 8:46 AM IST (360p proxy, narration and our r2 check in `handoff/`). Next:
  `gemini_handoff.sh pull phwr-700` → check → the owner approves the cut → 4K master once → the package.

## 27 NOV 2026, about 11:15 AM IST: both Gemini r3 audits checked, r4 mix, 4K master rendering
- Gemini's two r3 replies (`review/gemini_cut-audit_r3.md`, `_r3b.md`): picture locked, audio-only fixes. Checked on
  the real r3 stems: `review/gemini_cut-audit_r3_check.md` (all sound leads confirmed or partly; two numbers not taken).
- **The owner: "Fix everything and render in 4k"** (27 NOV), taken as the cut's approval.
- **r4 mix:** music levelled on the bus and about 11 dB under the voice (was 22); 2 s equal-power crossfades; Pokhran
  and the walk-out under The Boardroom, the warm strings on "Indian engineers finished it on their own", the outro on
  "Subscribe"; the rail roar, the crashes on the weight and the diagram cut, and the slam on "doctor" gone; every cue
  low-passed or shortened as needed and fitted 4 dB under the voice. −14.2 LUFS, −2.2 dBTP. Drive `mix/mix.wav`
  (r3's: `mix/mix_r3.wav`); `renders/phwr_review_r4_720p.mp4` = r3 picture + r4 mix.
- **4K master:** run 45945459762 (15 runners, scale 2, from `main`), joins with Drive `mix/mix.wav` (r4) →
  `renders/phwr_master_4k.mp4`. If the join ran before the r4 mix was up, re-join with `join_from`.
- **Next:** check the master (§13.1 measures on the 4K file, three frames each side of every seam), then the
  package (§15): SRT with real spellings, thumbnails, metadata, the fresh-facts gate within 24 h of upload.

## 27 NOV 2026, about 1:30 PM IST: cut approved, 4K master, release today 7:00 PM IST
- Gemini on r4: APPROVED (`review/gemini_cut-audit_r4.md`); **the owner approved the cut** ("Ok approved").
- **4K master:** the runners rendered all 21 shards (run 45945459762), but the join's copy to Drive hung for 45+ min,
  so the shards were pulled as artifacts and joined here with the r4 mix (concat, stream copy): 3840×2160, 60 fps,
  623.42 s, 1.6 GB, −14.2 LUFS, LRA 2.9. Every frame's luma matches the approved r4 cut (max 2.4/255, no flashes);
  three frames each side of every seam checked. The run was cancelled. Drive: `renders/phwr_master_4k_local.mp4`.
- **Fresh-facts gate (27 NOV):** RAPP-8 has not gone critical (AERB cleared its first approach to criticality on 19
  NOV: World Nuclear News "Start-up milestones for Indian plants"), so "the date to watch" stands.
- **Package:** `youtube/metadata.json` (title, description, chapters, tags, playlist, pinned comment and sources
  reply), `youtube/phwr-700.en.srt` (`make_srt.py`: numerals, CIRUS, NPCIL, TV; 42-character lines), thumbnails
  (`make_thumbs.py`, frames of the film: main "1974" on the face and flask; "LEFT HALF-BUILT"; "1974" on the NPCIL
  worker), in Drive `youtube/`.
- **Uploaded 27 NOV, about 12:40 PM IST: https://youtu.be/0BgAi3dGfl0, Private, scheduled 7:00 PM IST** (owner chose: "I upload, you schedule"; slot today 7:00 PM IST):** `scripts/yt_upload.py` rebuilt (resumable,
  thumbnail, SRT, playlist, containsSyntheticMedia false, made for kids No). Left for the owner in Studio: Test & Compare
  with the two challengers, the end screen (Arjun film + playlist), pinning the comment.
- **At the slot:** `python3 scripts/yt_upload.py projects/phwr-700 --comment <id>` posts the comment and its sources
  reply; the owner pins it. Studio checks at 24 h, 7 d, 28 d (§15.5).
