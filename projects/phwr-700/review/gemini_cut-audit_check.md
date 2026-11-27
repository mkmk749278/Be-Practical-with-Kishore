# Gemini cut audit of review cut r2: our check (27 NOV 2026, about 8:30 AM IST)

Reply: `gemini_cut-audit.md` (completed 27 NOV, 12:52 AM IST; verdict FIXES_REQUIRED). Each lead was checked on frames
pulled from `renders/phwr_review_r2_720p.mp4` at its time, against the scene code, and against the mix itself
(levels in the voice's pauses: mix against `vo-render/phwr_vo_full.wav`). Gemini's times run up to about 1 s off ours.

| # | Lead | Our check | Fix in r3 |
|---|---|---|---|
| 1 | 2:45 "KAKRAPAR · FUELLING MACHINE" shows NPCIL's CMD B.C. Pathak talking | **CONFIRMED**, our worst error: `clips.tsv` had 415–418.8 s, a typo for 4:15, which landed in the CMD's interview | K05_fm re-cut to 261.75–264.20 s (an operator at the fuelling machine, one shot, checked on stills); tag now "A FUELLING MACHINE · 700 MW" (the featurette does not say which plant) |
| 2 | 0:02.7 the grey hatch over the top half of the 1970s photo reads as a broken image | **CONFIRMED** | The unbuilt half is a blueprint sheet: drafting grid, a pencil line sweeping across, "HALF BUILT" |
| 3 | 1:08–1:14 the steel pot holds 6.8 s with almost no motion | **CONFIRMED** | Bolted flange and nozzles (reads forged, not a jar); "one giant steel pot" calls out ONE THICK STEEL WALL; "Most reactors in the world" shrinks it into a row of seven pots |
| 4 | 1:28 the empty canvas before "1 KG ON 1 CM²" | **CONFIRMED** (2.3 s of an empty table) | The weight is lowered on a cord from the shot's first frame and lands on "one" |
| 5 | 1:36 the ×100 stack waits 2.3 s | **PARTLY** (the one-kilo weight is on screen) | The stack starts climbing on "pushed" |
| 6 | 2:18 the top of the "What happened to it?" frame is empty | **PARTLY** | The half-grey 306 face, dim, behind the question (it is "your half built reactor") |
| 7 | 2:33 "962 DAYS" unreadable over the white control-room wall at 480p | **CONFIRMED** ("DAYS" is thin) | Every counter now sits on a dark pill with a coloured rule (kit `Count`) |
| 8 | 2:55 the 0–30 year ruler empty for about 5 s | **CONFIRMED** (4.7 s) | A YEAR cursor walks the ruler from the first frame; the 10–12 shade lands on "ten". Gemini's "DESIGN LIFE: 30 YEARS" bar is not taken: no source in `claims.csv` |
| 9 | 3:40–3:55 a flat 15.5 s hold on the hydrogen channel | **NOT CONFIRMED**: the shot already pushes in from 1.7× to 2.3× and changes on every sentence (hydrogen, cold spot, blisters, crack, split) | none |
| 10 | 4:32 label the other countries round the owners' table | **NOT TAKEN**: membership facts are not in our sources | none |
| 11 | 5:02 the OPG clip's own small title is illegible | **PARTLY**: it is the source's text, not ours; we point at nothing in it | none in r3: the source's own label on a credited clip, 1.6 s on screen |
| 12 | 5:07 a blank white drawing sheet for 2.8 s | **CONFIRMED** | "Machines that did not exist yet": the tool stands as a dashed ghost with a "?" from the first frame; it inks on "Indian engineers designed them" |
| 13 | 5:38 empty dashed cost boxes for 7 s | **CONFIRMED** | A BUSINESS INDIA · AS REPORTED slip lands on "Business India"; the rupee stack starts climbing on "rupees" and reaches ₹250 crore on its words. Gemini's US$/C$ figures are **not taken** (owner's lock: rupees in crores) |
| 14 | 5:51 the blank canvas before 1995–97 | **CONFIRMED** (about 2 s) | The three calendar pages hang blank and sway from the first frame; each fills on its year |
| 15 | 6:03 "1ST CANADA / 2ND RAWATBHATA" waits on an empty grid | **CONFIRMED** (3.5 s) | The RAWATBHATA-2 plate stands from the first frame; "first such job in India" writes 1ST · IN INDIA; "second" turns it to 2ND · IN THE WORLD; Canada's 1ST lands beside it |
| 16 | 6:31–6:37 music under the TV-remote line | **NOT CONFIRMED**: the bed ends at 6:31.2; in the pauses of that line the mix is the voice's room tone alone (−35 to −50 dB) | none |
| 17 | 0:04 the badge touches Ladakh; 6:49 the Kakrapar map crops J&K and the south | **PARTLY**: at 0:04 the north tip met the frame's top; 6:49 is a zoom into Gujarat (a zoom, not a cut boundary). Our own find: the 9:59 lights map cut off Kanyakumari | All whole-India maps now sit at 0.84–0.88 scale, Ladakh to Kanyakumari inside the frame (stills checked at 0:04 and 9:59) |
| 18 | 8:45–8:52 a hundred grey dots still for 7 s | **CONFIRMED** | On "every hundred units" all hundred warm up in a sweep; on "three" ninety-seven fall back and three stay lit |
| 19 | 9:00 the '10–'20 tick labels small and grey | **CONFIRMED** (30 px, dim) | 40 px, ink white |
| 20 | 9:05 an empty line before the ten domes | **CONFIRMED** (about 3 s) | The ten domes stand as dashed outlines (approved, not built) and turn solid on "ten" |
| 21 | 1:28 the cooker whistle 2.5 s late and loud, over "Inside, the steam pushes…" | **CONFIRMED**: cued after the sentence at −8 dB, while the picture's whistle lifts on the word | On "whistle", −14 dB (the gap before S26 is now −26 dB, was −11) |
| 22 | 4:18 and 4:21 two metal hits over "What would you have done?" and its pause | **CONFIRMED**: one 5.2 s vault-door cue on "doctor" with a second hit at +3 s; the pause after S79 measured −17 dB | First slam only (1.6 s), −11 dB; the pause is now −45 dB, dry as planned |
| 23 | 5:15 the cutter sound carries people talking | **CONFIRMED by its envelope**: the trim (1.5–4.6 s) was the recording's quiet pre-roll, not the cut | 5.5–7.1 s of the cut itself, −18 dB |
| 24 | 8:09 the dew alarm 2.5 s, loud, over "went critical" | **CONFIRMED** | 0.8 s, −17 dB |
| 25 | Peaks at 1:54, 3:55, 6:54, 2:45 | **PARTLY**: 1:54 is the designed Pokhran hit; the 3:54 steam hiss did run 4 s over S73 | Pokhran −6→−8 dB; steam hiss 2.3 s at −13; rods −8→−11; fuelling hum −16→−19 |

Mix r3: −14.1 LUFS, −2.5 dBTP (`scripts/score_mix.py`), Drive `mix/mix.wav` (r2's kept as `mix/mix_r2.wav`).
