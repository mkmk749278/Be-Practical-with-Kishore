import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {COUNTRIES} from '../../../../../lib/remotion/map/indiaGeo';
import {C, F} from '../theme';
import {CHAMBAL, RAJASTHAN} from './geo';
import {ez, tw, useSpring} from './kit';

// The film's drawings (word_map.md, "R" and "T" rows). Every one sits on the steel drafting table (Plate) and is
// labelled ILLUSTRATION or OUR CALCULATION by its shot. Frames are local to the shot.

const ink = C.ink;
const line = {fill: 'none', stroke: ink, strokeLinecap: 'round', strokeLinejoin: 'round'} as const;

// ---------------------------------------------------------------- the 306 face
/** 306 channel centres: the lattice points nearest the core centre on a half-offset square grid (as phwr_hero.py). */
export const LATTICE: [number, number][] = (() => {
	const pts: [number, number][] = [];
	for (let i = -12; i < 12; i++) {
		for (let j = -12; j < 12; j++) {
			pts.push([i + 0.5, j + 0.5]);
		}
	}
	return pts.sort((a, b) => Math.hypot(...a) - Math.hypot(...b) || a[0] - b[0] || a[1] - b[1]).slice(0, 306);
})();
// the order the count lights them: rows from the top, left to right (reads like counting)
const COUNT_ORDER = [...LATTICE].map((p, i) => ({p, i})).sort((a, b) => a.p[1] - b.p[1] || a.p[0] - b.p[0]);

/**
 * The reactor face from straight on: 306 end fittings in the end shield.
 * countA..countB: they light up row by row (the count lands on countB). greyAt: the right half greys out
 * (left half-built). relightAt: the grey half lights back. wornAt: one fitting near the centre dims (S2).
 */
export const Face306: React.FC<{
	pitch?: number;
	countA?: number;
	countB?: number;
	greyAt?: number;
	relightAt?: number;
	wornAt?: number;
	cx?: number;
	cy?: number;
}> = ({pitch = 40, countA, countB, greyAt, relightAt, wornAt, cx = 960, cy = 540}) => {
	const f = useCurrentFrame();
	const lit = countA !== undefined && countB !== undefined ? tw(f, countA, countB, 0, 306, ez.sweep) : 306;
	const grey = greyAt !== undefined ? tw(f, greyAt, greyAt + 40, 0, 1, ez.sweep) : 0;
	const back = relightAt !== undefined ? tw(f, relightAt, relightAt + 50, 0, 1, ez.sweep) : 0;
	const rank = new Map(COUNT_ORDER.map((o, k) => [o.i, k]));
	const R = pitch * 10.2;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<defs>
				<radialGradient id="shield" cx="50%" cy="45%" r="60%">
					<stop offset="0%" stopColor="#3a3f44" />
					<stop offset="100%" stopColor="#15181b" />
				</radialGradient>
				<radialGradient id="fit" cx="40%" cy="35%" r="70%">
					<stop offset="0%" stopColor="#d9dee3" />
					<stop offset="55%" stopColor="#7f8a94" />
					<stop offset="100%" stopColor="#2a3036" />
				</radialGradient>
			</defs>
			<circle cx={cx} cy={cy} r={R + 34} fill="#0e1013" stroke="#4a525a" strokeWidth={3} />
			<circle cx={cx} cy={cy} r={R + 14} fill="url(#shield)" stroke="#2c3238" strokeWidth={6} />
			{LATTICE.map(([x, y], i) => {
				const k = rank.get(i) ?? 0;
				const on = Math.max(0, Math.min(1, lit - k));
				const right = x > 0;
				const g = right ? grey * (1 - back) : 0;
				const worn = wornAt !== undefined && Math.abs(x + 0.5) < 0.01 && Math.abs(y + 0.5) < 0.01 ? tw(f, wornAt, wornAt + 30, 0, 1) : 0;
				const px = cx + x * pitch;
				const py = cy + y * pitch;
				return (
					<g key={i} opacity={0.25 + 0.75 * on}>
						<circle cx={px} cy={py} r={pitch * 0.4} fill="url(#fit)" opacity={1 - 0.75 * g} />
						<circle cx={px} cy={py} r={pitch * 0.2} fill="#0b0d0f" opacity={0.9} />
						{on > 0 && countA !== undefined ? <circle cx={px} cy={py} r={pitch * 0.42} fill="none" stroke={C.amber} strokeWidth={2.5} opacity={on * (1 - g)} /> : null}
						{g > 0 ? <circle cx={px} cy={py} r={pitch * 0.4} fill="#3b4046" opacity={0.85 * g} /> : null}
						{right && back > 0 ? <circle cx={px} cy={py} r={pitch * 0.42} fill="none" stroke={C.green} strokeWidth={3} opacity={back * (1 - 0.5 * tw(f, relightAt! + 60, relightAt! + 120, 0, 1))} /> : null}
						{worn > 0 ? (
							<g opacity={worn}>
								<circle cx={px} cy={py} r={pitch * 0.9} fill={C.stress} opacity={0.18} style={{filter: 'blur(6px)'}} />
								<circle cx={px} cy={py} r={pitch * 0.48} fill="#3b4046" stroke={C.stress} strokeWidth={5} />
								<path d={`M${px - pitch * 0.3} ${py - pitch * 0.1}l${pitch * 0.18} ${pitch * 0.08}l${pitch * 0.12} -${pitch * 0.06}l${pitch * 0.18} ${pitch * 0.1}`} stroke={C.stress} strokeWidth={2} fill="none" />
							</g>
						) : null}
					</g>
				);
			})}
		</svg>
	);
};

