
## Session 4 (2026-11-13): narration v2 written and reviewed; waiting for the owner
- `vo.txt` (the recording text) and `narration.md` (v2, with the promise check, the creative pass and the review's
  changes); `review_narration_v1.md`; `words.txt` (subject words for the lint); new rows in `claims.csv` and
  `config/pronunciation.csv`. Both gates pass.
- 10,273 characters, so two takes, split at "Has anyone made it work?" (chapter 4).
- **Waiting for the owner:** approval of `narration.md`. No audio before that.
- **Next after approval:** `vo_blocks.py` with the split, `eleven_tts.py` (check the credit balance first),
  `vo_take_check.py`, `vo_rejoin.py`, the joined MP3 to Drive and to the owner. In parallel: the Blender heroes
  (H1, H3, H4) and the second footage request.

## Session 5 (2026-11-13): outside review applied; still waiting for the owner
- The owner attached an outside review "for refinement only". Its physics matches C22 and C23. Taken: the count in
  three blocks of its own (real-time pause, no edit of the take), "Bilu" respelt "Beeloo" in `vo.txt` and
  `config/pronunciation.csv`, TV-first notes for S1, the power spike and S3 in `plan.md`. Not taken, with reasons, in
  `narration.md`. Both gates pass (10,282 characters, still two takes split at chapter 4).
- **Owner, 2026-11-13: narration approved** ("max 10000 characters in one block, split where a natural split happens").
- **Audio:** two takes (Akash, Eleven v4, Creative 0.0, 50%, MP3 192 kbps), split at chapter 4 ("Has anyone made it
  work?"): `vo_blocks.md` built with `--limit 6127` (blocks 6,127 and 4,148 characters). No re-takes. Credit before:
  19,005 left; the API billed 4,521. Joined with `vo_rejoin.py`, gap 1.25 s at the chapter break, room tone −73 dB.
  Then 0.25 s of the take's own pause (−77 dB) added before "Three." so the count runs evenly (onsets 0.95 s and 0.99 s
  apart; PLAYBOOK §6.6 allows lengthening pauses with room tone; no word touched). **642.98 s (10:43)**, review MP3
  −16.7 LUFS, −1.6 dBTP (two-pass linear loudnorm).
