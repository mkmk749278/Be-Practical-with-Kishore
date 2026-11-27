## repo: Be-Practical-with-Kishore slug: phwr-700 task\_type: cut-audit completed\_ist: 2026-11-27 09:58 IST verdict: FIXES\_REQUIRED

# PHWR-700 Review Cut r3 Audit: Visuals APPROVED, Audio/Music/SFX Remix Required

## 1\. Verdict

Visuals in r3 are APPROVED and locked (do not re-render visuals). Run an audio-only remix (mix\_r4.wav) and stream-copy mux onto phwr\_review\_r3\_720p.mp4 to fix 10 music and SFX issues before the 4K Modal render.

## 2\. Files Inspected

- [phwr\_r3\_proxy\_360p.mp4](https://drive.google.com/file/d/1vwnuyJc298trhEP-Jtgzv8chj4iJCeQs/view)  
- [phwr\_review\_r3\_720p.mp4](https://drive.google.com/open?id=16aJro5KYVRBKQUaDx5hw9aLj8Qb4w01l)  
- [gemini\_cut-audit\_check.md](https://drive.google.com/file/d/1cQntlMqtWEUlXYuxr4WGFQnzU8RVFcu3/view)  
- [narration.md](https://drive.google.com/file/d/1xNvNtpAcp8Sj_O-gOKhLGKKZUTSvJUjQ/view)

## 3\. Music & SFX Fixes for mix\_r4.wav (10 Edits)

- **01:55.0 to 02:21.5 (Music emotional mismatch)**: Move pr04\_hopeful.mp3 entry from 01:55.0 to 02:21.5 (on "Indian engineers finished it on their own"). Use fx03\_boardroom.mp3 (from 00:37 at \-26 dB) across 01:55.0 to 02:21.5 over Pokhran and Canada's walk-out.  
- **09:54.0 to 09:59.0 (Early outro entry)**: Extend pr10\_human.mp3 through 09:58.5 and enter pr11\_outro.mp3 (00:00) at 09:59.0 on "Subscribe, so you are there with me".  
- **04:22 to 05:11, 07:05 to 07:45, 08:45 to 09:04 (Music level trims)**: Trim pr05\_counter by \-2 dB (04:22 to 05:11), fx03\_boardroom by \-2.5 dB (07:05 to 07:45), and pr04\_hopeful by \-3 dB (08:45 to 09:04); add a 2.0 s crossfade at 05:54 to 05:56.  
- **02:06.0, 03:59.5, 04:18.5, 05:26.0 (Misplaced heavy vault-door slams)**: Replace 02:06.0 (-9.7 dB) with a crisp paper/folder stamp at \-16 dB; replace 03:59.5 (-9.3 dB) with a soft control-room relay click at \-19 dB; remove 04:18.5 (-14.7 dB over "doctor") completely; remove 05:26.0 (-15.7 dB over quiet control room) completely.  
- **05:17.2 to 05:22.8 (Subway-like rail carriage roar)**: Drop 05:17.2 to 05:22.5 rail roar by \-6.5 dB (to \-26 dB) with a 1.5 kHz low-pass filter, and trim the 05:22.8 vault lock from \-12.0 dB to \-16.0 dB.  
- **01:30.2 to 01:31.0 (Over-loud 1 kg weight drop)**: Trim from \-10.3 dB to \-18.3 dB.  
- **06:53.5 to 06:54.5 (Heavy shutdown-rod crash)**: Trim from \-11.5 dB to \-17.0 dB with a tight 0.8 s tail.  
- **02:45.5 to 02:49.0 (Harsh fuelling-machine roar)**: Low-pass at 1.2 kHz, add 0.6 s fade-in/out ramps, and trim to \-27 dB.  
- **01:54.5 (Pokhran hard-cut thud)**: Trim \-3 dB (from \-8.5 dB to \-11.5 dB).  
- **Glassy UI reveal chimes (00:13.5, 01:18.2, 01:39.0, 01:48.5, 03:09.2, 03:31.5, 05:30.0, 05:37.8, 07:08.8, 07:50.5, 08:30.0, 09:55.8)**: Duck all chimes by \-6 dB (ceiling \-22 dB), and replace 03:09.2 (-13.3 dB) with a dry low mechanical warning thump (-18 dB).

## 4\. Fast Audio-Only Mux

- **Check 6 (Real machinery recordings: do they feel real and sit under the voice?):**  
- Run python3 scripts/score\_mix.py \--slug phwr-700 \--out mix/mix\_r4.wav (-14.0 LUFS, \-1.5 to \-2.5 dBTP).  
- Mux without re-encoding video: ffmpeg \-y \-i renders/phwr\_review\_r3\_720p.mp4 \-i mix/mix\_r4.wav \-map 0:v:0 \-map 1:a:0 \-c:v copy \-c:a aac \-b:a 192k renders/phwr\_review\_r4\_720p.mp4.