// ---------------------------------------------------------------- maps (official India boundary, Natural Earth)
type Cam = {x: number; y: number; z: number};
const camAt = (f: number, a: Cam, b: Cam, f0: number, f1: number): Cam => {
	const k = tw(f, f0, f1, 0, 1, ez.cam);
	return {x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, z: Math.exp(Math.log(a.z) + (Math.log(b.z) - Math.log(a.z)) * k)};
};
/** lon/lat → map units, the same projection as lib/remotion/map (Lambert azimuthal equal-area at 80E 22N, 3 km a unit) */
export const proj = (lon: number, lat: number): [number, number] => {
	const r = Math.PI / 180;
	const l = (lon - 80) * r;
	const p = lat * r;
	const p0 = 22 * r;
	const k = Math.sqrt(2 / (1 + Math.sin(p0) * Math.sin(p) + Math.cos(p0) * Math.cos(p) * Math.cos(l)));
	return [(6371 * k * Math.cos(p) * Math.sin(l)) / 3, (-6371 * k * (Math.cos(p0) * Math.sin(p) - Math.sin(p0) * Math.cos(p) * Math.cos(l))) / 3];
};
export const RAWATBHATA = proj(75.59, 24.93);
export const KOTA = proj(75.83, 25.18);

const MapPin: React.FC<{at: [number, number]; z: number; from: number; label: string; sub?: string; side?: 'left' | 'right'; color?: string}> = ({at, z, from, label, sub, side = 'right', color = C.flask}) => {
	const f = useCurrentFrame();
	const p = useSpring(from, 170, 14);
	if (f < from) {
		return null;
	}
	const s = 1 / z;
	const ring = ((f - from) % 90) / 90;
	const dx = side === 'left' ? -30 : 30;
	return (
		<g transform={`translate(${at[0]} ${at[1]}) scale(${s})`}>
			<circle r={10 + ring * 40} fill="none" stroke={color} strokeWidth={3} opacity={(1 - ring) * 0.7} />
			<circle r={10 * p} fill={color} stroke="#0b0d0f" strokeWidth={3} />
			<g opacity={p} transform={`translate(${dx} 14)`}>
				<text textAnchor={side === 'left' ? 'end' : 'start'} fontFamily={F.label} fontWeight={800} fontSize={50} fill={ink} stroke="#0b0d0f" strokeWidth={8} paintOrder="stroke" letterSpacing={2}>
					{label}
				</text>
				{sub ? (
					<text y={46} textAnchor={side === 'left' ? 'end' : 'start'} fontFamily={F.label} fontWeight={700} fontSize={34} fill={C.dim} stroke="#0b0d0f" strokeWidth={7} paintOrder="stroke" letterSpacing={1}>
						{sub}
					</text>
				) : null}
			</g>
		</g>
	);
};

