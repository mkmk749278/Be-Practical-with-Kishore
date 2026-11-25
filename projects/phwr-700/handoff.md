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
