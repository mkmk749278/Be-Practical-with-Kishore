import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {ExportFile, Face306} from '../parts/drawings';
import {QuoteSlip} from '../parts/drawings2';
import {ClubTable, CostStacks, DoseMeter, FirstSecond, NoPowerYears, OpenRadio, ToolSheet, TubeJourney} from '../parts/drawings3';
import {Archive, ChapterCard, tw, useSpring} from '../parts/kit';
import {C, F} from '../theme';
import {s0, s1, w0} from '../timing';
import {clip, cnt, CR, draw, hero, lab, pre, shot, SubscribePill, tag} from './common';

// Chapter 3 "India opens the heart itself" (S80–S121), word_map.md. H4 is drawn (drawings3.tsx TubeJourney).
// Names (Chaturvedi, Arya) sit over places, never over a face we cannot name (no face implied).
const S = s0;
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;
const arch = (t: number, name: string, credit: string, year: string, startAt = 0, mono = true) =>
	shot(t, name, (d) => <Archive name={name} dur={d} startAt={startAt} year={year} mono={mono} />, {credit});
const CA = 'VIDEO: ONTARIO POWER GENERATION';
const BR = 'VIDEO: BRUCE POWER';

/** the take-home saying, typeset large, arriving word group by word group (S118) */
const Saying: React.FC = () => {
	const p = useSpring(0, 110, 20);
	const q = useSpring(70, 110, 20);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `rgba(3,7,13,${0.55 * p})`}}>
			<div style={{fontFamily: F.label, fontWeight: 800, fontSize: 84, color: C.ink, textAlign: 'center', lineHeight: 1.15, maxWidth: 1500, textShadow: '0 6px 30px rgba(0,0,0,0.9)'}}>
				<div style={{opacity: p, transform: `translateY(${(1 - p) * 20}px)`}}>A MACHINE IS TRULY YOURS</div>
				<div style={{opacity: q, transform: `translateY(${(1 - q) * 20}px)`, color: C.flask}}>ONLY WHEN YOU CAN OPEN IT, AND MEND IT.</div>
			</div>
		</AbsoluteFill>
	);
};

/** Kishore's desk at the subscribe ask: the small TV remote on the table under the lamp (S119–S121) */
const RemoteDesk: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<g transform={`translate(1280 ${620 - 6 * Math.sin(f / 40)}) rotate(-18)`}>
				<rect x={-70} y={-220} width={140} height={440} rx={40} fill="#1b1d20" stroke="#3b4147" strokeWidth={4} />
				<circle cx={0} cy={-150} r={20} fill={C.fail} />
				{[0, 1, 2, 3].map((r) => [0, 1, 2].map((c) => <rect key={`${r}${c}`} x={-48 + c * 36} y={-80 + r * 44} width={24} height={24} rx={6} fill="#4b525a" />))}
				<circle cx={0} cy={140} r={36} fill="#3b4147" />
			</g>
		</svg>
	);
};

/** the ₹ sign before the counter (Count shows the number only) */
export const RupeeMark: React.FC = () => {
	const f = useCurrentFrame();
	return <div style={{position: 'absolute', left: 140, top: 186, fontFamily: F.mono, fontWeight: 700, fontSize: 110, color: C.green, opacity: tw(f, 0, 12, 0, 1), textShadow: '0 4px 24px rgba(0,0,0,0.8)'}}>₹</div>;
};

