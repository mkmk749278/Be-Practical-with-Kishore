# Gemini Deep Research prompt, v1 (owner, 2026-11-23; PLAYBOOK §4)

The owner runs this in Gemini Deep Research on the phone and pastes the result (or its PDF) into the session. It is a
**wide, fresh sweep for leads**; the session then checks every item against a primary source, and only what holds up
becomes a `claims.csv` row. Gemini's text is never quoted in a film as fact. Replace the `{…}` fields; the session
fills them in and gives the owner the finished prompt as a click-to-copy block.

- `{TOPIC}`: the film in one line (e.g. "India's indigenous 700 MW pressurised heavy water reactors").
- `{MACHINE}`: the hard part under stress (e.g. "the Zr-2.5%Nb pressure tubes / coolant channels").
- `{SINCE}`: the date of our last research pass (day-first, e.g. 23 November 2026).
- `{GAPS}`: what our research still lacks, one per line (from `research/landscape.md` "Still to do").

---

Research this topic for a long English documentary for Indian viewers (mostly men over 45, India and the diaspora):
**{TOPIC}**. The heart of the film is one piece of hard engineering: **{MACHINE}**.

Rules for your answer:
- Prefer primary sources: government and regulator releases (PIB, the ministry, the regulator), parliament answers,
  audit (CAG) reports, the operator's own documents, technical papers, court records, company filings, and dated
  reports by named journalists. Wikipedia, blogs and YouTube are leads only: say so when you use them.
- For every fact give: the fact, the **exact sentence from the source in quotation marks**, the source name, the
  **direct URL**, and the source's date. If you cannot find the exact sentence, write "NO QUOTE FOUND" rather than
  paraphrasing.
- Never fill a gap with a guess. If sources disagree, give each version with its source. Mark anything you are unsure
  of as UNVERIFIED.
- Numbers with their units and the date they were true. Dates day-first.
- Indian place names with town and state.

Give me these sections, as tables where possible:
1. **New since {SINCE}:** news, official statements, orders, test results, delays or milestones, each dated.
2. **How the machine works and fails:** the physics and the numbers (temperature, pressure, size, weight, lifetime),
   and every known failure, incident or near-miss in India and abroad, with dates.
3. **Moments:** dated scenes (the day, the place, who was there, what happened, in what order), from the history to
   today.
4. **People:** named Indian engineers, scientists, workers, officials, with their job, what they did and anything they
   said on record (exact quote and source).
5. **The hard truths:** delays, cost overruns, failures, dependence on foreign suppliers, and the official reasons
   given, each with a source.
6. **What India did right:** firsts, records, things India solved alone, with sources (attribute any claim an
   organisation makes about itself).
7. **What critics and sceptical viewers say:** the strongest objections, with who makes them and the evidence on each
   side.
8. **Numbers an ordinary Indian can picture:** comparisons already made by credible sources (e.g. "as long as a
   football field"), with the source.
9. **Pictures that exist:** official photos and videos, archive footage, documents, with their URLs and any licence
   shown.
10. **Our open questions** (answer each, or say clearly that you found nothing):
{GAPS}

End with a list of every URL you used. Do not write an essay or a script, only the sections above.
