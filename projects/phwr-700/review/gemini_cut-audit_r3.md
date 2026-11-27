repo: Be-Practical-with-Kishore
slug: phwr-700
task_type: cut-audit
completed_ist: 2026-11-27 10:15 IST
verdict: FIXES_REQUIRED

# PHWR-700 Review Cut r3 Audit: Visuals 100% LOCKED, Audio/Music/SFX Remix Required (mix.wav Only)

## 1. Verdict in One Sentence

**Visuals are 100% APPROVED and LOCKED in r3 (do not re-render a single video frame), but the audio mix (mix/mix.wav) requires an immediate audio-only remix pass (FIXES_REQUIRED)** because the music bed is buried too deep (-32 to -35 dB median, making it feel thin and disconnected) while raw sound effects spike 14 to 24 dB louder than the music (-8.5 to -19 dB), including a 5.6-second screeching subway-train recording (05:17.1 to 05:22.7) under the tube-pulling schematic and a -10.3 dB steel-gate crash on the 1-kilo kitchen weight diagram (01:30.5).

## 2. Files Inspected in Full

- **360p Review Cut r3 (watched and auditioned in full, plus voice-subtracted background stem bg_r3_only analyzed across all 623.47 s)**: [phwr_r3_proxy_360p.mp4](https://drive.google.com/file/d/1vwnuyJc298trhEP-Jtgzv8chj4iJCeQs/view)
- **720p Full-Quality Review Cut r3**: [phwr_review_r3_720p.mp4](https://drive.google.com/file/d/16aJro5KYVRBKQUaDx5hw9aLj8Qb4w01l/view?usp=drivesdk)
- **Round 2 Check Log**: [gemini_cut-audit_check.md](https://drive.google.com/file/d/1cQntlMqtWEUlXYuxr4WGFQnzU8RVFcu3/view)
- **Approved Narration Script**: [narration.md](https://drive.google.com/file/d/1xNvNtpAcp8Sj_O-gOKhLGKKZUTSvJUjQ/view)
- **Handoff Prompt**: [to_gemini.md](https://drive.google.com/file/d/1fGYMRJG2_kvQ9b8OTK68kyY3qhqyZ3cY/view?usp=drivesdk)

## 3. Visual Audit of r3 — ALL VISUAL FIXES LANDED AND LOCKED

Every visual fix from r2 landed cleanly in r3 and is approved by the owner:

- **0:02.7**: Half-built 1970s photo now has a clean dark-blue blueprint drafting grid and "HALF BUILT" header.
- **0:04.2, 7:21, 9:53 to 10:00**: Full-India maps now sit at 0.84 to 0.88 scale with 100% of Ladakh and Kanyakumari inside the frame.
- **1:08 to 1:14**: Forged vessel with bolted flange and nozzles (ONE THICK STEEL WALL) shrinks into a row of 7 pots (MOST REACTORS IN THE WORLD).
- **1:28 & 1:36**: The 1 KG weight lowers on a cord from frame 1, and the 100x stack climbs on "pushed".
- **2:18**: Dimmed half-built 306-port calandria face sits behind YOU ASK KISHORE / WHAT HAPPENED TO IT?.
- **2:33**: 962 DAYS counter sits on a high-contrast dark backing pill (kit Count).
- **2:45**: Re-cut to the operator at the fuelling machine (A FUELLING MACHINE · 700 MW).
- **2:55**: YEAR 1 to YEAR 10 cursor walks the ruler from frame 1 before 10-12 YEARS lands.
- **5:07**: Dashed ghost tool with ? sits from frame 1 and inks on "Indian engineers designed them".
- **5:38, 5:51, 6:03**: BUSINESS INDIA · AS REPORTED slip and climbing rupee stack (₹250 CRORE), three swaying blank calendar pages filling on each year (1995, 1996, 1997), and RAWATBHATA-2: 1ST IN INDIA turning to 2ND IN THE WORLD next to 1ST CANADA all move from frame 1.
- **8:45, 9:00, 9:04**: All 100 dots sweep warm on "every hundred units" before 3 stay lit; '10 to '20 labels are 40 px white; 10 dashed reactor domes stand from frame 1 and turn solid on "ten".

**Visual Gate Instruction**: Freeze the video stream (phwr_review_r3_720p.mp4 video track). Do not re-render Remotion frames; after fixing mix/mix.wav, mux the new audio directly with ffmpeg -i phwr_review_r3_720p.mp4 -i mix/mix.wav -c:v copy -map 0:v:0 -map 1:a:0.

## 4. Detailed Audio, Music & Sound-Effects Audit (Why the Sound Feels Off in r3)

We subtracted the dry voiceover (phwr_vo_full.wav) from phwr_r3_proxy_360p.mp4 to listen to the isolated music-and-SFX stem (bg_r3_only) and measured every 100 ms window. Here is exactly what is wrong with the music and sound effects:

### A. Why the Music Bed Feels Thin, Disconnected, and Uneven

1. **Music Median Level Is Too Quiet (-32 dB to -35.5 dB RMS), While Uncompressed Swells Poke Out (-20 to -23 dB)**:
   - Across 0:00 to 10:05, the steady music bed median sits at -32.0 to -35.5 dB (18 to 21 dB quieter than the -14 LUFS voice). On phone speakers and TV speakers, the quiet passages of fx02_mechanism (0:45 to 1:15), fx04_cascade (3:15 to 3:50), pr05_counter (4:22 to 5:10), pr06_capability (5:55 to 6:30), and pr04_hopeful (7:45 to 8:40) almost disappear into silence, making the voice feel unsupported — and then sudden drum/string swells (00:44 at -19.4 dB, 01:18 at -17.4 dB, 04:31 at -18.9 dB, 04:45 at -21.6 dB, 06:22 at -19.0 dB, 08:30 at -18.2 dB) jump out by +10 to +14 dB over the bed.
   - **Exact Fix on the Music Bus**: Apply a gentle 3:1 compressor / leveling limiter on each music track (threshold: -24 dB, ratio: 3:1, attack: 15 ms, release: 250 ms, high-pass: 90 Hz, 2.5 dB dip at 1.8 kHz for vocal pocket) and set the compressed music bus to a steady **-26.0 dB integrated level under voice** (with swells capped at -23.5 dB). That way the music is always warmly audible at -26 dB without ever disappearing to -35 dB or jumping up to -18 dB.
   - **Abrupt Music Cut-Offs and Unsmoothed Section Joins (04:15, 05:11, 06:31, 09:54)**:
   - At 05:11 (the internal splice inside pr05_counter.mp3 from 00:50 to 01:58), the music drops and is immediately buried under 8 seconds of loud machinery noise (05:15 to 05:23). Use a smooth 2.0 s equal-power crossfade across every music edit and section boundary (0:39, 1:55, 2:26, 3:02, 5:11, 5:55, 6:37, 7:45, 9:29, 9:54), and use a 2.5 s cosine fade-out into the two dry silence windows (04:13.0 to 04:15.5 and 06:29.0 to 06:31.2).

### B. Seven Sound Effects That Sound Fake, Harsh, Misplaced, or Way Too Loud

2. **05:15.5 – 05:23.2 (CRITICAL — 7.7 Seconds of Screeching Subway Train + Angle Grinder + Vault Crash at -12.0 to -19.1 dB)**
   - **What you hear**: At 05:15.5 to 05:17.1 ("A tool reaches in and cuts it free"), the angle grinder buzzes at -21.5 dB, and then from **05:17.1 to 05:22.7** ("The tube is drawn, slowly, into a heavy steel flask. The flask carries it away to a vault"), **metro-stopping-and-starting-1-s3039 (a full-bandwidth outdoor recording of a subway train screeching and rumbling on steel tracks!)** blasts continuously at **-19.1 dB for 5.6 seconds**, ending with a massive -12.0 dB metal door crash at 05:22.7 and another -15.7 dB metallic bang at 05:26.0!
   - **Why it feels bad**: It sounds like a loud subway station and construction site for 8 straight seconds on top of a clean 2D schematic, fighting the narrator's voice.
   - **Exact Fix**:
     - **DELETE metro-stopping-and-starting-1-s3039 (05:17.1 to 05:22.7) and the 05:26.0 hit completely.** A nuclear pressure tube being drawn slowly into a flask on a 2D diagram does not sound like a subway train.
     - Keep only a short 1.0 s muffled metallic cut at 05:15.5 to 05:16.5 (low-passed at 1.6 kHz, peak -24.0 dB), followed by silence/music bed while the tube slides into the flask (05:16.5 to 05:22.5), and a single soft, low-passed latch click (low-pass 700 Hz, peak -21.0 dB, 0.4 s duration) at 05:22.6 when the flask reaches the vault.
3. **01:30.2 – 01:31.2 (-10.3 dB!) & 03:59.5 – 04:00.2 (-9.3 dB!) (CRITICAL — Massive 2-Ton Industrial Steel-Gate Crash Used on 2D Diagrams)**
   - **What you hear**:
     - At 01:30.5, when the small 1 KG weight touches the 1 CM2 dashed square on the word "one kilo", grinding-metal-barrier-closure (a heavy industrial steel barrier crash) explodes at **-10.3 dB** (+6.2 dB louder than the voice and +19.3 dB louder than the music bed!).
     - At 03:59.5 (in the pause after "...brought the reactor safely to a stop" as the screen cuts to the 2D 306-circle diagram), that exact same **-9.3 dB steel barrier crash** fires out of nowhere when nothing on screen is colliding!
   - **Why it feels bad**: Using a -9 to -10 dB industrial steel-gate crash on a 1-kg kitchen weight diagram and a 2D circle cut feels jarring and artificial.
   - **Exact Fix**:
     - **DELETE the 03:59.5 steel-barrier crash completely.**
     - At 01:30.5 (when the 1 KG weight lands), either remove the SFX or replace it with a tiny, dull low-end tap (low-pass 400 Hz, 0.15 s, peak **-24.0 dB**). Keep grinding-metal-barrier-closure ONLY for the 3D Blender yellow steel flask locking onto the reactor face at 00:26.2 (and trim 00:26.2 from -11.8 dB down to **-18.0 dB**).
4. **02:45.2 – 02:49.5 (-22.4 dB Broadband Plant-Noise Wall Switching On and Off Abruptly)**
   - **What you hear**: Across 02:45.2 to 02:49.5 ("You can feed fresh fuel in while it runs. What wears out is the tubes"), a broadband industrial noise recording (Coal Power Plant Int, full of 1 to 6 kHz white-noise hiss) jumps the background floor from -33.1 dB up to -22.4 dB for 4.3 seconds and then cuts off dead at 02:49.5.
     - **Why it feels bad**: Because the surrounding archival shots have no ambient room hiss, a 4.3-second block of broadband plant noise sounds like a noisy air-conditioner or audio static turning on and off under the voice.
   - **Exact Fix**: **DELETE the 4.3-second 02:45.2 to 02:49.5 ambient plant-hum insert completely** (let fx02_mechanism.mp3 carry that 4-second B-roll cut cleanly, just like the rest of Chapter 2a).
5. **03:09.2 – 03:10.0 (-13.3 dB), 03:54.7 – 03:56.2 (-17.9 dB steam hiss), and 06:53.7 – 06:54.7 (-11.5 dB metal door slam) (Harsh Diagram SFX Overpowering the Voice)**
   - **What you hear**:
     - At 03:09.2 ("one tube broke at full power" on the 2D circle diagram), a loud -13.3 dB metallic bang/alarm (+18.2 dB over the bed) steps right on "broke at full power".
     - At 03:54.7 to 03:56.2 ("...until the tube split. The operators, I should tell you..."), the 2.3-second high-frequency steam blowdown hiss sounds like bright white static colliding with the narrator's sibilants ("s", "t", "sh").
     - At 06:53.7 to 06:54.7 ("The reactor shut itself down" on the 2D 4-rod diagram), a reverberant metal door slam (-11.5 dB, +18.7 dB over the bed) crashes right over "shut itself down".
   - **Exact Fix**:
     - **At 03:09.2**: Trim by -9 dB (from -13.3 dB to **-22.5 dB**) so the red dot pulse is subtle.
     - **At 03:54.7**: Shorten the tube-split cue to **0.9 s (03:54.7 to 03:55.6)**, low-pass filter it at **1.1 kHz** (removing all white-noise static hiss above 1.1 kHz), and trim to **-22.0 dB** so it ends before "The operators, I should tell you".
     - **At 06:53.7**: Trim the shutdown-rod drop by -9.5 dB (from -11.5 dB to **-21.0 dB**), low-pass at 800 Hz, and shorten to 0.6 s so it feels like a muffled internal rod drop, not a loud metal door slam.
6. **04:18.5 – 04:19.1 (-14.7 dB Metal Vault Slam Step-Masking the Word "doctor")**
   - **What you hear**: In r3, the second slam at 04:21.5 was removed, **but the first 1.6-second reverberant metal door slam at 04:18.5 (-14.7 dB) still fires directly on top of the word "doctor"** in "And no doctor would come. What would you have done?".
   - **Why it feels bad**: It steps on the key emotional word "doctor" right when the film should be dropping into sober silence.
   - **Exact Fix**: **DELETE the 04:18.5 metal door slam completely.** Fade fx04_cascade.mp3 out to silence by 04:15.5 and leave 04:15.5 to 04:22.2 ("So India had the same disease. And no doctor would come. What would you have done?" + the 1.0 s pause) 100% dry voiceover with zero SFX.
7. **01:25.8 – 01:26.6 (-18.0 dB Cooker Whistle) & 08:09.0 – 08:09.8 (-18.1 dB Dew Alarm Buzzer)**
   - **What you hear**:
     - At 01:25.8 (on "You know that whistle"), the 0.8-second slice from the pressure-cooker file is mostly broadband steam frying hiss (-18.0 dB) rather than a pure whistle tone, and it lands directly on top of the word "whistle".
     - At 08:09.0 (on "Here, the dew is the alarm"), the 0.8-second fire-alarm panel buzzer (-18.1 dB) has harsh high-frequency square-wave harmonics (2.5 to 6 kHz) that buzz over the word "alarm".
   - **Exact Fix**:
     - **At 01:26.0**: Band-pass filter the pressure-cooker whistle (1.2 kHz to 3.2 kHz) to remove the broadband frying hiss, trim to **-22.0 dB** (0.65 s duration), and place its peak at 01:26.15 in the brief breath right after "whistle".
     - **At 08:09.0**: Low-pass filter the alarm beep at **1.8 kHz** (rounding off the harsh square-wave buzz), shorten to **0.5 s (08:09.1 to 08:09.6)**, and trim to **-23.0 dB**.
8. **01:54.5 (-8.5 dB Pokhran Cut) & 02:06.0 (-9.7 dB 1974 Folder Slam) & 00:20.0 / 04:39.0 (-15.7 dB / -17.9 dB Rubber Stamps)**
   - **What you hear**: The rubber stamps at 00:20.0 (NOT PERMITTED, -15.7 dB) and 04:39.0 (-17.9 dB) sound crisp and authentic, as do the 02:33 counter ticks (-18.8 dB). However, the 01:54.5 Pokhran impact (-8.5 dB) and particularly the 02:06.0 CLOSED · 1974 folder slam (-9.7 dB) still jump +21 dB above the music bed.
   - **Exact Fix**: Keep the rubber stamps (00:20.0, 04:39.0) and 02:33 counter ticks exactly as they are; trim the 01:54.5 Pokhran hit by -4.5 dB (to **-13.0 dB**) and trim the 02:06.0 CLOSED · 1974 folder close by -7.5 dB (to **-17.2 dB**).

## 5. Execution-Ready Claude Code Spec (docs/phwr-700_audio_remix_r4_spec.md)

### Philosophy: Documentary Restraint ("Fewer, Softer, Warmer")

On Be-Practical-with-Kishore, sound effects must never turn a 2D explanatory diagram into a noisy cartoon or industrial construction site. Real machinery foley belongs only on physical hero moments, tucked **6 to 10 dB below the voice (-20 to -24 dB)** and low-passed so the 1 kHz to 4 kHz vocal presence band always belongs 100% to Kishore's voice.

### Step 1 — Delete These 5 Bad/Intrusive SFX Events From the Timeline

9. **DELETE 01:30.2 – 01:31.2** (-10.3 dB steel-barrier crash on the 1 KG ON 1 CM2 diagram).
10. **DELETE 02:45.2 – 02:49.5** (-22.4 dB broadband coal-plant noise burst on the fuelling-machine B-roll).
11. **DELETE 03:59.5 – 04:00.2** (-9.3 dB steel-barrier crash on the 2D 306-circle diagram cut).
12. **DELETE 04:18.5 – 04:19.2** (-14.7 dB vault-door slam on the word "doctor" in "And no doctor would come").
13. **DELETE 05:17.1 – 05:22.7 & 05:25.7 – 05:26.3** (-19.1 dB screeching metro-train rail recording s3039 and extra clunk during the Ch.3a tube-draw schematic).

### Step 2 — Soften & EQ the Remaining 8 Kept SFX Cues (Strict -18 to -24 dB Ceiling)

-

| Timestamp | Cue Description | Current r3 Peak | Required r4 Peak & EQ Filter |
| :---- | :---- | :---- | :---- |
| **00:20.0** | Red NOT PERMITTED rubber stamp | -15.7 dB | **-18.0 dB** (keep as-is, trim -2.3 dB) |
| **00:26.2** | 3D Yellow steel flask lock clunk | -11.8 dB | **-18.0 dB**, low-pass at 1.4 kHz (deep metallic thud, no high clatter) |
| **01:26.1** | Pressure-cooker whistle (0.65 s) | -18.0 dB | **-22.0 dB**, band-pass 1.2 kHz – 3.2 kHz (clean whistle tone, zero frying hiss) |
| **01:54.5** | Pokhran 1974 hard-cut thud | -8.5 dB | **-13.0 dB**, low-pass at 900 Hz |
| **02:06.0** | CLOSED · 1974 folder close | -9.7 dB | **-17.5 dB**, low-pass at 1.2 kHz |
| **02:33.0 – 02:35.0** | 962 DAYS counter ticks | -18.8 dB | **-19.5 dB** (already clean; keep as-is) |
| **03:09.2** | Pickering single red tube fault pulse | -13.3 dB | **-22.5 dB**, soft low-end pulse (0.3 s) |
| **03:54.7 – 03:55.6** | Pickering tube-split steam release (0.9 s) | -17.9 dB (2.3 s) | **-22.0 dB**, shorten to **0.9 s**, low-pass at **1.1 kHz** (ends before "The operators") |
| **04:39.0** | Ch.3 NOT PERMITTED rubber stamp | -17.9 dB | **-18.5 dB** (already clean; keep as-is) |
| **05:15.5 – 05:16.5** | Remote pipe cutter (1.0 s) + 05:22.6 vault latch (0.4 s) | -19.5 dB / -12.0 dB | Cutter: **-24.0 dB**, 1.0 s, low-pass 1.6 kHz; 05:22.6 vault latch: **-21.0 dB**, 0.4 s, low-pass 700 Hz |
| **06:53.7 – 06:54.3** | Kakrapar shutdown-rod drop (0.6 s) | -11.5 dB | **-21.0 dB**, 0.6 s, low-pass at 800 Hz |
| **08:09.1 – 08:09.6** | Dew-point alarm pulse (0.5 s) | -18.1 dB (0.8 s) | **-23.0 dB**, 0.5 s, low-pass at 1.8 kHz |

### Step 3 — Level & Warm Up the 9-Section Music Stem

14. Keep the exact Round 2 track list and start offsets currently in r3 (fx03_boardroom 0:00 -> fx02_mechanism 0:39 -> pr04_hopeful 1:55 -> fx02_mechanism 01:15 at 2:26 -> fx04_cascade 3:02 -> dry silence 4:15.5 to 4:22.0 -> pr05_counter 0:00 at 4:22 & 01:58 at 5:11 -> pr06_capability 01:03 at 5:55 -> dry silence 6:31.2 to 6:37.0 -> fx03_boardroom 00:37 at 6:37 -> pr04_hopeful 0:00 at 7:45 -> pr10_human 01:13 at 9:29 -> pr11_outro 0:00 at 9:54 to 10:23).
15. Run the music bus through a **3:1 leveling compressor** (threshold -24 dB, makeup +4.5 dB, high-pass 90 Hz, -2.5 dB bell dip at 1.8 kHz Q=1.2) so the quiet pads rise from -34 dB up to **-26.5 dB** while the loud drum/string swells are clamped at **-23.5 dB**.
16. Apply 2.0 s equal-power crossfades at every music transition so there are zero abrupt cuts.

### Step 4 — Fast Audio-Only Rebuild & Mux (Under 30 Seconds, Zero Video Re-Render)

-

```sh
# 1. Re-build mix/mix.wav with the Step 1-3 audio spec above and verify loudness:
python3 scripts/score_mix.py mix/mix.wav
# Target: Integrated -14.0 LUFS, True Peak <= -1.5 dBTP, max SFX peak under speech <= -18.0 dB (except 1:54.5 Pokhran at -13.0 dB)

# 2. Mux new mix/mix.wav directly into the locked r3 720p video and 360p proxy without re-encoding video:
ffmpeg -y -i renders/phwr_review_r3_720p.mp4 -i mix/mix.wav -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 renders/phwr_review_r4_720p.mp4
ffmpeg -y -i renders/phwr_r3_proxy_360p.mp4 -i mix/mix.wav -c:v copy -c:a aac -b:a 96k -map 0:v:0 -map 1:a:0 renders/phwr_r4_proxy_360p.mp4
```

  -
