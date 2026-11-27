#!/usr/bin/env python3
"""The YouTube SRT (PLAYBOOK §15.3): vo/captions.en.srt (voice spellings, locked timing) with real spellings and
numerals, wrapped to 42 characters, at most two lines (a longer cue splits in two at a comma, timed by length)."""
R = [("nineteen seventy four", "1974"), ("nineteen eighty three", "1983"), ("half built", "half-built"), ("nineteen sixties", "1960s"),
     ("nineteen ninety five, ninety six or ninety seven", "1995, 1996 or 1997"), ("nineteen ninety eight", "1998"),
     ("nineteen ninety six", "1996"), ("nineteen ninety five", "1995"), ("nineteen eighty one", "1981"),
     ("twenty twenty seven to twenty thirty five", "2027 to 2035"), ("twenty twenty five", "2025"),
     ("twenty twenty six", "2026"), ("twenty twenty", "2020"), ("twenty sixteen", "2016"), ("twenty ten", "2010"),
     ("nine hundred and sixty two", "962"), ("three hundred and ninety two", "392"), ("three hundred and six", "306"),
     ("Three hundred and six", "306"), ("three hundred and ten degrees", "310 degrees"),
     ("seven hundred megawatt", "700 MW"), ("one thousand one hundred crore rupees", "₹1,100 crore"),
     ("two hundred and fifty crore", "₹250 crore"), ("a thousand crore", "₹1,000 crore"),
     ("seventy thousand crore rupees", "₹70,000 crore"), ("twenty two million pounds", "22 million pounds"),
     ("ten thousand tonnes", "10,000 tonnes"), ("four thousand seven hundred", "4,700"),
     ("sixty four kilometres", "64 km"), ("four millimetres", "4 mm"),
     ("one kilo on every square centimetre", "1 kg on every square centimetre"), ("ten to twelve years", "10 to 12 years"),
     ("eleventh of March", "11 March"), ("unit two", "unit 2"), ("unit eight", "unit 8"), ("Unit seven", "Unit 7"),
     ("N-P-C-I-L", "NPCIL"), ("T-V", "TV"), ("Cyrus", "CIRUS"), ("twenty years later", "20 years later"),
     ("ten years later", "10 years later"), ("ten more", "10 more"), ("a hundred times", "100 times"),
     ("every hundred units", "every 100 units"), ("seven in the evening", "7 in the evening"),
     ("nine in the morning", "9 in the morning")]


def ts(s):
    h, m, r = s.split(":"); s_, ms = r.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s_) + int(ms) / 1000


def fmt(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(txt, w=42):
    lines, cur = [], ""
    for word in txt.split():
        if cur and len(cur) + 1 + len(word) > w:
            lines.append(cur); cur = word
        else:
            cur = (cur + " " + word).strip()
    return lines + [cur]


def split(t0, t1, txt):
    if len(wrap(txt)) <= 2:
        return [(t0, t1, "\n".join(wrap(txt)))]
    words = txt.split(); half = len(words) // 2
    commas = [i + 1 for i, w in enumerate(words[:-1]) if w.endswith(",")]
    k = min(commas, key=lambda i: abs(i - half)) if commas and min(abs(i - half) for i in commas) <= half // 2 + 1 else half
    p1, p2 = " ".join(words[:k]), " ".join(words[k:])
    tm = t0 + (t1 - t0) * len(p1) / (len(p1) + len(p2))
    return split(t0, tm, p1) + split(tm, t1, p2)


out = open("vo/captions.en.srt", encoding="utf-8").read()
for a, b in R:
    if a not in out:
        print("unused:", a)
    out = out.replace(a, b)
cues = []
for b in out.strip().split("\n\n"):
    l = b.split("\n"); a, z = l[1].split(" --> ")
    cues += split(ts(a), ts(z), " ".join(l[2:]))
open("youtube/phwr-700.en.srt", "w", encoding="utf-8").write(
    "\n\n".join(f"{i + 1}\n{fmt(a)} --> {fmt(b)}\n{t}" for i, (a, b, t) in enumerate(cues)) + "\n")
print(len(cues), "cues")
