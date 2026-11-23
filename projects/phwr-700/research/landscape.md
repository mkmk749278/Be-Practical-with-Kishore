# 700 MW reactors · research landscape (first pass, 2026-11-23)

Sources are leads until they are rows in `claims.csv` with a verbatim quote. NPCIL, BARC and DAE documents are the
primary record for the design and history. Their self-praise ("record time", "shortest time", "export") goes in the
film only as attributed.

## 1. What everyone says
- **The big Indian nuclear films** (YouTube, gl=IN, 23 NOV; comments in `competitor_comments.json`):
  - **KK Create**, "Reality of India's nuclear power" (6.6M). It's not about reactors: it's about the families near
    the uranium mines of Jaduguda, Jharkhand. The comments are grief and anger. *For us:* a viewer who saw it will ask
    "and the people near the mines?" Answer it with dignity and attribution, or not at all. Never wave it away.
  - **Mohak Mangal**, "India Just Did What 99% of Countries Failed At" (1.7M, the April 2026 PFBR criticality).
    Most-liked comments: "Indian Scientists 🗿 Indian Politicians 🤡", "Respect to Dr. Homi Jehangir Bhabha", "Even if it
    had costed 16000 crore it would not pain a single Indian", a student who missed the BARC cut-off and won't give up.
    *Pride in the scientists, anger at the system.*
  - **Insights by Apoorv**, "Why India's Nuclear Program is Shaking the World" (1.2M, thorium). Comments are dominated
    by Kerala beach-sand mining fears and "Ambani and Adani will grab it".
  - **Vigyan Recharge**, "How India's Thorium Dream Turned Deadly" (986K; Bhabha's death, scientists' deaths).
    Conspiracy and emotion in the comments.
  - **AKTK**, "How India's Nuclear Success SLAPPED the West?" (345K): chest-thumping, the tone we never use.
  - Thorium hype everywhere: "400 years of free energy", "700 years power secret".
- **What nobody shows:** the reactor that actually makes India's nuclear power (the PHWR, natural uranium, heavy
  water), the 1974 walk-out told as engineering, the pressure tubes, or the people who replace them. Every film jumps
  to thorium and stage 2.
- **News now:** AERB cleared RAPP-8 (Rawatbhata, Rajasthan) for first approach to criticality on 19 NOV 2026, the
  4th indigenous 700 MW unit (PIB PRID 2339225, 20 NOV). Grid power reportedly expected in 2027 (unconfirmed).
  Cameco (Canada) signed a ~US$2.6 bn, nine-year uranium supply deal with India on 2 MAR 2026 during PM Carney's visit
  (WNN, ANS).

## 2. What it actually is (draft)
**The machine.** A PHWR has no single pressure vessel. A tank of cold heavy water (the calandria) is pierced
horizontally by 306 pressure tubes (220 MW) or 392 (540 and 700 MW). Each Zr-2.5%Nb tube (about 103 mm bore, 4.3 mm
wall) holds 12 fuel bundles and carries heavy water at about 100 kg/cm² in at 266 °C, out at 310 °C. The 700 MW design
lets it boil by up to 3% at the channel exit (NPCIL Safety A6; IAEA ARIS). Each hot pressure tube sits inside a cooler
calandria tube, held apart by garter springs. Natural uranium needs no enrichment plant: that's why India chose it.
Refuelling is done on power, by fuelling machines from the control room (BARC 2003: "more than 25,000 channels").

**The wound and the cure.**
- Zircaloy-2 tubes of the early design lasted 10–12 years, not 30, because they picked up hydrogen where they touched
  the calandria tube (NPCIL, *Quest for Excellence: RAPS*, 2017).
- Pickering-2, Canada, 1 AUG 1983: a Zircaloy-2 tube broke after a garter spring moved about a metre and the sagging
  hot tube touched the cold one; hydride blisters cracked (nuclearheritage.com; IAEA INIS). This was the world's
  warning.
- RAPS-2, 1996–97: all 306 tubes replaced with Zr-2.5%Nb using "indigenously developed remote handling tools… for the
  first time in an Indian nuclear reactor and only the second time in the world" (NPCIL 2017). Later MAPS-1 and 2,
  NAPS-1 and 2, KAPS-1 (NPCIL); MAPS-2 in 2002–03 (Varghese et al.); RAPS-3 2024; Kaiga-1 2026 (Powerline, 17 SEP 2026).
- BARC tools: remote creep measurement, wet scraping of slivers to measure hydrogen, a garter-spring repositioning
  system "being developed" (BARC Newsletter Jul 2003). BARC's claim: "saving about 3300 man-rem, generating extra
  electricity worth about 1100 crore rupees".
- Kakrapar-1, 11 MAR 2016: an automatic shutdown at about 9 am after a leak in the primary system; AERB found three
  cracks in one coolant channel, from corrosion caused by impurities in the CO2 annulus gas, limited to KAPS-1 and 2;
  612 channels replaced in both units (~₹500 Cr), finished ahead of schedule (AERB updates; WNN; Business Standard).

