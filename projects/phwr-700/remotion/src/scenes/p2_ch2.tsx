import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {Face306} from '../parts/drawings';
import {CalendarPage, Channel, HydrogenWall, QuoteSlip, SafeStop, TubeLife, Tumbler} from '../parts/drawings2';
import {Archive, ChapterCard, tw} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, draw, hero, lab, pre, shot, tag} from './common';

// Chapter 2 "What breaks a tube" (S45–S79), word_map.md. Pickering news is kept to S59 only (cleared 5–8 s in all:
// 6.4 s across the film). H3 is the drawn channel section (drawings2.tsx).
const S = s0;
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;
const arch = (t: number, name: string, credit: string, year: string, startAt = 0, mono = true) =>
	shot(t, name, (d) => <Archive name={name} dur={d} startAt={startAt} year={year} mono={mono} />, {credit});

/** the vault's light closes like a door (S78): the face darkens from the sides */
const DoorClose: React.FC<{at: number}> = ({at: a}) => {
	const f = useCurrentFrame();
	const k = tw(f, a, a + 70, 0, 1);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<AbsoluteFill style={{background: `linear-gradient(90deg, rgba(0,0,0,0.92) ${k * 46}%, transparent ${k * 46 + 8}%, transparent ${100 - k * 46 - 8}%, rgba(0,0,0,0.92) ${100 - k * 46}%)`}} />
		</AbsoluteFill>
	);
};

const sectionStart = pre(S(60));
const sec = (word: number, l: number) => at(word, sectionStart, l);

