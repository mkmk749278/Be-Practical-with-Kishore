import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame} from 'remotion';
import type {Part} from '../Film';
import {DesignSheet, ExportFile, Face306, MayPage, PotTank, RajMap, TubeWall, Weights, Cooker} from '../parts/drawings';
import {Archive, ChapterCard, tw} from '../parts/kit';
import {C} from '../theme';
import {s0, s1, w0} from '../timing';
import {ask, clip, cnt, CR, draw, hero, lab, pre, shot, tag} from './common';

// Cold open (S0–S9) and chapter 1 "306 pressure cookers" (S10–S44), word_map.md. Every frame comes from the locked
// audio. H1_face = Blender hero 1 (Drive renders/face, prepared at 60 fps): its own frame numbers are given in /60 s.
const S = s0;
/** a word's frame inside a shot that starts at `at` with lead `l` */
const at = (word: number, shotStart: number, l: number) => word - shotStart + l;

/** an archive clip laid on the drafting table, with its year and maker */
const arch = (t: number, name: string, credit: string, year: string, startAt = 0, mono = true, mask = 0) =>
	shot(t, name, (d) => <Archive name={name} dur={d} startAt={startAt} year={year} maker={undefined} mono={mono} mask={mask} />, {credit});

const open: Part = {
	shots: [
		// S0: the first frame is the thumbnail's subject: the 306 face in the dark vault, the push begins
		hero(S(0), 'H1_face', 0),
		// "half built": the dome of the time, half of it masked in scaffold grey
		shot(pre(w0(0, 'half')), 'FDA_dome', (d) => <Archive name="FDA_dome" dur={d} year="1970s" mono mask={1} />, {credit: CR.fd}),
		// "on the Chambal river, in Rajasthan": the official map, Rajasthan lit, the Chambal drawn, Rawatbhata pinned
		shot(pre(w0(0, 'on the chambal')), 'map-chambal', (d, l) => (
			<RajMap dur={d} mode="chambal" rajAt={at(w0(0, 'rajasthan'), pre(w0(0, 'on the chambal')), l)} riverA={at(w0(0, 'chambal'), pre(w0(0, 'on the chambal')), l)} riverB={at(w0(0, 'river'), pre(w0(0, 'on the chambal')), l) + 30} pinAt={at(w0(0, 'rajasthan'), pre(w0(0, 'on the chambal')), l) + 10} />
		), {tag: 'MAP: NATURAL EARTH · INDIA’S OFFICIAL BOUNDARY'}),
		// S1: an Indian operator sits down to work
		arch(S(1), 'FDA_panel', CR.fd, '1980s', 0, false),
		// S2: back to the face, the push goes on; one end fitting near the centre wears out
		draw(S(2), 'face-worn', (d, l) => <Face306 wornAt={at(w0(2, 'wearing'), S(2), l)} />, 'ILLUSTRATION', [1.0, 0, 0], [1.12, 0, -10]),
		// S3: 306, counted on the face
		draw(S(3), 'face-count', (d, l) => <Face306 countA={at(w0(3, 'three'), S(3), l)} countB={at(w0(3, 'tubes'), S(3), l)} />, 'ILLUSTRATION', [1.08, 0, 0], [1.0, 0, 0]),
		// S4–5: the only country that had done it: Pickering, 1983 (owner cleared, 26 NOV: 5–8 s, credited)
		arch(pre(w0(4, 'replaced')), 'PK_face', CR.pk, 'PICKERING · 1983', 0, false),
		arch(pre(S(5)), 'PK_station', CR.pk, 'CANADA', 0, false),
		// S6: the export file; the stamp lands on "kept"
		draw(S(6), 'export-file', (d, l) => <ExportFile stampAt={at(w0(6, 'kept'), S(6), l)} />, 'ILLUSTRATION'),
		// S7: the yellow flask glides in on its rails; the clunk lands in the gap after the sentence (render frame 480)
		hero(S(7), 'H1_face', 240 / 60),
		// S8: Indian engineers at the face, one tube carried out, back to the flask settling after the lock
		clip(pre(w0(8, 'indian')), 'RAPS_face', CR.npcil),
		clip(pre(w0(8, 'one')), 'RAPS_tube', CR.npcil),
		hero(pre(w0(8, 'steel')), 'H1_face', 500 / 60),
		// S9: the new reactor taking in fuel (a sister 700 at Kakrapar) → the same lake
		clip(pre(w0(9, 'new')), 'K4_fuel', CR.npcil, 0, 'ILLUSTRATIVE FOOTAGE · KAKRAPAR-4'),
		clip(pre(w0(9, 'same')), 'RAPS_lake', CR.npcil),
	],
	overlays: [
		tag(w0(0, 'nineteen'), w0(0, 'half'), '1974', 140, 180, 90, C.flask, true),
		tag(w0(2, 'twenty'), s1(2), '20 YEARS LATER', 140, 180, 60, C.ink, true),
		cnt(w0(3, 'three'), w0(3, 'tubes'), s1(3) + 30, 306, 'TUBES', 140, 180, 120, C.flask),
		tag(w0(4, 'only'), s1(4), 'ONLY ONE COUNTRY HAD DONE IT', 140, 860, 50),
		tag(w0(6, 'export'), s1(6), 'CANADA’S EXPORT RULES', 140, 180, 52, C.ink),
		tag(w0(8, 'flask'), s1(8), 'A STEEL FLASK', 140, 860, 56, C.flask),
		tag(w0(9, 'september'), w0(9, 'same'), 'SEPTEMBER 2026', 140, 180, 60, C.ink, true),
		tag(w0(9, 'lake'), s1(9), 'THE SAME LAKE', 140, 860, 56),
	],
};