/**
 * India (official boundary) → Rajasthan lit → the Chambal drawn on → Rawatbhata pinned (S0), or the Kota road (S11).
 * mode 'chambal': rajAt (Rajasthan lights), riverA..riverB (the river draws), pinAt.
 * mode 'kota': pinAt (Kota), roadA..roadB (the road draws at road speed), kmAt (64 KM).
 */
export const RajMap: React.FC<{dur: number; mode: 'chambal' | 'kota'; rajAt?: number; riverA?: number; riverB?: number; pinAt?: number; roadA?: number; roadB?: number; kmAt?: number}> = ({
	dur,
	mode,
	rajAt = 0,
	riverA = 0,
	riverB = 1,
	pinAt = 0,
	roadA = 0,
	roadB = 1,
	kmAt = 0,
}) => {
	const f = useCurrentFrame();
	const wide: Cam = {x: 20, y: -60, z: 0.95};
	const raj: Cam = {x: RAWATBHATA[0] - 20, y: RAWATBHATA[1] - 40, z: 2.6};
	const close: Cam = {x: (RAWATBHATA[0] + KOTA[0]) / 2, y: (RAWATBHATA[1] + KOTA[1]) / 2, z: 28};
	const cam = mode === 'chambal' ? camAt(f, wide, raj, 0, Math.max(30, dur - 10)) : camAt(f, {...close, z: 14}, close, 0, dur);
	const tf = `translate(960 540) scale(${cam.z}) translate(${-cam.x} ${-cam.y})`;
	const rajOn = mode === 'kota' ? 1 : tw(f, rajAt, rajAt + 24, 0, 1, ez.arrive);
	const river = mode === 'kota' ? 1 : tw(f, riverA, riverB, 0, 1, ez.sweep);
	const road = tw(f, roadA, roadB, 0, 1, ez.sweep);
	const sw = 1 / cam.z;
	return (
		<AbsoluteFill style={{background: '#0b0f13'}}>
			<svg width={1920} height={1080}>
				<g transform={tf}>
					{Object.entries(COUNTRIES)
						.filter(([k]) => k !== 'IND')
						.map(([k, ds]) => ds.map((d, i) => <path key={k + i} d={d} fill="#1a1f24" stroke="#2e353c" strokeWidth={1.2 * sw} />))}
					{COUNTRIES.IND.map((d, i) => (
						<path key={i} d={d} fill="#3a3226" stroke={C.sand} strokeWidth={2.2 * sw} />
					))}
					<path d={RAJASTHAN} fill={C.sand} fillOpacity={0.35 * rajOn} stroke={C.flask} strokeOpacity={rajOn} strokeWidth={3 * sw} />
					<path d={CHAMBAL} fill="none" stroke={C.water} strokeWidth={4 * sw} strokeLinecap="round" pathLength={1} strokeDasharray={`${river} 1`} />
					{mode === 'kota' ? (
						<path
							d={`M${KOTA[0]} ${KOTA[1]}Q${(KOTA[0] + RAWATBHATA[0]) / 2 + 6} ${(KOTA[1] + RAWATBHATA[1]) / 2 + 4} ${RAWATBHATA[0]} ${RAWATBHATA[1]}`}
							fill="none"
							stroke={C.flask}
							strokeWidth={5 * sw}
							strokeDasharray={`${road} 1`}
							pathLength={1}
						/>
					) : null}
					{mode === 'chambal' ? (
						<MapPin at={RAWATBHATA} z={cam.z} from={pinAt} label="RAWATBHATA" sub="CHAMBAL RIVER · RAJASTHAN" side="left" />
					) : (
						<>
							<MapPin at={KOTA} z={cam.z} from={0} label="KOTA" side="right" color={C.dim} />
							<MapPin at={RAWATBHATA} z={cam.z} from={roadB} label="RAWATBHATA" side="left" />
						</>
					)}
				</g>
			</svg>
			{mode === 'kota' && f >= kmAt ? (
				<div style={{position: 'absolute', left: 960, top: 190, transform: `translateX(-50%) scale(${0.9 + 0.1 * tw(f, kmAt, kmAt + 14, 0, 1, ez.arrive)})`, opacity: tw(f, kmAt, kmAt + 12, 0, 1), fontFamily: F.mono, fontWeight: 700, fontSize: 92, color: C.flask, textShadow: '0 4px 24px rgba(0,0,0,0.9)'}}>
					64 KM
				</div>
			) : null}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the export file (S6, S38)
/** A buff file on the table, "CANADA · NUCLEAR EXPORTS"; a stamp lands on stampAt; the cover shuts on closeAt. */
export const ExportFile: React.FC<{stampAt?: number; closeAt?: number}> = ({stampAt, closeAt}) => {
	const f = useCurrentFrame();
	const st = useSpring(stampAt ?? 1e9, 260, 16);
	const shut = closeAt !== undefined ? tw(f, closeAt, closeAt + 26, 0, 1, ez.sweep) : 0;
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'relative', width: 980, height: 680, transform: 'translate(120px, 40px) rotate(-4deg)', perspective: 2000}}>
				{/* the sheet inside */}
				<div style={{position: 'absolute', inset: 0, background: C.paper, boxShadow: '0 40px 90px rgba(0,0,0,0.7)', padding: '70px 80px', fontFamily: F.label, color: C.pencil}}>
					<div style={{fontWeight: 800, fontSize: 52, letterSpacing: 4}}>CANADA</div>
					<div style={{fontWeight: 700, fontSize: 40, letterSpacing: 2, marginTop: 8, color: '#5a6470'}}>NUCLEAR EXPORTS · INDIA</div>
					<div style={{marginTop: 60, display: 'flex', flexDirection: 'column', gap: 26}}>
						{[0.92, 0.8, 0.86, 0.6].map((w, i) => (
							<div key={i} style={{height: 14, width: `${w * 100}%`, background: '#b9b1a0', borderRadius: 3}} />
						))}
					</div>
					{stampAt !== undefined && f >= stampAt ? (
						<div
							style={{
								position: 'absolute',
								right: 90,
								bottom: 110,
								transform: `rotate(-10deg) scale(${1.7 - 0.7 * st})`,
								opacity: st,
								border: `9px solid ${C.fail}`,
								color: C.fail,
								padding: '12px 30px',
								fontWeight: 800,
								fontSize: 66,
								letterSpacing: 6,
								whiteSpace: 'nowrap',
							}}
						>
							NOT PERMITTED
						</div>
					) : null}
				</div>
				{/* the cover swings shut over it */}
				<div
					style={{
						position: 'absolute',
						inset: 0,
						background: '#c8a875',
						transformOrigin: '0% 50%',
						transform: `rotateY(${-178 + 178 * shut}deg)`,
						backfaceVisibility: 'hidden',
						boxShadow: '0 30px 70px rgba(0,0,0,0.6)',
						opacity: shut > 0.02 ? 1 : 0,
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						fontFamily: F.label,
						fontWeight: 800,
						fontSize: 60,
						color: '#5a4426',
						letterSpacing: 6,
					}}
				>
					CLOSED · 1974
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the design sheet (S13, S14)
/** A drawing sheet slides onto the table at 12°: the reactor's elevation, the title block "DESIGN · CANADA". */
export const DesignSheet: React.FC<{lampAt?: number}> = ({lampAt}) => {
	const f = useCurrentFrame();
	const slide = tw(f, 0, 40, 1, 0, ez.arrive);
	const draw = tw(f, 10, 110, 0, 1, ez.sweep);
	const lamp = lampAt !== undefined ? tw(f, lampAt, lampAt + 40, 0, 1) : 0;
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'relative', width: 1300, height: 860, transform: `translate(${slide * 900}px, ${slide * 120}px) rotate(${-12 + 0 * slide}deg)`, background: '#dfe6ea', boxShadow: '0 50px 100px rgba(0,0,0,0.7)'}}>
				<svg width={1300} height={860} style={{position: 'absolute'}}>
					<rect x={30} y={30} width={1240} height={800} fill="none" stroke="#2e4a66" strokeWidth={3} />
					{/* the calandria in section: a drum lying on its side, tubes running through it */}
					<g stroke="#2e4a66" strokeWidth={3} fill="none" pathLength={1} strokeDasharray={`${draw} 1`}>
						<rect x={330} y={190} width={640} height={380} rx={40} pathLength={1} />
						<rect x={290} y={170} width={40} height={420} pathLength={1} />
						<rect x={970} y={170} width={40} height={420} pathLength={1} />
						{Array.from({length: 13}, (_, i) => (
							<path key={i} d={`M230 ${210 + i * 27}H1070`} pathLength={1} strokeWidth={2} />
						))}
						<path d="M650 570V690M560 690H740" pathLength={1} />
					</g>
					<g opacity={tw(f, 70, 100, 0, 1)}>
						<rect x={880} y={700} width={360} height={110} fill="#dfe6ea" stroke="#2e4a66" strokeWidth={3} />
						<text x={900} y={748} fontFamily={F.label} fontWeight={800} fontSize={40} fill="#1d3550" letterSpacing={3}>DESIGN · CANADA</text>
						<text x={900} y={790} fontFamily={F.label} fontWeight={700} fontSize={28} fill="#3e5a76" letterSpacing={2}>RAJASTHAN UNIT 1</text>
					</g>
				</svg>
			</div>
			<AbsoluteFill style={{background: `radial-gradient(ellipse 55% 50% at 55% 45%, rgba(255,190,110,${0.22 * lamp}), transparent 70%)`, mixBlendMode: 'screen'}} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- pot → tank → 306 tubes → cooker (S19–S23)