export const p2: Part = {
	shots: [
		clip(S(45), 'RAPS_lake', CR.npcil, 3.0),
		// S46–47: Kaiga, 962 days, a world record
		clip(pre(w0(46, 'kaiga')), 'NP_kaiga', CR.npcil),
		clip(pre(w0(46, 'nine')), 'NP_ctrl', CR.npcil),
		clip(S(47), 'NP_panel', CR.npcil),
		// S48: what stops a machine like that? The face, still
		hero(S(48), 'H1_face', 0.5),
		// S49–51: not the fuel; fresh fuel goes in while it runs
		arch(S(49), 'FD80_bundle', CR.fd80, 'FUEL', 0.6),
		clip(pre(w0(51, 'while')), 'K05_fm', CR.npcil, 0, 'KAKRAPAR · FUELLING MACHINE'),
		// S52–53: the tubes wear out; the early tubes, made of an older metal mix
		arch(S(52), 'FD80_rack', CR.fd80, 'THE TUBES'),
		arch(S(53), 'FD80_pilger', CR.fd80, '1980'),
		// S54: they soaked up hydrogen
		draw(S(54), 'hydrogen-wall', (d) => <HydrogenWall dur={d} />, 'ILLUSTRATION'),
		// S55: NPCIL: 10–12 years
		draw(S(55), 'tube-life', (d, l) => <TubeLife shadeAt={at(w0(55, 'ten'), S(55), l)} />, 'SOURCE: NPCIL'),
		// S56: August 1983, near Toronto
		draw(S(56), 'aug-1983', () => <CalendarPage month="AUG" year="1983" />, undefined, [1.0, 0, 30], [1.3, 0, -20]),
		// S57–58: one tube broke at full power; just one, out of hundreds
		draw(S(57), 'face-broke', (d, l) => <Face306 brokeAt={at(w0(57, 'broke'), S(57), l)} />, 'ILLUSTRATION', [1.0, 0, 0], [1.16, -90, 120]),
		// S59: but that is all it takes (the plant video of the time, stamp kept)
		shot(S(59), 'PK_platform', (d) => <Archive name="PK_platform" dur={d} year="PICKERING · 1983" mono={false} />, {credit: CR.pk}),
		// S60–72: one channel in section: the hot tube in the cool tube, the springs, the slip, the sag, the touch,
		// hydrogen to the cold spot, blisters, the crack, the split. The tumbler cuts in at S66–67.
		draw(sectionStart, 'channel', (d, l) => (
			<Channel
				labelsAt={l + 30}
				springsAt={sec(w0(60, 'break'), l)}
			/>
		), 'ILLUSTRATION', [1.0, 0, 0], [1.04, 0, 0]),
		// S61–62: the real thing: a cut sample, the pressure tube inside the calandria tube
		clip(pre(S(61)), 'CNL_cut', 'VIDEO: CANADIAN NUCLEAR LABORATORIES'),
		clip(pre(w0(62, 'coiled')), 'CNL_turn', 'VIDEO: CANADIAN NUCLEAR LABORATORIES'),
		draw(pre(S(63)), 'channel-2', (d, l) => (
			<Channel
				labelsAt={-100}
				springsAt={-100}
				slipA={at(w0(63, 'slipped'), pre(S(63)), l)}
				slipB={at(s1(63), pre(S(63)), l)}
				sagA={at(w0(64, 'sagged') - 30, pre(S(63)), l)}
				sagB={at(w0(65, 'touched'), pre(S(63)), l)}
				coldAt={at(w0(65, 'cold'), pre(S(63)), l)}
			/>
		), 'ILLUSTRATION', [1.0, 0, 0], [1.12, 0, -60]),
		draw(S(66), 'tumbler', (d, l) => <Tumbler dropsA={at(w0(67, 'drops'), S(66), l) - 30} dropsB={at(s1(67), S(66), l)} />, 'ILLUSTRATION', [1.0, 0, 0], [1.1, 0, 30]),
		draw(S(68), 'channel-3', (d, l) => (
			<Channel
				labelsAt={-100}
				springsAt={-100}
				slipA={-100}
				slipB={-90}
				sagA={-100}
				sagB={-90}
				coldAt={-100}
				hA={at(w0(68, 'hydrogen'), S(68), l)}
				hB={at(w0(69, 'coldest'), S(68), l) + 30}
				blisterAt={at(w0(70, 'blisters'), S(68), l)}
				crackA={at(w0(71, 'cracked'), S(68), l)}
				crackB={at(w0(72, 'growing'), S(68), l) + 20}
				splitAt={at(w0(72, 'split'), S(68), l)}
			/>
		), 'ILLUSTRATION', [1.7, 0, -250], [2.3, 0, -380]),   // close on the contact point: TV-readable
		// S73: the operators brought it safely to a stop
		draw(S(73), 'safe-stop', (d, l) => <SafeStop stopA={at(w0(73, 'brought'), S(73), l)} stopB={at(w0(73, 'stop'), S(73), l)} />, 'ILLUSTRATION'),
		// S74: every reactor of this kind had a question: the face pulses
		draw(S(74), 'face-question', (d, l) => <Face306 questionAt={at(w0(74, 'question'), S(74), l) - 20} />, 'ILLUSTRATION', [1.12, 0, 0], [1.0, 0, 0]),
		// S75: Rawatbhata's tubes, the same older metal
		arch(S(75), 'FD80_ends', CR.fd80, 'RAWATBHATA'),
		// S76: Business India, quoted
		draw(S(76), 'quote-bi', (d, l) => (
			<QuoteSlip
				source="BUSINESS INDIA, AS QUOTED"
				text={'“denied detailed knowledge of the accident, its cause and the remedy”'}
				litA={at(w0(76, 'denied'), S(76), l)}
				litB={at(w0(76, 'remedy'), S(76), l) + 30}
			/>
		)),
		// S77: the same disease: one fitting on the face wears
		draw(S(77), 'face-disease', (d, l) => <Face306 wornAt={at(w0(77, 'disease'), S(77), l)} />, 'ILLUSTRATION', [1.0, 0, 0], [1.2, 0, 0]),
		// S78–79: no doctor would come: the light closes on the face; hold on the question
		shot(S(78), 'H1_face-door', (d, l) => (
			<AbsoluteFill>
				{hero(0, 'H1_face', 1.0).el(d, l)}
				<DoorClose at={at(w0(78, 'doctor'), S(78), l)} />
			</AbsoluteFill>
		), {tag: 'ILLUSTRATION'}),
	],
	overlays: [
		lab(S(45), S(45) + 300, 'chapter 2', <ChapterCard n={2} text="WHAT BREAKS A TUBE" />),
		tag(w0(46, 'kaiga'), w0(46, 'nine') - 6, 'KAIGA · KARNATAKA', 140, 860, 56),
		cnt(w0(46, 'nine'), w0(46, 'days'), s1(47) + 20, 962, 'DAYS', 140, 180, 120, C.flask),
		tag(w0(47, 'world'), s1(47) + 20, 'A WORLD RECORD', 140, 860, 60, C.green),
		tag(w0(50, 'not'), s1(50), 'NOT THE FUEL', 140, 860, 60, C.ink),
		tag(w0(52, 'tubes'), s1(52), 'THE TUBES WEAR OUT', 140, 860, 60, C.stress),
		tag(w0(53, 'older'), s1(53), 'AN OLDER METAL MIX', 140, 860, 54),
		tag(w0(56, 'toronto'), s1(56), 'PICKERING · NEAR TORONTO', 140, 860, 54),
		tag(w0(57, 'full'), s1(57), 'AT FULL POWER', 140, 860, 56, C.fail),
		tag(w0(58, 'one'), s1(58), 'JUST ONE', 140, 180, 70, C.fail),
		tag(w0(66, 'glass'), s1(67), 'A COLD GLASS, A HOT DAY', 140, 180, 52),
		tag(w0(75, 'same'), s1(75), 'THE SAME OLDER METAL', 140, 860, 56, C.stress),
		tag(w0(79, 'what'), s1(79) + 40, 'WHAT WOULD YOU HAVE DONE?', 140, 860, 60, C.flask),
	],
};