const ch1: Part = {
	shots: [
		clip(S(10), 'RAPS_drive', CR.npcil),
		clip(pre(w0(10, 'rawatbhata')), 'RAPS_gate', CR.npcil),
		clip(S(11), 'RAPS_lake', CR.npcil, 2.2),
		shot(pre(w0(11, 'sixty')), 'map-kota', (d, l) => <RajMap dur={d} mode="kota" roadA={at(w0(11, 'sixty'), pre(w0(11, 'sixty')), l)} roadB={at(w0(11, 'kota'), pre(w0(11, 'sixty')), l)} kmAt={at(w0(11, 'kilometres'), pre(w0(11, 'sixty')), l)} />, {tag: 'MAP: NATURAL EARTH'}),
		// S12: the 1960s: the plan on the map, then the engineers' drawing hall
		arch(S(12), 'FD80_map', CR.fd80, '1960s', 2.6),
		arch(pre(w0(12, 'canada and india')), 'FD80_dae', CR.fd80, 'DEPARTMENT OF ATOMIC ENERGY', 2.0),
		arch(pre(w0(12, 'building')), 'FD80_draw', CR.fd80, '1970s'),
		// S13–14: the design sheet slides in; the lamp warms on the question
		draw(S(13), 'design-sheet', (d, l) => <DesignSheet lampAt={at(S(14), S(13), l)} />, 'ILLUSTRATION'),
		// S15: Trombay, where the choice was made
		arch(S(15), 'FDB_trombay', CR.fd, 'TROMBAY · 1960s', 1.6),
		// S16–18: no enriched uranium; natural uranium in fuel bundles; Indian factories
		arch(S(16), 'FD80_uplant', CR.fd80, 'URANIUM OXIDE PLANT'),
		arch(S(17), 'FD80_bundle', CR.fd80, 'NATURAL URANIUM FUEL'),
		arch(S(18), 'FD80_tubes', CR.fd80, 'MADE IN INDIA'),
		// S19–23: the giant pot (most reactors) dissolves into a tank pierced by 306 tubes; one becomes a cooker
		draw(S(19), 'pot-tank', (d, l) => (
			<PotTank
				dissolveAt={at(S(21), S(19), l)}
				tankAt={at(w0(22, 'tank'), S(19), l) - 10}
				pierceA={at(w0(22, 'pierced'), S(19), l)}
				pierceB={at(w0(22, 'tubes'), S(19), l) + 20}
				liftAt={at(w0(23, 'each'), S(19), l)}
				cookerAt={at(w0(23, 'pressure'), S(19), l)}
			/>
		), 'ILLUSTRATION', [1.0, 0, 0], [1.1, 0, 20]),
		// S24–25: the cooker in your kitchen; the whistle lifts (stock kitchen footage: requested in the next round)
		draw(S(24), 'cooker', (d, l) => <KitchenCooker whistleAt={at(w0(25, 'whistle'), S(24), l)} dur={d} />, 'ILLUSTRATION', [1.04, 0, 0], [1.14, 0, -30]),
		// S26: one kilo on a square centimetre
		draw(S(26), 'weight-one', (d, l) => <Weights oneAt={at(w0(26, 'one'), S(26), l)} />, 'OUR CALCULATION'),
		// S27: India's newest: the 700 at Rawatbhata
		clip(S(27), 'R7_dome', CR.npcil),
		clip(pre(w0(27, 'moment')), 'R7_towers', CR.npcil),
		// S28: a hundred times harder, at 310 °C
		draw(S(28), 'weight-100', (d, l) => <Weights oneAt={-60} stackA={at(w0(28, 'hundred'), S(28), l)} stackB={at(w0(28, 'harder'), S(28), l) + 20} tempAt={at(w0(28, 'three'), S(28), l)} />, 'OUR CALCULATION'),
		// S29–31: the wall in section; the pencil; thinner than that
		draw(S(29), 'tube-wall', (d, l) => <TubeWall pencilAt={at(S(30), S(29), l)} compareAt={at(S(31), S(29), l)} />, 'ILLUSTRATION · TO SCALE', [1.0, 0, 0], [1.18, -60, 0]),
		// S32–33: May 1974
		draw(S(32), 'may-1974', () => <MayPage />, undefined, [1.0, 0, 30], [1.3, 0, -20]),
		// S34: Pokhran
		shot(pre(S(34)), 'TH74_blast', (d) => <Archive name="TH74_blast" dur={d} startAt={1.6} year="18 MAY 1974" aspect={1290 / 900} punch />, {credit: CR.fdTH, hard: true}),
		// S35–36: the test site after
		arch(S(35), 'FDA_pokhran', CR.fd, 'POKHRAN · 1974'),
		// S37: CIRUS at Trombay
		arch(S(37), 'FDB_hall', CR.fd, 'TROMBAY'),
		arch(pre(w0(37, 'cyrus')), 'FDB_cirus', CR.fd, 'CIRUS'),
		// S38: the file shuts
		draw(S(38), 'export-close', (d, l) => <ExportFile closeAt={at(w0(38, 'stopped'), S(38), l)} />, 'ILLUSTRATION'),
		// S39: the dome, empty; the light drops
		shot(S(39), 'FDA_dome-empty', (d) => (
			<AbsoluteFill>
				<Archive name="FDA_dome" dur={d} year="1974" startAt={1.5} />
				<LightDrop dur={d} />
			</AbsoluteFill>
		), {credit: CR.fd}),
		// S40: the first unit was running
		arch(S(40), 'FDA_panel', CR.fd, 'UNIT 1', 2.4, false),
		// S41: the second, half done: half the face greys out
		arch(S(41), 'FD80_ends', CR.fd80, 'UNIT 2'),
		draw(pre(w0(41, 'halfway')), 'face-half', (d, l) => <Face306 greyAt={l} />, 'ILLUSTRATION'),
		// S42: "You might ask me, Kishore…"
		draw(S(42), 'ask-desk', (d) => <KitchenCooker whistleAt={99999} dur={d} small />, undefined, [1.1, 0, 0], [1.0, 0, 0]),
		// S43–44: Indian engineers finished it; it went to work in 1981
		arch(S(43), 'FD80_face', CR.fd80, '1970s'),
		draw(pre(w0(44, 'work')), 'face-relit', (d, l) => <Face306 greyAt={-100} relightAt={l} />, 'ILLUSTRATION'),
	],
	overlays: [
		lab(S(10), S(10) + 300, 'chapter 1', <ChapterCard n={1} text="306 PRESSURE COOKERS" />),
		tag(w0(10, 'rawatbhata'), s1(10) + 30, 'RAWATBHATA', 140, 860, 64),
		tag(w0(11, 'rana'), w0(11, 'sixty') - 8, 'RANA PRATAP SAGAR', 140, 860, 56),
		tag(w0(12, 'nineteen'), s1(12), 'THE 1960s', 140, 180, 60, C.ink, true),
		tag(w0(16, 'no'), s1(16), 'NO ENRICHED URANIUM', 140, 860, 56, C.flask),
		tag(w0(17, 'natural'), s1(17), 'NATURAL URANIUM', 140, 860, 56, C.green),
		tag(w0(22, 'three'), s1(22), '306 TUBES', 140, 180, 70, C.flask, true),
		tag(w0(26, 'one'), s1(26), '1 KG ON 1 CM²', 140, 180, 60, C.ink, true),
		tag(w0(27, 'newest'), s1(27), 'RAWATBHATA · 700 MW', 140, 860, 54),
		tag(w0(29, 'four'), s1(29), '≈ 4 MM', 140, 180, 90, C.flask, true),
		tag(w0(34, 'pokhran'), s1(36), 'POKHRAN', 140, 860, 64),
		tag(w0(36, 'peaceful'), s1(36), '“PEACEFUL”', 140, 180, 60, C.ink),
		tag(w0(37, 'plutonium'), s1(37), 'PLUTONIUM', 140, 860, 56, C.stress),
		tag(w0(41, 'halfway'), s1(41), 'ABANDONED HALFWAY', 140, 860, 56, C.stress),
		ask(w0(42, 'kishore') - 10, s1(42), 'WHAT HAPPENED TO IT?'),
		tag(w0(44, 'nineteen'), s1(44) + 20, '1981', 140, 180, 100, C.green, true),
	],
};

