# Check of Gemini's second opinion (rounds 1–2, 26 NOV 2026)

Gemini's answers are leads (PLAYBOOK §13.3). What we checked and what we did:

| Point | Status | Evidence / action |
|---|---|---|
| CC0 machinery recordings (Freesound) | CONFIRMED | Licence "Creative Commons 0" read on each Freesound page by us; HQ previews in `assets/sfx/`, logged in `media_manifest.csv`, wired in `sound/sfx.json` |
| BigSoundBank picks (barrier closure, metro, air conditioner, pressure cooker) | NOT CHECKED | The site refused automated access; replaced with Freesound CC0 picks (trolley, pipe hits, steam valve) |
| Pressure cooker: CC0 recordings are Western steam cookers, not the Indian whistle | CONFIRMED (Gemini's own caveat) | Kept the stand-in whistle; asked the owner for a 3-second recording of a home cooker |
| The Exhibit too bright for the cold open; The Verdict is a trap beat | PARTLY | Taken on Gemini's listening (we cannot listen); The Verdict's catalogue text says the opposite, so the catalogue needs a fix |
| Track offsets (Mechanism 1:15, Counter-offensive splice 0:50→1:58, Made in India 1:03, Family's Story 1:13, Boardroom 0:37) | PARTLY | Used as given; slots anchored to our sentence times in `sound/score.json` |
| Film times and quoted lines in its map | NOT CONFIRMED | Several quotes are not in our narration (e.g. "Imagine a hairline crack in your pressure cooker", "Rs 4,000 Cr vs Rs 300 Cr") and its film times drift by up to 10 s; ignored, our timing.json rules |
| The block join at 4:21 is clean | CONFIRMED by its listening | Matches our own check on 25 NOV (1.0 s room-tone gap) |
