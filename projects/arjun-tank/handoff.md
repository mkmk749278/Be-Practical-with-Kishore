> Recovered 2026-11-23 from the 18 NOV session log (last edit 18 NOV, 08:38 UTC).

# Arjun tank film: handoff

## State (2026-11-17)
- Topic chosen by the owner after `projects/channel-research/2026-11-17/report.md`. Plan v2 approved (title "India
  Ordered 118 Arjun Tanks. Where Are They?", thumbnail WHERE'S THE ENGINE?; challengers NO ENGINE, WAITING SINCE
  2021). Fact-check: `claims.csv` 78 rows, gate passes. Narration v2 approved (`narration.md`), independent reviews
  `review_plan_v1.md`, `review_narration_v1.md`.
- **Audio approved and locked (owner, 2026-11-17):** the owner recorded the two blocks (`vo_blocks.md`) in the
  ElevenLabs app (the API account had 7,078 characters left until 3 Dec). Joined with `vo_rejoin.py` (gap 1.25 s at
  the factory chapter), 627.0 s, −16.6 LUFS. `vo_take_check.py` OK. `vo_lock.py --outro 20`: `vo/timing.json`,
  `vo/captions.en.srt`, `vo/lock.json` (SHA-256 6bab398b…). Drive `English/arjun-tank/vo/`.
- Chapters: 00:00 · 00:47 · 02:05 · 03:21 · 04:38 · 06:04 · 07:49 · 09:20 (`vo/chapters.tsv`).

## Footage r1 (2026-11-18)
- Searched with the channel's API (yt_search ×24, sheets in gitignored `assets/yt_search*`). Requests out:
  `footage_requests.md` (21 clips by Termux; Cowork: PIB Mysuru engine photos, PIB handover photos, DATRAN test
  vehicle, Rolls-Royce/MTU press photos, Pexels showroom/Swift/dunes/empty hall).
- From the cloud, in Drive `English/arjun-tank/footage/cloud/`: PIB order photos ×4 (PIB answers from the cloud
  now), CAG 35/2014 and 36/2016, AVNL annual report, Pixabay ×4. `media_manifest.csv` started (12 rows).
- Note: a competitor, DefenseVerse Intel, posted "52 Years, Zero Deliveries" (uakIVVgFcRM, 4 Nov 2026, 6 min): our
  edge (the engine shown, the factory's side, the two ways) still holds; watch its comments for objections.

## Footage vetted, Blender started (2026-11-18, later)
- Owner's batch landed: 19 of 21 clips (14 Mysuru coverage and 18 K2 failed; 14 not needed) and all Cowork items.
  Every clip stripped (`assets/strips/`); verdicts and clean spans in `footage_edl.md`; `media_manifest.csv` 46 rows.
  Key: PMO handover 74–84 s / 128–140 s (the real Mk1A, the first frame); Mk1A on a Chennai street; the Army's
  Battle Axe Division in the desert; HVF Avadi film (crop the bottom 24%); PIB Mysuru control room (no real photo
  of the engine itself exists: ours, labelled); RRPS press photos; Pexels Indian showroom/Swift/dunes.
- Still needed (r2): one K2 firing clip.
- `scripts/blender/arjun_hero.py`: the Mk1A from the PIB references (hull, skirts, 7 road wheels, tracks, plough,
  wedge turret, bustle basket, sleeved gun, RCWS, three-tone camo with AO grime and dust), the empty bay (mounts,
  final-drive flanges, pipe ends, ribs, cable trays, coolant lines), bay light linked to the hull only (no spill on
  the sand). Shots: `bayopen` (0–899: side → rear three-quarter → the covers lift → down into the glowing room),
  `thumb`. 1080p48 ≈ 2.8 min/frame on 4 threads. **bayopen rendering on GitHub** (6 shards, step 2) from this
  branch; download the artifacts, check, put in Drive `English/arjun-tank/renders/blender/`.
- Next Blender shots: the powerpack (MB 838-style V10 + Renk gearbox + radiators as one block, lifted by a crane;
  refs `assets/commons/mb838_*`), the bay through time (built / 2013 stopped / waiting), DATRAN on the Mysuru test
  bed, the landing crane stopping a hand's width above the mounts.

## Next
1. Footage: r2 (one K2 clip) with the word map. Original list: the Mk1A handover (Chennai, 14 Feb 2021; DD/PIB), HVF Avadi factory, Arjun firing in
   Rajasthan (Army/ADGPI), the Mysuru test-firing photos (PIB 20 Mar 2024), Zorawar firing (MoD Dec 2024), Altay and
   K2 (short credited excerpts), MTU Friedrichshafen (Rolls-Royce media), a 2021 car showroom; one Termux line, one
   Cowork request; `media_manifest.csv`.
2. Blender heroes (plan §8): the Arjun Mk1A in the Thar with the empty bay (also the thumbnail base), the powerpack
   lifted by a crane, the bay through time, DATRAN on a test stand. Design from real reference photos first.
3. Word map, Remotion build, renders (≤ 6 runners), music and sound, 720p cut, reviews, owner approval, 4K.
4. Fresh-facts gate within 24 h of upload: C09/C10 (none delivered), C17 (Rolls-Royce offer), C30 (next steps).

