import React from 'react';
import type {Part} from '../Film';
import {Face306} from '../parts/drawings';
import {CalendarPage, QuoteSlip, Tumbler} from '../parts/drawings2';
import {EndCard, FaceGrow, GasAlarm, HundredBulbs, IndiaPins, InesScale, PittedWall, RodsDrop, TenDomes, TenYears, TradeAgain, TypedQuestion} from '../parts/drawings4';
import {ChapterCard} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, draw, hero, lab, pre, shot, SubscribePill, tag} from './common';
import {RupeeMark} from './p3_ch3';

// Chapter 4 "Kakrapar: the worst day" (S122–S145), chapter 5 "From 306 to 392" (S146–S175), the landing (S176–S189)
// and the end card. No footage of the 2016 leak day exists: the map, the regulator's words and plain drawings carry it.
// Shots whose plant is not named in the source carry ILLUSTRATIVE FOOTAGE.
const S = s0;
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;
const ILL = 'ILLUSTRATIVE FOOTAGE · NPCIL';

export const p4: Part = {
	shots: [
		// S122–125: be fair; is it safe to live near one? the worst day
		clip(S(122), 'K05_towers', CR.npcil, 0, ILL),
		clip(S(124), 'RAPS_road', CR.npcil),
		// S126–128: 11 MAR 2016, Kakrapar, Gujarat, about nine in the morning
		draw(S(126), 'mar-2016', () => <CalendarPage month="11 MAR" year="2016" />, undefined, [1.0, 0, 30], [1.3, 0, -20]),
		shot(S(127), 'map-kakrapar', (d, l) => <IndiaPins dur={d} mode="kakrapar" at={l + 6} />, {tag: 'MAP: NATURAL EARTH · INDIA’S OFFICIAL BOUNDARY'}),
		// S129: the reactor shut itself down
		draw(S(129), 'rods', (d, l) => <RodsDrop dropAt={at(w0(129, 'shut'), S(129), l)} />, 'SIMPLIFIED'),
		// S130–131: no fuel failure; the regulator: no radiation harm
		clip(S(130), 'K05_ctrl', CR.npcil, 0, ILL),
		clip(pre(w0(131, 'people')), 'RAPS_lake', CR.npcil, 4.5),
		// S132–134: two out of seven: an incident
		draw(S(132), 'ines', (d, l) => <InesScale litAt={at(w0(133, 'two'), S(132), l)} />, 'SOURCE: IAEA INES'),
		// S135–137: a wrong chemical; small spots in the outer walls
		draw(S(135), 'pits', (d, l) => <PittedWall pitA={at(w0(137, 'eaten'), S(135), l)} pitB={at(s1(137), S(135), l)} />, 'ILLUSTRATION'),
		// S138–140: only in Kakrapar's two units
		shot(S(138), 'map-fleet', (d, l) => <IndiaPins dur={d} mode="fleet" at={at(w0(140, 'kakrapars'), S(138), l)} />, {tag: 'MAP: NATURAL EARTH · INDIA’S OFFICIAL BOUNDARY'}),
		// S141–143: every tube came out, 306 in each
		clip(S(141), 'RAPS_face', CR.npcil, 0, 'RAWATBHATA · ILLUSTRATIVE FOOTAGE'),
		draw(S(142), 'face-out', (d, l) => <Face306 greyAt={l} />, 'ILLUSTRATION', [1.0, 0, 0], [1.1, 0, 0]),
		// S144–145: a heart transplant
		draw(S(144), 'quote-heart', (d, l) => (
			<QuoteSlip source="S.K. JAIN, FORMER CHAIRMAN, NPCIL · AS REPORTED" text="Like a heart transplant for a human being" litA={at(S(145), S(144), l)} litB={at(s1(145), S(144), l)} />
		)),
		// S146: the start of a bigger story: the 700's face
		clip(S(146), 'K05_face700', CR.npcil, 0, undefined, 'none'),
		// S147–148: count with your eyes: 306 grows to 392
		draw(S(147), 'face-grow', (d, l) => <FaceGrow growA={at(w0(148, 'grow'), S(147), l)} growB={at(s1(148), S(147), l)} />, 'ILLUSTRATION', [1.06, 0, 0], [1.0, 0, 0]),
		// S149: India's own 700, designed here
		clip(S(149), 'K05_caps', CR.npcil),
		// S150–153: the dry gas, the drop, the dew, the alarm; the tumbler returns on "remember that glass?"
		draw(S(150), 'gas', (d, l) => <GasAlarm dropAt={at(w0(151, 'drop'), S(150), l)} alarmAt={at(w0(153, 'alarm'), S(150), l) - 6} />, 'ILLUSTRATION'),
		draw(S(152), 'tumbler-2', (d, l) => <Tumbler dropsA={l - 40} dropsB={l + 20} />, 'ILLUSTRATION'),
		draw(S(153), 'gas-2', (d, l) => <GasAlarm dropAt={-200} alarmAt={at(w0(153, 'alarm'), S(153), l) - 6} />, 'ILLUSTRATION'),
		// S154–158: Kakrapar's first 700 went critical in July 2020; critical = good news; tests in the lockdown
		clip(S(154), 'K05_ctrl', CR.npcil, 2.5, ILL),
		clip(S(155), 'K05_vault', CR.npcil, 0, ILL, 'none'),
		clip(S(158), 'NP_eng', CR.npcil),
		// S159–160: Rawatbhata got its own: unit seven
		clip(S(159), 'R7_aerial', CR.npcil),
		clip(pre(w0(160, 'unit')), 'R7_cheer', CR.npcil),
		clip(pre(w0(160, 'full')), 'R7_dome', CR.npcil),
		// S161–162: this September, the same lake, unit eight takes its fuel
		clip(S(161), 'RAPS_lake', CR.npcil, 0.5),
		clip(pre(w0(161, 'unit')), 'K4_fuel', CR.npcil, 0, 'ILLUSTRATIVE FOOTAGE · KAKRAPAR-4'),
		// S163–164: the honest part: 3 in 100
		draw(S(163), 'bulbs', (d, l) => <HundredBulbs litAt={at(w0(164, 'three'), S(163), l)} />, 'ILLUSTRATION'),
		// S165–168: late: 2010 → 2020
		draw(S(165), 'ten-years', (d, l) => <TenYears aAt={at(w0(167, 'twenty'), S(165), l)} bAt={at(w0(168, 'ten'), S(165), l)} />, 'ILLUSTRATION'),
		// S169–170: ten more, one fleet; ₹70,000 crore of orders
		draw(S(169), 'ten-domes', (d, l) => <TenDomes at={at(w0(169, 'ten'), S(169), l)} />, 'ILLUSTRATION'),
		// S171–175: the quiet ending: the file opens again
		draw(S(171), 'trade', (d, l) => <TradeAgain openAt={at(w0(172, 'canadian'), S(171), l)} sheetAt={at(w0(173, 'ten'), S(171), l)} />, 'ILLUSTRATION'),
		// S176–179: the fuel can be bought; the skill had to be grown
		clip(S(176), 'K4_fuel', CR.npcil, 3.0, 'ILLUSTRATIVE FOOTAGE · KAKRAPAR-4'),
		clip(S(178), 'NP_eng', CR.npcil, 2.0),
		clip(pre(w0(179, 'grow')), 'RAPS_cheer', CR.npcil, 1.0),
		// S180–182: the date to watch, on the same ground Canada left
		clip(S(180), 'RAPS_dusk', CR.npcil),
		// S183: the saying, over the face with the flask locked
		hero(S(183), 'H1_face', 540 / 60),
		// S184–185: next, 7 PM: India's lights come on; subscribe
		shot(S(184), 'map-lights', (d, l) => <IndiaPins dur={d} mode="lights" at={at(w0(184, 'lights'), S(184), l)} />, {tag: 'MAP: NATURAL EARTH · INDIA’S OFFICIAL BOUNDARY'}),
		// S186–187: the question
		draw(S(186), 'question', (d, l) => <TypedQuestion at={at(S(187), S(186), l)} text="Would you have waited for help, or opened it yourself?" />),
		// S188 → the end card (15 s, the end screen sits in its lower half)
		draw(S(188), 'end', (d) => <EndCard dur={d} />, undefined, [1.0, 0, 0], [1.06, 0, 0]),
	],
	overlays: [
		lab(S(122), S(122) + 300, 'chapter 4', <ChapterCard n={4} text="KAKRAPAR: THE WORST DAY" />),
		tag(w0(128, 'nine'), s1(128), 'ABOUT 9 AM · A TUBE LEAKS', 140, 860, 54, C.stress),
		tag(w0(130, 'no'), s1(130), 'NO FUEL FAILURE', 140, 860, 60, C.green),
		tag(w0(131, 'regulator'), s1(131), 'NO RADIATION HARM · AERB', 140, 860, 54, C.green),
		tag(w0(134, 'incident'), s1(134), 'AN INCIDENT, NOT AN ACCIDENT', 140, 180, 54, C.flask),
		tag(w0(136, 'chemical'), s1(136), 'A WRONG CHEMICAL IN THE GAS', 140, 860, 54, C.stress),
		tag(w0(139, 'no'), s1(140), 'NO', 140, 180, 80, C.green),
		tag(w0(143, 'three'), s1(143), '306 IN EACH REACTOR', 140, 180, 60, C.flask),
		lab(S(147), S(147) + 300, 'chapter 5', <ChapterCard n={5} text="FROM 306 TO 392" />),
		cnt(w0(148, 'grow'), s1(148), s1(148) + 30, 392, 'TUBES', 140, 820 - 640, 110, C.flask, 306),
		tag(w0(149, 'seven'), s1(149), 'INDIA’S OWN 700 MW', 140, 860, 60, C.ink),
		tag(w0(154, 'july'), s1(154), 'KAKRAPAR-3 · JULY 2020', 140, 860, 54),
		tag(w0(155, 'critical'), s1(157), 'CRITICAL = THE CHAIN REACTION HOLDS STEADY', 140, 860, 46, C.green),
		tag(w0(158, 'lockdown'), s1(158), 'TESTED IN THE LOCKDOWN', 140, 860, 54),
		tag(w0(160, 'march'), w0(160, 'full') - 6, 'UNIT 7 · ON THE GRID · MAR 2025', 140, 860, 50),
		tag(w0(160, 'february'), s1(160), 'FULL POWER · FEB 2026', 140, 860, 54, C.green),
		tag(w0(161, 'unit'), s1(161), 'UNIT 8 · FUEL · SEP 2026', 140, 860, 54, C.flask),
		cnt(w0(162, 'four'), w0(162, 'bundles'), s1(162) + 20, 4700, 'BUNDLES', 140, 180, 100, C.flask),
		tag(w0(162, 'three'), s1(162) + 20, 'FOR 392 TUBES', 140, 320, 50, C.ink),
		tag(w0(166, 'no'), s1(166) + 10, 'NO', 140, 180, 80, C.fail),
		cnt(w0(170, 'seventy'), w0(170, 'crore'), s1(170) + 20, 70000, 'CRORE', 230, 180, 100, C.green),
		lab(w0(170, 'seventy') - 6, s1(170) + 20, 'rupee-70k', <RupeeMark />),
		tag(w0(170, 'indian'), s1(170) + 20, 'ORDERS FOR INDIAN INDUSTRY', 140, 860, 50),
		tag(w0(174, 'not'), s1(175) + 20, 'NOT REVENGE. TRADE.', 140, 180, 60, C.flask),
		lab(S(176), S(176) + 300, 'landing', <ChapterCard n={6} text="WHAT IT MEANS TODAY" />),
		tag(w0(177, 'fuel'), s1(177), 'THE FUEL: INDIA CAN BUY', 140, 860, 56),
		tag(w0(178, 'skill'), s1(179), 'THE SKILL: INDIA HAD TO GROW IT', 140, 860, 54, C.flask),
		tag(w0(181, 'rajasthan'), s1(182), 'RAPP-8 · FIRST CRITICALITY', 140, 760, 64, C.flask, false, 'YOUR DATE TO WATCH'),
		tag(w0(183, 'machine'), s1(183), 'TRULY YOURS ONLY WHEN YOU CAN OPEN IT, AND MEND IT', 140, 860, 44, C.flask),
		tag(w0(184, 'seven'), s1(184), 'NEXT: 7 PM', 140, 180, 70, C.flask),
		lab(w0(185, 'subscribe') - 6, s1(185) + 30, 'subscribe-2', <SubscribePill press={18} />),
	],
};