**The history (NPCIL 2017 unless marked).**
- Bhabha's three stages: natural uranium first (PHWRs), then fast breeders, then thorium.
- Tarapur 1 and 2 (1969): GE boiling-water reactors, turnkey.
- RAPS-1 (220 MW, crit. 1973), a CANDU built with AECL: "essentially an imported technology". "After India conducted
  the Pokhran-I testing in 1974, the Canadians left, leaving India to face a technology denial regime that was to
  continue for over three decades. Indian scientists and engineers … commissioned RAPS-2 in 1981 with indigenous
  efforts."
- MAPS-1 (Kalpakkam, Tamil Nadu): critical July 1983, the first fully indigenous station; start-up delayed by a
  heavy-water shortage (Wikipedia, check primary). Narora (UP) standardised; Kakrapar (Gujarat) consolidated; Kaiga and
  RAPS-3 to 6 commercial; Tarapur 3 and 4 scaled to 540 MW; then 700 MW.
- Imported content cut to 10–15% (BARC Newsletter 2021). In 2008, the NSG waiver ended the denial regime (NPCIL
  timeline: "Sep. 2008").
- The 700 MW fleet: KAPP-3 first criticality 22 JUL 2020, 9:36 am ("India's first 700 MWe"; PM: "a shining example of
  Make in India"); KAPP-4; RAPP-7 critical 19 SEP 2024, grid 17 MAR 2025, commercial 15 APR 2025, first full 700 MW
  on 10 FEB 2026; RAPP-8 cleared 19 NOV 2026. Fleet-mode units at Kaiga 5 and 6 (Karnataka), Gorakhpur (Haryana),
  Chutka (MP), Mahi Banswara (Rajasthan); find the 2017 Cabinet release for the count and cost.
- Records: RAPS-5 ran 765 days non-stop (6 SEP 2014). Kaiga-1 ran 962 days (13 MAY 2016 to 31 DEC 2018), a world
  record for any nuclear plant, passing Heysham 2 (940) (WNN).
- Heavy water: India was cut off and short in the 1980s (and was accused of diverting Norwegian heavy water, which it
  denied). The Heavy Water Board now calls India "the largest producer of high-quality heavy water in the world" and
  exports to the USA and South Korea (HWB; OEC 2022: about US$14.7M to the US). Attribute the "largest" claim.
- Scale today: 8,780 MW nuclear in 24 reactors (PIB, Dec 2025); about 3% of generation; 100 GW target by 2047
  (Budget 2025–26). Since 2008 many PHWRs run on imported uranium under IAEA safeguards (Cameco 2015: ~3,000 tU;
  2026: ~22M lb over nine years).


## 2b. Second pass (23 NOV): the second refusal, the heart transplant
- **The second refusal (the spine):** Nucleonics Week, 1 JUN 1995 (via CCNR's archive of COG reports): India's DAE
  "has just decided" to retube Rajasthan-2 "with or without outside help", expected to take at least three years. The
  CANDU Owners Group (COG MD Bany Collingwood) wanted to cooperate, but the COG 1994/95 annual report says Canadian
  export policy on India was impeding cooperation. DAE would go alone "even if it takes longer" if Canada continued
  "to curtail COG activities". COG had sent seven Canadian operators to RAPS from 28 FEB to 5 MAR 1993. *So Canada
  walked out of building the reactor in 1974, and in 1995 its rules kept it from helping to repair it. India did the
  repair alone, in 1996–97.* Find the Nucleonics Week original or a second source before the plan locks.
- **Canada's suspension:** "Canada suspended nuclear cooperation with India following the explosion of a bomb at the
  Pokhran site in May 1974"; formally ended in May 1976 (CCNR, advocacy: attribute, or use a Canadian government
  source). The CIRUS research reactor that made the plutonium was Canadian-supplied (CCNR; widely documented).
- **"Heart transplantation":** former NPCIL chairman S.K. Jain likened coolant-channel replacement to "heart
  transplantation in human beings" (Deccan Herald, 18 SEP 2018). KAPS-2 went critical on 17 SEP 2018 after all 306
  channels and the feeders were replaced, three months ahead of the December 2018 target; work began July 2016 (WNN).
  V.K. Jain, Station Director KAPS-1 and 2, Jan 2017: "In all 612 coolant channels in both the units will be changed"
  (IANS via Business Standard). *A named person on record.*
- **Fleet mode:** the Cabinet approved 10 indigenous 700 MW PHWRs on 17 MAY 2017: about ₹70,000 crore in orders to
  Indian industry, 33,400+ jobs, 7,000 MW (PIB via pmindia.gov.in).
- **RAPP-8 fuel loading:** started about 20 SEP 2026, "4,704 fuel bundles across 392 coolant channels" (Business
  Standard, 20 SEP 2026), with commercial operation targeted in FY27. 392 × 12 = 4,704 checks out.
- **A Canadian moment for colour:** Nehru at CIRUS, 1961: "Our reactors, oil refineries, dams and steel plants are our
  new temples" (Scroll, 21 NOV 2026, quoting the archive). Use only if the plan needs the 1960s.

## 3. Our edge, in one sentence
Everyone sells India's nuclear future as thorium. We show the reactor that actually carries India today: born when
Canada walked out in 1974, made of a few hundred thin tubes that crack, sag and age, and kept alive because Indian
engineers learned to replace every tube inside a radioactive core by remote control, a job done "only the second
time in the world" when they first did it, in 1996–97, after Canada's rules had kept its experts from helping.

## 4. The objection ledger
| # | Objection | What the sources say | Where to answer |
|---|---|---|---|
| 1 | "India's reactors now run on Canadian and Russian uranium, so what's indigenous?" | True since 2008 for many units (Cameco 2015, 2026). The design, the tubes, the heavy water and the repair skill are Indian; the fuel is natural uranium bought on the open market, no enrichment needed. | A chapter turn: the irony that Canada sells us the fuel today |
| 2 | "Nuclear is only 3% of India's power. Why care?" | 8.78 GW, ~3%; 100 GW target by 2047 rests mostly on this 700 MW design and the fleet | The landing (yardstick and date) |
| 3 | "Thorium is the real thing. Why not show that?" | Thorium is stage 3; stage 1 (PHWRs) makes the plutonium stage 2 needs; the PFBR went critical 6 APR 2026 | One line plus a picture; pinned comment |
| 4 | "Kakrapar leaked. Is it safe?" | AERB: cracks from corrosion, limited to two units; the leak plugged in 11 days; tubes replaced | The honest wound, told plainly |
| 5 | "And the people near the uranium mines (Jaduguda)?" | Contested health claims; needs separate, careful sourcing | The pinned comment, or one dignified line if sourced |
| 6 | "Fukushima / Chernobyl" | Different reactor types; keep to sourced design features (passive heat removal on 700 MW, BARC 2021) | Only if the plan needs it |

## 5. Story bank (first pass: 17 items, all to become claims rows)
**Moments**
1. 1974: Pokhran-I; Canadian engineers leave the half-built RAPS-2 at Rawatbhata (NPCIL 2017). Find the month the
   AECL team left.
2. 1 AUG 1983, Pickering, Canada: one hot tube cracks after a ring slides a metre (nuclearheritage).
3. July 1983: MAPS-1 at Kalpakkam goes critical, India's first fully indigenous nuclear station.
4. 1996–97: RAPS-2, all 306 tubes cut out and replaced by remote tools ("only the second time in the world").
5. 11 MAR 2016, about 9 am: Kakrapar-1 shuts itself down; heavy water leaks for 11 days until the channel is plugged
   (22 MAR).
6. 31 DEC 2018: Kaiga-1 stops after 962 days non-stop, a world record.
7. 22 JUL 2020, 9:36 am: KAPP-3, the first 700 MW Indian reactor, goes critical, in the middle of the Covid lockdown.
8. 10 FEB 2026: RAPP-7 runs at full 700 MW for the first time.
9. 2 MAR 2026: Canada's Cameco signs a ~US$2.6 bn uranium deal with India (the country that walked out now sells fuel).
10. 19 NOV 2026: AERB clears RAPP-8 (the hook).
**People**
11. Homi Bhabha (the three stages; NPCIL 2017 calls his idea "brewing… even before the nation's independence").
12. The fuelling-machine crews ("dynamic and competent to face the challenges", BARC 2003); find names of RAPS-2 EMCCR
    and Kakrapar EMCCR leaders, and a 700 MW project director on record.
**Objects and senses**
13. A tube about 10 cm wide and about 4 mm thick holding water at about 100 times the air pressure and 310 °C.
14. The garter spring: a ring the size of a bangle that keeps hot from touching cold.
15. Sliver samples scraped from inside a live tube to read its hydrogen (BARC WEST).
**Numbers as things**
16. 392 tubes per 700 MW reactor, 12 bundles each; 962 days ≈ two years and eight months without stopping.
**Ironies and reversals**
17. Cut off from heavy water in the 1980s; now exports it to the USA. Canada walked out in 1974; it signed the
    biggest uranium deal in 2026.

## 6. Pictures that exist (to find in step 7)
NPCIL and DAE photo and video (RAPP-7/8, KAPP-3 control room, the calandria face with 392 end fittings), PIB photos,
Wikimedia Commons (Rawatbhata, Kakrapar, Kaiga), Films Division archive (1970s), CNS and Canadian archive (Pickering
retube, licence check), BARC newsletters (tool drawings, as reference for our renders). The hero 3D shots: the
calandria cut-away with the tubes, the tube inside the tube with the garter spring, the remote tool pulling a tube.

## 7. Still to do
Find the AECL withdrawal month and a Canadian primary source; the 2017 Cabinet fleet-mode release; a named engineer
on record for the EMCCR; KAPP-3 Covid-period detail; Jaduguda sourcing (careful); the RAPP-8 NPCIL release;
`research/search_terms.md`.