export const p3: Part = {
	shots: [
		// S80–81: the 1995 trade weekly, quoted; "with or without outside help" lights
		draw(S(80), 'quote-1995', (d, l) => (
			<QuoteSlip
				source="A NUCLEAR TRADE WEEKLY, 1995 · AS QUOTED"
				text={'“…decided to retube Rajasthan-2, with or without outside help”'}
				litA={at(w0(81, 'rajasthan'), S(80), l)}
				litB={at(w0(81, 'help'), S(80), l) + 20}
			/>
		)),
		// S82: the owners' club, India's seat
		draw(S(82), 'club', (d, l) => <ClubTable indiaAt={at(w0(82, 'india'), S(82), l)} />, 'ILLUSTRATION'),
		// S83: the export file again, stamped
		draw(S(83), 'export-again', (d, l) => <ExportFile stampAt={at(w0(83, 'kept'), S(83), l)} />, 'ILLUSTRATION'),
		// S84–86: the job came home: Rawatbhata; the names over the place
		clip(S(84), 'RAPS_drive', CR.npcil, 2.0),
		clip(S(85), 'RAPS_plant', CR.npcil),
		clip(S(86), 'RAPS_lake', CR.npcil, 1.0),
		// S87: can you picture the hardest part? the face
		hero(S(87), 'H1_face', 2.0),
		// S88: all 306 had been in a running reactor for years: the real Rawatbhata face
		clip(S(88), 'RAPS_core', CR.npcil, 0, undefined, 'none'),
		// S89–90: you cannot stand near it
		draw(S(89), 'dose', (d, l) => <DoseMeter swingAt={at(w0(89, 'stand'), S(89), l)} />, 'ILLUSTRATION'),
		// S91: every cut, pull, weld by machines (Canada's today; India's 1980 rig on "weld")
		clip(S(91), 'OPG_tool', CA, 0, 'DARLINGTON, CANADA'),
		arch(pre(w0(91, 'weld')), 'FD80_fmh', CR.fd80, 'INDIA · 1980'),
		// S92–93: machines that did not exist yet; Indian engineers designed them
		draw(S(92), 'tool-sheet', (d, l) => <ToolSheet fillAt={at(S(93), S(92), l)} />, 'ILLUSTRATION'),
		// S94–98: the old tube's journey
		draw(S(94), 'journey', (d, l) => (
			<TubeJourney
				cutAt={at(w0(95, 'cuts'), S(94), l)}
				drawA={at(w0(96, 'drawn'), S(94), l)}
				drawB={at(s1(96), S(94), l)}
				carryA={at(w0(97, 'carries'), S(94), l)}
				carryB={at(s1(97), S(94), l) + 30}
			/>
		), 'ILLUSTRATION', [1.0, 0, 0], [1.06, 0, 0]),
		// S99: from a distance: engineers at the screens
		clip(S(99), 'RAPS_screens', CR.npcil),
		// S100: a new tube goes in (Bruce Power's rollers, Canada)
		clip(S(100), 'BRU_feed', BR, 0, 'A NEW TUBE · CANADA'),
		// S101: a stronger mix, zirconium with niobium
		arch(S(101), 'FD80_zr', CR.fd80, 'ZIRCONIUM'),
		// S102–103: the next, 306 times: the face turns caution yellow, tube by tube
		draw(S(102), 'face-new', (d, l) => <Face306 newA={l} newB={at(s1(103), S(102), l)} />, 'ILLUSTRATION', [1.12, 0, 0], [1.0, 0, 0]),
		// S104–106: the cost
		draw(S(104), 'cost', (d, l) => <CostStacks indiaAt={at(w0(105, 'two'), S(104), l)} canadaAt={at(w0(106, 'more'), S(104), l)} />, 'OUR CALCULATION · BUSINESS INDIA, RBI 1996 RATE'),
		// S107–109: was it quick? no: three years, no power
		draw(S(107), 'no-power', (d, l) => <NoPowerYears at={at(w0(109, 'nineteen'), S(107), l)} />, 'ILLUSTRATION'),
		// S110: by 1998, running again
		clip(S(110), 'RAPS_lake', CR.npcil, 2.4),
		// S111–112: first in India, second in the world; the first in Canada
		draw(S(111), 'first-second', (d, l) => <FirstSecond secondAt={at(w0(111, 'second'), S(111), l)} firstAt={at(w0(112, 'first'), S(111), l)} />, 'SOURCE: NPCIL'),
		// S113–114: BARC counted the gain
		arch(S(113), 'FDB_barc', CR.fd, 'TROMBAY'),
		// S115–116: the broken radio we opened
		draw(S(115), 'radio', (d, l) => <OpenRadio openAt={at(w0(116, 'opened'), S(115), l)} />),
		// S117: the lesson of Rawatbhata
		clip(S(117), 'RAPS_cheer', CR.npcil),
		// S118: the saying over the crew in yellow at the face
		shot(S(118), 'saying', (d) => (
			<AbsoluteFill>
				{clip(0, 'RAPS_yellow', CR.npcil).el(d, 0)}
				<Saying />
			</AbsoluteFill>
		), {credit: CR.npcil}),
		// S119–121: subscribe; on the TV, the remote
		draw(S(119), 'subscribe', () => <RemoteDesk />, undefined, [1.04, 0, 0], [1.12, -30, 0]),
	],
	overlays: [
		lab(S(80), S(80) + 300, 'chapter 3', <ChapterCard n={3} text="INDIA OPENS THE HEART ITSELF" />),
		tag(w0(84, 'home'), s1(84), 'RAWATBHATA', 140, 860, 64),
		tag(w0(85, 'v'), s1(85) + 10, 'V.K. CHATURVEDI', 140, 760, 64, C.ink, false, 'PROJECT DIRECTOR, RAWATBHATA'),
		tag(w0(86, 'r'), s1(86) + 10, 'R.C. ARYA', 140, 760, 64, C.ink, false, 'LED THE TUBE TEAM'),
		tag(w0(88, 'years'), s1(88), 'YEARS INSIDE A RUNNING REACTOR', 140, 860, 50, C.stress),
		tag(w0(90, 'not'), s1(90) + 20, 'NOT FOR A MINUTE', 140, 180, 64, C.fail),
		tag(w0(91, 'machines'), s1(91), 'BY MACHINES', 140, 860, 60),
		tag(w0(92, 'exist'), s1(92), 'DID NOT EXIST YET', 140, 180, 60, C.ink),
		tag(w0(99, 'distance'), s1(99), 'FROM A DISTANCE', 140, 860, 60),
		tag(w0(101, 'zirconium'), s1(101), 'ZIRCONIUM + NIOBIUM', 140, 860, 60, C.flask),
		cnt(w0(102, 'next') - 6, s1(103), s1(103) + 30, 306, 'NEW TUBES', 140, 180, 110, C.flask),
		tag(w0(108, 'no'), s1(109), 'NO', 140, 180, 90, C.fail),
		tag(w0(110, 'nineteen'), s1(110), '1998 · RUNNING AGAIN', 140, 860, 60, C.green),
		tag(w0(113, 'bhabha'), s1(113), 'BHABHA ATOMIC RESEARCH CENTRE', 140, 860, 48),
		cnt(w0(114, 'one'), w0(114, 'crore'), s1(114) + 30, 1100, 'CRORE', 230, 180, 110, C.green),
		lab(w0(114, 'one') - 6, s1(114) + 30, 'rupee', <RupeeMark />),
		tag(w0(114, 'electricity'), s1(114) + 30, 'OF EXTRA ELECTRICITY', 140, 330, 50, C.ink),
		tag(w0(117, 'rawatbhata'), s1(117), 'THE LESSON OF RAWATBHATA', 140, 860, 56),
		lab(w0(119, 'subscribe') - 6, s1(121) + 60, 'subscribe', <SubscribePill press={w0(121, 'subscribe') - w0(119, 'subscribe') + 6} />),
	],
};