/**
 * potA: one giant steel pot draws on; dissolveAt: it fades; tankAt: a tank on its side; pierceA..pierceB: the tubes
 * slide through it; liftAt: one tube rises out of the row and turns into a pressure cooker (cookerAt).
 */
export const PotTank: React.FC<{dissolveAt: number; tankAt: number; pierceA: number; pierceB: number; liftAt: number; cookerAt: number}> = ({dissolveAt, tankAt, pierceA, pierceB, liftAt, cookerAt}) => {
	const f = useCurrentFrame();
	const pot = tw(f, 0, 50, 0, 1, ez.sweep) * tw(f, dissolveAt, dissolveAt + 30, 1, 0);
	const spin = Math.sin(f / 70) * 0.06;
	const tank = tw(f, tankAt, tankAt + 30, 0, 1);
	const pierce = tw(f, pierceA, pierceB, 0, 1, ez.sweep);
	const lift = tw(f, liftAt, liftAt + 40, 0, 1, ez.cam);
	const cook = tw(f, cookerAt, cookerAt + 30, 0, 1, ez.sweep);
	const rows = 9;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{/* the pot: a pressure vessel, drawn in steel */}
			<g opacity={pot} transform={`translate(960 560) scale(${1 + spin * 0.4} 1)`}>
				<path d="M-230 -260Q-230 -330 0 -340Q230 -330 230 -260V250Q230 330 0 340Q-230 330 -230 250Z" fill="#5a646d" stroke="#c9d2da" strokeWidth={6} />
				<path d="M-230 -200H230M-230 200H230" stroke={C.steel} strokeWidth={3} opacity={0.6} />
				<ellipse cx={-90 + spin * 600} cy={0} rx={40} ry={280} fill="#ffffff" opacity={0.05} />
			</g>
			{/* the tank on its side, tubes through it */}
			<g opacity={tank * (1 - 0.85 * cook)} transform={`translate(960 ${640 + 0 * lift})`}>
				<rect x={-380} y={-250} width={760} height={500} rx={60} fill="#1d3a4a" fillOpacity={0.45} stroke={C.steel} strokeWidth={5} />
				<rect x={-430} y={-280} width={50} height={560} fill="#2a3036" stroke={C.steel} strokeWidth={3} />
				<rect x={380} y={-280} width={50} height={560} fill="#2a3036" stroke={C.steel} strokeWidth={3} />
				{Array.from({length: rows}, (_, i) => {
					const y = -210 + i * 52.5;
					const lifted = i === 4;
					const dy = lifted ? -lift * 470 : 0;
					const len = 980 * pierce;
					return (
						<g key={i} transform={`translate(0 ${dy})`} opacity={lifted ? 1 - cook : 1}>
							<rect x={-490} y={y - 9} width={len} height={18} rx={9} fill={lifted && lift > 0 ? C.flask : '#9aa5ae'} stroke="#0b0d0f" strokeWidth={2} />
						</g>
					);
				})}
			</g>
			{/* the cooker the lifted tube becomes */}
			<g opacity={cook} transform={`translate(960 ${300 - 40 * cook}) scale(${1.0 + 0.3 * cook})`}>
				<Cooker whistle={0} />
			</g>
		</svg>
	);
};