- `align/` (script.tsv 212 sentences, align.json, sentences.json): 206 high confidence; the 6 flagged are short punch
  lines ("No.", "So steam is gone.", Nanda's two lines). `vo_take_check.py`: OK.
- Drive `Creator/English/carrier-catapult/vo/`: `cat_vo_full.mp3`, `cat_vo_full.wav`, both takes with their `.txt`.

## Session 5, continued (2026-11-13): audio approved and locked
- **Owner, 2026-11-13: "Audio aproved".** Locked with `vo_lock.py` on `cat_vo_full.mp3` (SHA-256 892915fe…,
  642.98 s, 60 fps, 4 s outro): `vo/timing.json` (212 sentences, 1,877 words, 7 chapters), `vo/captions.en.srt` (real
  forms from `vo/caption_forms.tsv`: Bilu, INS, USS, DRDO, dates, km/h, ₹ with Indian grouping), `vo/lock.json`.
  The two flagged sentences ("One.", "No.") sit where the first alignment put them; nothing set by hand.
  Render copy `vo_full.wav` (48 kHz) in Drive `English/carrier-catapult/vo/`.
- Chapters (description): 00:00 Rafale on INS Vikrant without a catapult · 00:50 Why INS Vikrant has a ski-jump
  ramp · 01:59 India's 1961 steam catapult and the 1971 war · 04:41 How an electric catapult (EMALS) works · 06:25
  China's Fujian vs America's USS Ford · 07:48 DRDO's electric catapult demonstrator · 09:32 What India needs next.
- **Second footage request** (`footage_requests.md` r2): one Termux line, nine clips (Sea Hawks and Alizés on the
  first Vikrant, 1971 east, the Rafale M Goa ski-jump, MiG-29Ks and a trap landing on Vikrant, the first EMALS launch,
  Ford launches, Fujian's KJ-600), and one Cowork request for stills (DRDO's demonstrator, the first Vikrant at
  Belfast, Cdr Roy Chowdhury's photo). The owner ran both (Antigravity in place of Cowork), 2026-11-13.
- **`word_map.md` written** on the locked timing: every sentence group with its base, its word cutaways and its idea
  level; the slot motif's five returns; S1, S2, S3 and a set piece per chapter; labels; the stock list.
- **Next:** the Blender heroes H1, H3, H4 (`scripts/blender/catapult_hero.py`, rendered by `blender-render.yml`);
  stock via the Pixabay API; contact sheets and `media_manifest.csv` once r2 lands; then the Remotion build.

## Session 5, continued (2026-11-13): footage in; the lorry corrected; audio r2
- **In Drive:** all nine r2 clips (`footage/01_…` to `09_…`, `fetched.csv`); stills from Antigravity in
  `footage/cowork/stills/`: Cdr Roy Chowdhury's official portrait and the Vir Chakra handover (PIB, usable with
  credit); two IWM Sea Hawk photos under IWM's non-commercial licence (H4 reference only, never in the film).
  Not found: the Belfast commissioning photo; any DRDO launcher photo.
- **Fact corrected:** Antigravity found DRDO showed a *railgun* trailer at Aero India 2025. Checked: Janes
  (14 Feb 2025) and DRDO's clippings (NPC15to17Feb2025) show only a railgun model; the "EMLS on a trailer" rests on
  one idrw post. C33 rewritten; the four lorry lines now say "a small test model" (C32, as reported).
- **Owner: "Only record what needed, adjust that in audio".** Four paragraphs re-recorded (314 credits billed)
  and placed into the approved audio at their paragraph pauses, levels matched (≤1.1 dB), pauses kept;
  `vo_take_check.py` OK; re-locked: **644.15 s, SHA-256 f416a57d…**, 211 sentences. Drive `vo/r2/`. The old
  lock's audio is still in `vo/`. New lines at 0:29.7, 7:55.5, 9:23.5, 10:18.5.
- `word_map.md` retimed to r2 (old S156 removed; later ids −1) and its rows point at what exists. PLAYBOOK: two
  lessons (paragraph re-records; "shown at" needs the event's own coverage).
- **The owner sent an outside audio audit of r2 (all four edits pass, levels within ~1 dB):** r2 accepted.
- **Footage vetted** (contact sheets in the gitignored `assets/footage/sheets/`), spans and verdicts in
  `media_manifest.csv`. Key finds: the Navy's landing full-frame in India Today's clip at 10.0–14.5 s (crop the logo):
  the first frame; real Indian Sea Hawks on the first Vikrant (roundel, IN157, a launch off the bow at 1.0–2.5 s, the
  nose-wheel match-cut frame at 8–9.5 s); the real EMALS trough at Lakehurst (10–19 s); a clean Ford launch (1–9 s).
  Rejected: the "Goa" compilation (its Rafale shots are animation; S7 is a map pin now), the PM's vertical clip except
  7–9 s, IWM photos (non-commercial).
- **Stock:** Pixabay API: ceiling fan, coil winding, steam, an Indian city road (Drive `footage/stock-pixabay/`).
  Request r3 in `footage_requests.md` (Pexels, for the laptop): flyover end, cooker, family under the fan, meter,
  lattu, kirana balance, Indian engineers. **With the owner.**

## Session 5, continued (2026-11-13): hero shots rendering
- `scripts/blender/catapult_hero.py`: **H3 store** (the motor generator spins up, copper glows, the energy runs out
  at 600), **H4 catapult** (1961 cutaway: the piston fires on steam, the shuttle drags the jet), **H4 drum** (cracks
  glow, three steel bands ratchet tight at 420/560/700), **H4 room** (the gauge needle swings into the red and holds,
  the camera pulls back through the empty boiler room). Test stills checked by eye at each fix.
- **H1 dropped** (tried and judged crude): the deck moments now use the Navy's own footage (TRAP, LAND, LAND-NDTV);
  the flat-to-ramp morph and the hull cutaway become Remotion drawings (R) on the drafting table. `word_map.md` updated.
- **Rendering on GitHub (owner, 2026-11-13: "all 20 runners are free")**: blender-render runs 21 store (6 shards),
  22 drum (6), 23 catapult (4), 24 room (4); 1920x1080, 24 samples, every 2nd frame; about 54 s a frame on a runner,
  so about 75 minutes. A check-in is scheduled to collect, check and upload them to Drive `renders/`.
- **Next:** collect the renders; the Remotion build (word map scenes, R drawings: the deck plan, the balance, the
  radar circles, the side-elevation morph, the hull cutaway, the working of the 19 units, the engine bars, the DOT&E
  bars, the 17 m vs 90 m pull-back, India maps on the official boundary); then music and sound; the 720p review cut.
- **Hero renders done (2026-11-13):** all 20 shards succeeded; frames checked (counts, no dark frames, contact
  sheets); encoded at 60 fps (every 2nd frame held) to Drive `renders/`: `cat_H_store.mp4` (16 s), `cat_H_drum.mp4`
  (16 s), `cat_H_catapult.mp4` (10 s), `cat_H_room.mp4` (10 s). Logged in `media_manifest.csv`. The 16-bit frames
  stay in the gitignored `assets/renders/` (not in Drive: 7.7 GB). A shard takes about 2.3 h on a runner (not 75 min).
- **Next:** the Remotion build (word map scenes and the R drawings), then music and sound, the 720p review cut.

## Session 5, continued (2026-11-13): the Remotion build
- `remotion/` (Remotion 4.0.534, comp `Catapult`, 648.15 s with the 4 s end card), built from Matsya's skeleton:
  `scenes/p1_open_ch2.tsx`, `p2_ch3_ch4.tsx`, `p3_ch5_end.tsx` (every shot and tag on its word from `vo/timing.json`),
  `parts/drawings.tsx` (the deck plan and slot, meter, ramp side, radar circles, cooker, steam split, the 1961
  elevation, the hull cutaway, the fan unrolled, the working, two meters, engine bars, land track, DOT&E bars, the
  document pose, 17 m vs 100 m, China/India, the two ships, the honest sum, three slots, dates, ramp or catapult),
  `parts/SeaMap.tsx` (India's official boundary). Credits and honesty tags are drawn outside the reframing.
  Test stills checked; fixed: SVG glow on horizontal lines (filterUnits userSpaceOnUse), cut-off credits, overlaps.
- `media/clips.tsx` → 41 clips by `tools/prep_clips.py` (Drive `render-media/` before the GitHub render).
- Photos: the "portrait" from Antigravity is a memorial graphic with captions not in claims.csv: only the face and
  the medal are cropped and used (`roy_face.jpg`, `vrc_medal.jpg`).
- Sound: `sound/score.json` (12 library tracks along the feeling curve; no music under the landing and the count),
  `sound/sfx.json` (the three-second motif: whine, thump, wind; steam hiss and clang for 1961; the bands);
  `scripts/score_mix.py` gained whine, thump, wind, steam_hiss, clang, whistle. Mix: −14.0 LUFS, −1.4 dBTP, in Drive
  `mix/`. `vo-render/` holds lock.json and vo_full.wav.
- **Next:** finish the clips, sync `render-media/`, render the 720p review cut on GitHub, our own review
  (`review-cut`), then the independent viewer review.

## Session 5, continued (2026-11-13): the review cuts
- r1 (run 43399044281), r2 (43404314348), r3 (43407401810): measured and read against the words each time; every
  fix in `review/review.md`. r3: no freezes, −14.0 LUFS, −1.4 dBTP. One overlap left in r3 ("FAR SHORT" over the
  181 label, 7:16), fixed in code for the next render.
- **Owner, 2026-11-13: share r3 for the independent viewer review.** r3 shared "anyone with the link" (Drive file
  17N1kR999AlaYPqynqS9aPBANWBG4Rggg). Review session `session_019NnLekPrc9ecvtsWJk5rj8` (no repo); its answer →
  `review/review_viewer_r3.md`, then fixes, `review_ack_r1.md`, the owner's approval of the cut, the 4K master.

## Session 5, end (2026-11-14): viewer review collected → handoff (owner: "after collecting review, prepare handoff
## and merge work; we open a new session later")
- **The independent viewer review of r3 is in:** `review/review_viewer_r3.md` (verdict: not ready; publishable after
  its fixes 1–5; scores 7–9; peak at the boiler/Bilu/1971 stretch; drifts at the repeated flywheel/Ford shots, the
  document cards, and the end).
- **State:** composition on `main` = r3 + one fix ("FAR SHORT" moved clear of the 181 label). Audio locked
  (`vo/lock.json`, f416a57d…), mix in Drive `mix/` (−14 LUFS). Clips in Drive `render-media/` (37) and in the
  gitignored `assets/media/` of this session only. Cuts: Drive `renders/carrier-catapult_review_r{1,2,3}_720p.mp4`;
  **r3 is shared "anyone with the link"** (file 17N1kR999AlaYPqynqS9aPBANWBG4Rggg): unshare it once the review round
  is closed.

### Next session: start here
1. **Pull the media first:** `scripts/gdrive_pull.sh English/carrier-catapult/render-media projects/carrier-catapult/assets/media`
   and `.../vo-render` → `assets/vo`; `cd remotion && npm ci`. Test stills: `npx remotion still` on a bundle (see
   this file's earlier sections); shot list and run-out check: the esbuild snippet in `review/review.md`'s history
   (bundle `src/_shots.ts`, list every shot's start and length; flag clips whose footage is under half the shot).
2. **Check every review point against the composition and a frame before changing anything** (§13.3), then fix and
   write `review/review_ack_r1.md` (FIXED / FIXED NEXT / OPEN / CHECKED with evidence). My first read of its points:
   - **#1 real:** S2's "FIRST VIKRANT · 1961" tag sits on the *new* ship's deck plan (the ramp hatch is drawn).
     Either draw the 1961 ship (flat deck, slot to the bow; `Elevation61` already exists in side view) or change the
     tag (e.g. "INDIA'S FIRST CARRIER HAD ONE · 1961") so it no longer labels this outline.
   - **#2 real:** tags sit at y 760–860 of 1080 (`tag(..., 140, 860, ...)` in the scene files): move every lower-third
     to ≤ 740 and the size up (subtitles take the bottom ~15% for a third of the audience). Also `Label` size.
   - **#3 real (measured):** `sound/score.json` `duck_db` −20 → about −26 and `bed_rms_db` −24 → −28; the stamp at
     S150 and the cue near 6:28 (`w:126:power` impact_low) down 6 dB in `sound/sfx.json`; re-run `score_mix.py`,
     upload `mix/mix.wav`.
   - **#4 real:** `ThreeItems` row runs off the right edge: pull the third item in (x 1560 → 1450) or scale the row.
   - **#5 real:** `Doc` cards: larger (the line in focus big, the rest small), less time each; merge the White House
     and General Atomics cards (S148–150) into one split.
   - **#6:** a Sea Harrier picture needs a licence-clean source (none in hand: search Wikimedia Commons for an
     Indian Navy Sea Harrier, CC BY / PD); animate `Elevation61` (it already seals the slot and lifts the ramp on
     S83: check the frame the reviewer saw).
   - **#7:** the market balance (S24–30): keep the real Indian picture, but cut it to two shorter shots and add the
     ramp drawing's load bar; or replace as suggested.
   - **#8:** repeats: H_store at S120/122/124/135, FORD_launch/FORD_cat ×6, LAND_ramp ×3, H_drum ×4: vary.
   - **#9:** the islands line is a *new fact on screen*: only with a source in `claims.csv`, else skip.
   - **#10:** a 20 s end card means re-locking with `--outro 20` (`vo_lock.py`) and re-mixing (the score's last slot runs
     to `end`); the speed counter from 0 (S106: check, it already counts from 0 on "standing"); blurred fills behind
     the vertical clips (the `Insert` kit already blurs a copy behind: check 1:04 and 4:22).
3. Render r4 (720p, `remotion-render.yml`, 11 runners), our review again, send the owner r4 + `review_ack_r1.md`;
   **the owner approves the cut**, then the 4K master (`scale 2`), then the package when asked.
4. Before upload: the fresh-facts gate (PLAYBOOK §8): the `fresh` rows in `claims.csv` (the next carrier's status,
   the US steam plan, the rupee rate for $1.321 billion).

## Session 6 (2026-11-14): viewer-review fixes → r4
- Every point of `review/review_viewer_r3.md` checked on stills, fixed in code: `review/review_ack_r1.md` (FIXED 1–10,
  islands line not added: no source). New drawings: `RampLoad`, `Cycle45`, `Queue`, `PriceShip`, `DocPair`; `DeckPlan
  oldAt` (the 1961 ship); lower-thirds moved above the subtitle zone in `common.tsx` `tag()`.
- Sea Harrier photo (U.S. Navy, PD) in Drive `render-media/photos/sea_harrier.jpg`, logged.
- End card 20 s: `vo/timing.json` outro 20 (39,849 frames; same as `vo_lock.py --outro 20`). `scripts/score_mix.py`:
  "end" = picture end. New mix in Drive `mix/` (−14.0 LUFS, −1.4 dBTP; voice −15.0 vs bed −35.6 LUFS).
- **r4 dispatched:** run 43578275297 (6 runners) → Drive `renders/carrier-catapult_review_r4_720p.mp4`.
- **Next:** our review of r4 (freeze, loudness, frames at every changed beat), then r4 + `review_ack_r1.md` to the
  owner for approval; unshare r3 (Drive file 17N1kR999AlaYPqynqS9aPBANWBG4Rggg); then the 4K master.
- **r4 (run 43578275297) checked:** −14.0 LUFS, −1.4 dBTP, no black; frames at every changed beat right. Found and
  fixed: the 1961 label touched the old ship's island, the document heads were cut off, the 20 s end card held
  still (freezes from 10:45). **r5** (run 43580873877, Drive `renders/carrier-catapult_review_r5_720p.mp4`, file
  1TceL2huLkdlBnb2eP475N5WbNGitBa4P): −14.0 LUFS, −1.4 dBTP, 11:04, no freezes, no black; the three spots checked.
- **Next:** the owner approves r5 (or asks for changes); then unshare r3 (17N1kR999AlaYPqynqS9aPBANWBG4Rggg), the 4K
  master (`scale 2`, same workflow), the package when asked, the fresh-facts gate within 24 h of upload.

## Session 7 (2026-11-15): the owner's notes on r5 → r6
**Owner, on r5 (screenshots):** the market balance (S24–30) and the flyover (S17) "not at all matching": remove both;
the pressure cooker: "show the real one"; the 3D shots: "concentrate more and get the best".
- This session started from `main`, which did not have r4/r5: the r4/r5 work sat on the unmerged branch
  `claude/continue-mdzoqo`; it is merged into `ccr-63b72672-k96ytx` (this session's branch).
- **3D rebuilt:** `scripts/blender/catapult_hero2.py` (scanned CC0 materials via `ph_assets.py`, HDRIs, haze, DOF,
  keyframed motion blur). Rebuilt with the same timings: catapult (now twin cylinders in a red-faced cutaway, a
  1950s jet on its bridle), drum (riveted lap seams, rows of generating tubes, hot cracks), room (a Bourdon gauge on
  its pigtail, hazy boiler room), store. New: **deckrun** (S17, the pilot's seat up the ski-jump into the sky) and
  **rampjet** (S24–26, behind a loaded jet: afterburners on "engines", off the lip on "lighter").
- **Render:** run 43741411807 (`blender-render.yml`, now one run for several shots, 6 jobs at a time, 30 jobs):
  deckrun 0-299, rampjet 0-449, catapult 0-479, drum 0-959, room 240-599, store 0-959, step 2, 24 samples.
- **Cooker:** three real Commons photos (stove PD; the weight and the release CC BY-SA 4.0, credited on screen) +
  the Pixabay steam (screen blend). `cooker_weight.jpg` is in `assets/media/photos`; the other two were rate-limited
  by Wikimedia (429) and retried in the background; check `assets/media/photos/cooker_{stove,steam}.jpg` are JPEGs.
- **Remotion:** `p1_open_ch2.tsx`: flyover → `H_deckrun`; balance → `H_rampjet` (S24) + `RampLoad` (S27–31);
  cooker drawing → the three photos. Clip names expected: `H_deckrun`, `H_rampjet` (+ the four rebuilt `H_*`).
- **Next:** collect the frames (artifacts `<shot>_<range>`), check them, encode `cat2_H_*.mp4` at 60 fps (each frame
  held twice) to Drive `renders/` and `render-media/clips/H_*.mp4`; stills of S17, S24–31, S47–50 and every hero
  use; render r6 (720p), our review, then r6 to the owner.

## Session 8 (2026-11-17): the package
- **Owner: "start the catapult package".** Everything in `youtube/` and Drive `English/carrier-catapult/youtube/`
  (source pictures in `youtube/src/`): `thumb_a.jpg` main (HAD ONE. 1961.), `thumb_b.jpg` (NO CATAPULT, red),
  `thumb_c.jpg` (3 SECONDS, the deck cut open on glowing coils), `metadata.json` (locked title + 2 alternatives,
  description, chapters from `vo/timing.json`, playlist, slot, tags, pinned comment), `vo/captions.en.srt`.
- **Thumbnail pictures:** Canva's image generator (as for Matsya), text prompts from the locked concept; the first
  main picture had a twin-tail jet and a lit ramp, so it was edited to a single-fin Rafale shape, a curved ski-jump
  and the band ending under the jet. Words by `youtube/make_thumbs.py` (new `--side right`). Checked at 168×94.
  Promise check: sentence 1 confirms all three (the Rafale on Vikrant, 1961, the missing catapult; 3 seconds at 0:30).
- **Fresh-facts gate (web search, 2026-11-17):** no DAC/CCS approval of the next carrier; no published outcome of the
  US steam plan; the Rafale landing holds. The rupee is about 94 per dollar, so $1.321 billion is about Rs 12,400
  crore; **the owner kept "around eleven thousand crore" as said** ("we used around"). Gate valid until 18 Nov:
  re-run it if the upload is later.
- Master: Drive `renders/carrier-catapult_master_4k.mp4`, md5 cb1a3ec6581cae698ae3bbae870533a0, 11:04.
- **Next:** the owner picks the main thumbnail and says when to upload; upload by `scripts/yt_upload.py` (private,
  `publishAt` Sunday 22 Nov 11:30 IST = 06:00 UTC, our SRT, playlist, AI use No); unshare r3
  (17N1kR999AlaYPqynqS9aPBANWBG4Rggg); after upload: end screen, Test & Compare (b, c), pin the comment at release.
- **Uploaded 2026-11-17:** video **`7n1ECxfW-2o`**, private, `publishAt` 2026-11-17T11:00:00Z (**today 4:30 PM IST**,
  owner), main thumbnail **B (NO CATAPULT)** (owner), our SRT, playlist Practical India, AI use No; processing done.
- **Title changed by the owner** to the outside reviewer's "Why India's ₹20,000 Cr Aircraft Carrier Has No Catapult"
  (for CTR); the cost is PIB's "close to Rs. 20,000 Crs" (claims C48). Set by the API; `metadata.json` updated.
- **Open:** pin `pinned_comment` at 4:30 PM IST; end screen (Studio: the AIP or Tejas film + subscribe); Test &
  Compare with `thumb_a.jpg` and `thumb_c.jpg`; unshare r3 (17N1kR999AlaYPqynqS9aPBANWBG4Rggg); Studio at 24 h.

## Notes recovered from the session logs (16 NOV; their exact place in this file was lost)
- **Renders done (2026-11-16):** runs 43742506996, 43783579469 (drum/store timeouts redone in smaller jobs),
  43784249063 (catapult in a lit hangar, gauge fill hidden from the glass), 43792152001 (deckrun/rampjet: the two
  lead lines were coplanar and rendered black where they met; fixed). Owner: "use all 20 runners" (workflow input
  `parallel`). Clips encoded (frames held twice; room with a 4 s lead so its time matches the render's frame numbers)
  → Drive `renders/cat2_H_*.mp4` and `render-media/clips/H_*.mp4`; cooker photos → `render-media/photos/`.
  Stills checked at S17, S24–27, S47–50 and every hero use.
- **r6** dispatched on `remotion-render.yml` (20 runners) → Drive `renders/carrier-catapult_review_r6_720p.mp4`.
- **r6 checked (2026-11-16):** run 43799836735; Drive `renders/carrier-catapult_review_r6_720p.mp4` (file
  1A5nFomwWxIsZCpRhvVXRRLv_ySJtSfOO): 11:04, −14.0 LUFS, −1.4 dBTP, no freezes, no black; frames at every changed
  beat right. **Next:** the owner approves r6 (or asks for changes); then unshare r3, the 4K master, the package.
- **Owner approved r6 (2026-11-16): "render in 4K".** 4K master dispatched on `remotion-render.yml` (scale 2, 20
  runners) → Drive `renders/carrier-catapult_master_4k.mp4`. The cut is locked: no more edits. Next: check the master
  (loudness, freeze, length 11:04), unshare r3 (17N1kR999AlaYPqynqS9aPBANWBG4Rggg), the package when the owner asks,
  the fresh-facts gate within 24 h of upload.
- **4K master done (2026-11-16):** run 43823741430 (the first, 43816390250, timed out at 30 s on 4K video frames:
  `render_shards.mjs` now waits 2 minutes). Drive `renders/carrier-catapult_master_4k.mp4` (file
  1l7t3akrRQGBQD7cpmdb7VDnxW0nTdV7z, 1.7 GB). **Next:** unshare r3 (17N1kR999AlaYPqynqS9aPBANWBG4Rggg); the package
  (thumbnails, title, description, metadata) when the owner asks; the fresh-facts gate within 24 h of upload.