/** The kitchen cooker on the table under a warm lamp; the whistle lifts and steam bursts (stock steam, screened). */
const KitchenCooker: React.FC<{whistleAt: number; dur: number; small?: boolean}> = ({whistleAt, small}) => (
	<CookerScene whistleAt={whistleAt} small={small} />
);
const CookerScene: React.FC<{whistleAt: number; small?: boolean}> = ({whistleAt, small}) => {
	const f = useCurrentFrame();
	const lift = tw(f, whistleAt, whistleAt + 8, 0, 1) * tw(f, whistleAt + 40, whistleAt + 60, 1, 0.3);
	const steam = tw(f, whistleAt, whistleAt + 14, 0, 1);
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<g transform={`translate(${small ? 1420 : 860} ${small ? 700 : 560})`}>
					<Cooker whistle={lift} scale={small ? 0.9 : 1.7} />
				</g>
			</svg>
			{steam > 0 ? (
				<AbsoluteFill style={{opacity: 0.55 * steam, mixBlendMode: 'screen', maskImage: 'radial-gradient(ellipse 30% 45% at 50% 30%, black, transparent)'}}>
					<OffthreadVideo src={staticFile('assets/media/clips/STEAM.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</AbsoluteFill>
			) : null}
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 45% 40% at 50% 55%, rgba(255,190,110,0.18), transparent 70%)', mixBlendMode: 'screen'}} />
		</AbsoluteFill>
	);
};

/** The light over the empty dome drops as the Canadians leave (felt, S39). */
const LightDrop: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	return <AbsoluteFill style={{background: '#000', opacity: tw(f, 20, dur, 0, 0.45)}} />;
};

export const p1: Part = {shots: [...open.shots, ...ch1.shots], overlays: [...open.overlays, ...ch1.overlays]};