/** A home pressure cooker on its side view: body, lid, handle and the whistle (lift 0..1 raises the weight). */
export const Cooker: React.FC<{whistle: number; scale?: number}> = ({whistle, scale = 1}) => (
	<g transform={`scale(${scale})`}>
		<path d="M-190 -40H190V120Q190 170 140 170H-140Q-190 170 -190 120Z" fill="#b9c2c9" stroke="#0b0d0f" strokeWidth={4} />
		<path d="M-200 -40Q0 -90 200 -40Z" fill="#9aa5ae" stroke="#0b0d0f" strokeWidth={4} />
		<rect x={190} y={-70} width={230} height={34} rx={14} fill="#1b1d20" stroke="#0b0d0f" strokeWidth={3} />
		<g transform={`translate(0 ${-78 - whistle * 26})`}>
			<rect x={-10} y={-10} width={20} height={24} fill="#4b5258" />
			<path d="M-24 -10H24L16 -40H-16Z" fill="#2a3036" stroke="#0b0d0f" strokeWidth={3} />
		</g>
	</g>
);

// ---------------------------------------------------------------- the weights (S26, S28)
/** One kilo on a fingertip square (one square centimetre), then a hundred stacked on it, and 310 °C. */
export const Weights: React.FC<{oneAt: number; stackA?: number; stackB?: number; tempAt?: number}> = ({oneAt, stackA, stackB, tempAt}) => {
	const f = useCurrentFrame();
	const one = useSpring(oneAt, 180, 16);
	const n = stackA !== undefined && stackB !== undefined ? Math.round(tw(f, stackA, stackB, 1, 100, ez.sweep)) : 1;
	const t = tempAt !== undefined ? tw(f, tempAt, tempAt + 40, 0, 1) : 0;
	const cols = 10;
	return (
		<AbsoluteFill>
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				{/* the square centimetre, a fingertip's size, drawn on the table */}
				<rect x={900} y={870} width={120} height={120} fill="none" stroke={C.flask} strokeWidth={5} strokeDasharray="12 8" />
				<text x={1040} y={950} fontFamily={F.label} fontWeight={800} fontSize={44} fill={C.flask}>1 CM²</text>
				{Array.from({length: n}, (_, i) => {
					const col = i % cols;
					const row = Math.floor(i / cols);
					const big = n === 1 ? 2.6 : 1;
					const x = 960 + (col - (Math.min(n, cols) - 1) / 2) * 62;
					const y = 860 - row * 70;
					return (
						<g key={i} transform={`translate(${x} ${y - (i === 0 ? (1 - one) * 300 : 0)}) scale(${big})`} opacity={i === 0 ? one : 1}>
							<path d="M-28 0H28L22 -52H-22Z" fill="#3b4147" stroke="#0b0d0f" strokeWidth={3} />
							<rect x={-10} y={-64} width={20} height={14} rx={4} fill="#3b4147" stroke="#0b0d0f" strokeWidth={2} />
							{n === 1 ? <text y={-18} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={18} fill={ink}>1 KG</text> : null}
						</g>
					);
				})}
			</svg>
			{stackA !== undefined && f >= stackA ? (
				<div style={{position: 'absolute', left: 140, top: 180, fontFamily: F.mono, fontWeight: 700, fontSize: 110, color: C.amber, textShadow: '0 4px 24px rgba(0,0,0,0.9)'}}>
					{n}×
				</div>
			) : null}
			{t > 0 ? (
				<div style={{position: 'absolute', right: 160, top: 180, opacity: t, fontFamily: F.mono, fontWeight: 700, fontSize: 110, color: C.stress, textShadow: `0 0 ${40 * t}px rgba(240,136,62,0.6)`}}>
					310 °C
				</div>
			) : null}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the tube wall and the pencil (S29–S31)
/** The pressure tube in section (103 mm across, 4.2 mm wall, to scale), then a pencil laid beside the wall. */
export const TubeWall: React.FC<{pencilAt: number; compareAt: number}> = ({pencilAt, compareAt}) => {
	const f = useCurrentFrame();
	const mm = 7.2; // px per mm
	const r = 51.5 * mm;
	const wall = 4.2 * mm;
	const ring = tw(f, 0, 40, 0, 1, ez.sweep);
	const pen = useSpring(pencilAt, 120, 18);
	const cmp = tw(f, compareAt, compareAt + 40, 0, 1, ez.cam);
	// the pencil: 7 mm across, it slides from the side until it lies along the wall's edge
	const px = 960 + r + 3.5 * mm + 160 - cmp * 154;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<circle cx={960} cy={540} r={r - wall / 2} fill="none" stroke={C.flask} strokeWidth={wall} pathLength={1} strokeDasharray={`${ring} 1`} />
			<circle cx={960} cy={540} r={r - wall} fill="#1d3a4a" fillOpacity={0.25} />
			<text x={960} y={620} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={48} fill={ink} opacity={ring}>
				WALL ≈ 4 MM
			</text>
			<g opacity={pen} transform={`translate(${px} ${540 + (1 - pen) * 300})`}>
				<rect x={-3.5 * mm} y={-260} width={7 * mm} height={460} fill="#e8b331" stroke="#0b0d0f" strokeWidth={3} />
				<path d={`M${-3.5 * mm} 200L0 260L${3.5 * mm} 200Z`} fill="#e9d1a8" stroke="#0b0d0f" strokeWidth={3} />
				<path d={`M${-1.2 * mm} 245L0 260L${1.2 * mm} 245Z`} fill="#222" />
				<rect x={-3.5 * mm} y={-290} width={7 * mm} height={30} fill="#c0c6cb" stroke="#0b0d0f" strokeWidth={3} />
			</g>
			{cmp > 0.6 ? (
				<g opacity={tw(f, compareAt + 24, compareAt + 40, 0, 1)}>
					<path d={`M${960 + r - wall} 470H${960 + r + 7 * mm + 6}`} stroke={C.stress} strokeWidth={4} />
					<text x={960 + r - wall - 24} y={484} textAnchor="end" fontFamily={F.label} fontWeight={800} fontSize={48} fill={C.stress} stroke="#0b0d0f" strokeWidth={6} paintOrder="stroke">THINNER THAN A PENCIL</text>
				</g>
			) : null}
		</svg>
	);
};

// ---------------------------------------------------------------- the calendar page (S32, S33)
export const MayPage: React.FC = () => {
	const p = useSpring(0, 150, 16);
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{width: 640, height: 720, background: C.paper, transform: `rotate(${3 - 2 * tw(f, 0, 200, 0, 1)}deg) translateY(${(1 - p) * -500}px)`, boxShadow: '0 40px 90px rgba(0,0,0,0.7)', display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: F.label, color: C.pencil}}>
				<div style={{width: '100%', height: 70, background: '#8c2f24'}} />
				<div style={{fontWeight: 800, fontSize: 150, marginTop: 50, letterSpacing: 10}}>MAY</div>
				<div style={{fontWeight: 800, fontSize: 130, color: '#8c2f24'}}>1974</div>
			</div>
		</AbsoluteFill>
	);
};

/** Seeded scatter for small marks (dust on the table, not data). */
export const seeded = (seed: string, n: number): number[] => Array.from({length: n}, (_, i) => random(`${seed}-${i}`));
export {line};
