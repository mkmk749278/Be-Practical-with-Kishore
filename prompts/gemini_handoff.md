# Gemini handoff request templates (Be Practical with Kishore)

`scripts/gemini_handoff.sh new <slug> <task>` copies one section below into `projects/<slug>/handoff/to_gemini.md`
under its front matter. Fill every `<fill: …>` line (push refuses a file that still has one), cut what does not
apply, add what this film needs. Gemini's answer is a list of leads: we check each point (PLAYBOOK §13.3).

## task: research
## Files in Drive to inspect
- Brief: <fill: Drive link to projects/<slug>/brief.md copy in Creator/English/<slug>/repo/>

## Specific checks requested
1. Run Deep Research (really run it; open every page you cite) on: <fill: the topic in one line>.
2. What everyone says: the 5 strongest YouTube films on this topic (views, length, the angle, what their top
   comments ask or complain about) and the common news line.
3. What the primary record says (government, PIB, CAG, Parliament answers, ministry reports, papers, company
   filings), each point with its URL and the exact sentence.
4. Gaps: what no film explains well, and the objections viewers raise that nobody answers.
5. Real Indian people at work, named towns and states, dated moments we could open on (story bank).
6. Search words viewers type, in English.
Do not write a script or a title.

## task: fact-check
## Files in Drive to inspect
- Narration: <fill: Drive link to narration.md>
- Claims file: <fill: Drive link to claims.csv>

## Specific checks requested
1. For every row of claims.csv: open the source URL. Is the quote really on the page? Does it support the narration
   line exactly (number, unit, date, name, tense)? Answer per row: OK / WRONG / UNSUPPORTED / SOURCE DEAD, with the
   correct figure and a better primary source where you find one.
2. Any factual line in the narration that has no claims.csv row.
3. Any absolute ("first", "only", "never", "zero") the record does not support.

## task: fresh-facts
## Files in Drive to inspect
- Claims file: <fill: Drive link to claims.csv>
- Package: <fill: Drive link to youtube/metadata.json>

## Specific checks requested
1. News of the last 30 days on <fill: topic>: anything that changes or dates a line of the film or its title?
2. Every "now", "today", "currently", "latest" row: still true today? Give the page and its date.

## task: narration-review
## Files in Drive to inspect
- Narration: <fill: Drive link to narration.md>
- Locked promise (title + thumbnail concept): <fill: one line>

## Specific checks requested
Read it as five viewers: a retired engineer of 68 on the family TV, a 50-year-old NRI in the Gulf, a 45-year-old
government officer, a 30-year-old engineering graduate, and a 60-year-old who watches with English subtitles.
1. Does sentence 1 keep the thumbnail's promise? Paradox by 0:25, open loop by 0:45?
2. Where would each viewer stop watching or check the phone? Quote the line.
3. Every line over 25 words, every jargon word, Hindi tag, hype word, "Welcome" or "In this video".
4. Is the objection ledger answered? Is there a saying to take home and a date to watch?
5. Scores 1–10 per viewer: would you watch to the end, would you subscribe.

## task: audio-audit
## Files in Drive to inspect
- Takes (in order): <fill: Drive links to the enhanced takes>
- Script read: <fill: Drive link to vo.txt>

## Specific checks requested
Listen to every file in full against vo.txt (voice: Akash, warm Indian English, an elder brother over coffee).
1. Wrong, skipped, repeated or added words.
2. Every number, date and unit read as written; acronyms as written (D-R-D-O letter by letter, Isro as a word).
3. Indian names and places: any mispronunciation, with how it sounded.
4. Delivery: uptalk, vocal fry, robotic or glitchy spots, clicks, loudness or room changes, rushed numbers.
5. Re-take list (exact sentences, in order of importance) and a keep list (5 best moments).

## task: cut-audit
## Files in Drive to inspect
- 720p review cut: <fill: Drive link>
- Narration: <fill: Drive link to narration.md>

## Specific checks requested
Watch it in full as the viewer on a family TV, then as a phone viewer.
1. Any still over 1.5 s, hold over 5 s, a slide-deck look (cards, bullets, text over 15% of frame), or empty canvas.
2. Every name, number, place and verb: does its picture land on its word? Drift over 100 ms between voice and
   picture?
3. Text too small to read on a phone or at 480p; maps of India without the official boundary.
4. Music too loud under the voice, sudden sound changes, dead silence.
5. The first 60 seconds: would you keep watching? Where in the film would you leave?
6. Return a fix list as a Claude Code spec: timestamp, what is wrong, the exact change.

## task: analytics-audit
## Files in Drive to inspect
- Studio export or screenshots: <fill: Drive link>

## Specific checks requested
1. Read impressions, CTR, average view duration, retention curve dips, traffic sources, TV vs phone, returning vs
   new, subscribers per film.
2. Where viewers leave (timestamps) and why, from the film itself.
3. Three changes for the next film, most valuable first.

## task: second-opinion
## Files in Drive to inspect
- <fill: Drive links>

## Specific checks requested
1. <fill: the exact question>

## How to answer (every task)
Save the answer as `from_gemini.md` (a file or a Google Doc named from_gemini) at the `return_path` above. If you
cannot write to Drive, email the whole answer instead, subject `[GEMINI-RESULT] <repo> <slug> <task_type>`.
Start with this front matter, then the sections:
```
---
repo: <repo>
slug: <slug>
task_type: <task_type>
completed_ist: YYYY-MM-DD HH:MM IST
verdict: APPROVED | FIXES_REQUIRED | DO_NOT_PROCEED
---
```
1. Verdict in one sentence. 2. Findings, most serious first, each with a timestamp (file, mm:ss) or line, what you
saw or heard, why it matters to the viewer, and the exact fix. 3. What is good and must be kept. 4. Anything you
could not open or check (say so; never guess). Every fact you report carries the URL of the page you opened.
