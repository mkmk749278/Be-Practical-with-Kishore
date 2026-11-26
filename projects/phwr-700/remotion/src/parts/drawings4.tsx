import React from 'react';
import {AbsoluteFill, Img, random, staticFile, useCurrentFrame} from 'remotion';
import {COUNTRIES} from '../../../../../lib/remotion/map/indiaGeo';
import {C, F} from '../theme';
import {proj} from './drawings';
import {ez, tw, useSpring} from './kit';

// Chapters 4–5 and the landing (word_map.md S122–S189). Every drawing sits on the table; frames are local.
const ink = C.ink;
const lab = (x: number, y: number, text: string, color: string, o: number, size = 46, anchor: 'start' | 'middle' | 'end' = 'start') => (
	<text x={x} y={y} textAnchor={anchor} fontFamily={F.label} fontWeight={800} fontSize={size} fill={color} opacity={o} stroke="#0b0d0f" strokeWidth={7} paintOrder="stroke" letterSpacing={1}>
		{text}
	</text>
);

// ---------------------------------------------------------------- India with pins (official boundary)
export const SITES = {
	kakrapar: proj(73.35, 21.24),
	rawatbhata: proj(75.59, 24.93),
	tarapur: proj(72.66, 19.83),
	narora: proj(78.41, 28.16),
	kaiga: proj(74.44, 14.86),
	kalpakkam: proj(80.17, 12.56),
};
const CITIES: [number, number][] = [
	[77.21, 28.61], [72.88, 19.08], [88.36, 22.57], [80.27, 13.08], [77.59, 12.97], [78.49, 17.39], [72.58, 23.03], [73.86, 18.52], [75.79, 26.91], [80.95, 26.85],
	[85.14, 25.59], [75.86, 22.72], [76.27, 9.93], [83.22, 17.69], [79.09, 21.15], [77.41, 23.26], [91.74, 26.14], [85.82, 20.3], [74.87, 31.63], [78.01, 27.18],
];

/** mode 'kakrapar': India, Gujarat's pin (S127). 'fleet': the PHWR sites calm, Kakrapar's two dots marked (S140).
 *  'lights': India at dusk, the cities' lights come on (S184). */
export const IndiaPins: React.FC<{dur: number; mode: 'kakrapar' | 'fleet' | 'lights'; at?: number}> = ({dur, mode, at = 0}) => {
	const f = useCurrentFrame();
	const z0 = mode === 'kakrapar' ? 0.95 : 0.9;
	const z1 = mode === 'kakrapar' ? 2.2 : 1.0;
	const c0 = {x: 20, y: -40};
	const c1 = mode === 'kakrapar' ? {x: SITES.kakrapar[0] + 40, y: SITES.kakrapar[1]} : {x: 20, y: -20};
	const k = tw(f, 0, dur, 0, 1, ez.cam);
	const z = Math.exp(Math.log(z0) + (Math.log(z1) - Math.log(z0)) * k);
	const cx = c0.x + (c1.x - c0.x) * k;
	const cy = c0.y + (c1.y - c0.y) * k;
	const sw = 1 / z;
	const pin = (p: [number, number], color: string, from: number, label?: string, side: 'left' | 'right' = 'right') => {
		const s = tw(f, from, from + 14, 0, 1, ez.arrive);
		return (
			<g transform={`translate(${p[0]} ${p[1]}) scale(${sw})`} opacity={s}>
				<circle r={14 * s} fill={color} stroke="#0b0d0f" strokeWidth={3} />
				{label ? (
					<text x={side === 'right' ? 26 : -26} y={14} textAnchor={side === 'right' ? 'start' : 'end'} fontFamily={F.label} fontWeight={800} fontSize={46} fill={ink} stroke="#0b0d0f" strokeWidth={8} paintOrder="stroke">
						{label}
					</text>
				) : null}
			</g>
		);
	};
	const night = mode === 'lights' ? tw(f, 0, 40, 0, 1) : 0;
	return (
		<AbsoluteFill style={{background: '#0b0f13'}}>
			<svg width={1920} height={1080}>
				<g transform={`translate(960 540) scale(${z}) translate(${-cx} ${-cy})`}>
					{Object.entries(COUNTRIES)
						.filter(([c]) => c !== 'IND')
						.map(([c, ds]) => ds.map((d, i) => <path key={c + i} d={d} fill="#1a1f24" stroke="#2e353c" strokeWidth={1.2 * sw} />))}
					{COUNTRIES.IND.map((d, i) => (
						<path key={i} d={d} fill={mode === 'lights' ? `rgb(${58 - 40 * night},${50 - 34 * night},${38 - 26 * night})` : '#3a3226'} stroke={C.sand} strokeWidth={2.2 * sw} />
					))}
					{mode === 'kakrapar' ? pin(SITES.kakrapar, C.stress, at, 'KAKRAPAR · GUJARAT') : null}
					{mode === 'fleet'
						? (
								<>
									{(['rawatbhata', 'tarapur', 'narora', 'kaiga', 'kalpakkam'] as const).map((s, i) => (
										<g key={s}>{pin(SITES[s], C.green, 6 + i * 6)}</g>
									))}
									{pin(SITES.kakrapar, C.stress, at, 'KAKRAPAR 1 & 2', 'left')}
								</>
							)
						: null}
					{mode === 'lights'
						? CITIES.map(([lo, la], i) => {
								const p = proj(lo, la);
								const on = tw(f, at + i * 5, at + i * 5 + 16, 0, 1);
								const flick = 0.85 + 0.15 * Math.sin(f / 7 + i);
								return <circle key={i} cx={p[0]} cy={p[1]} r={(10 + 8 * on) * sw} fill="#ffcf6a" opacity={on * flick} style={{filter: 'blur(1.5px)'}} />;
							})
						: null}
				</g>
			</svg>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the reactor shuts itself down: rods drop (S129, SIMPLIFIED)
export const RodsDrop: React.FC<{dropAt: number}> = ({dropAt}) => {
	const f = useCurrentFrame();
	const d = tw(f, dropAt, dropAt + 16, 0, 1, (t) => t * t);
	const glow = 1 - tw(f, dropAt + 10, dropAt + 70, 0, 1);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={560} y={420} width={800} height={420} rx={60} fill="#1d3a4a" stroke={C.steel} strokeWidth={6} />
			<rect x={600} y={460} width={720} height={340} rx={40} fill={C.amber} opacity={0.25 + 0.45 * glow} />
			{[700, 860, 1060, 1220].map((x) => (
				<rect key={x} x={x - 16} y={160 + 330 * d} width={32} height={300} fill="#2a3036" stroke="#0b0d0f" strokeWidth={3} />
			))}
			{lab(960, 120, 'SHUTDOWN RODS', ink, 1, 48, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- the international scale: 2 out of 7 (S133–S134)
export const InesScale: React.FC<{litAt: number}> = ({litAt}) => {
	const f = useCurrentFrame();
	const build = tw(f, 0, 40, 0, 1, ez.sweep);
	const lit = tw(f, litAt, litAt + 20, 0, 1, ez.arrive);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{Array.from({length: 8}, (_, i) => {
				const h = 60 + i * 60;
				const on = i === 2 ? lit : 0;
				return (
					<g key={i} opacity={tw(f, i * 4, i * 4 + 12, 0, 1)}>
						<rect x={360 + i * 160} y={880 - h * build} width={120} height={h * build} fill={on ? C.flask : i <= 3 ? '#3b4147' : '#4a2d2a'} stroke="#0b0d0f" strokeWidth={3} />
						<text x={420 + i * 160} y={940} textAnchor="middle" fontFamily={F.mono} fontWeight={700} fontSize={46} fill={on ? C.flask : C.dim}>
							{i}
						</text>
					</g>
				);
			})}
			{lab(420 + 2 * 160, 880 - 180 - 30, 'INCIDENT', C.flask, lit, 46, 'middle')}
			{lab(420 + 6 * 160, 880 - 420 - 30, 'ACCIDENTS', C.dim, build, 38, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- small spots eaten into the outer wall (S136–S137)
export const PittedWall: React.FC<{pitA: number; pitB: number}> = ({pitA, pitB}) => {
	const f = useCurrentFrame();
	const k = tw(f, pitA, pitB, 0, 1, (t) => t);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={240} y={380} width={1440} height={320} rx={30} fill="#7f8a94" stroke="#0b0d0f" strokeWidth={4} />
			<rect x={240} y={380} width={1440} height={60} fill="#9aa5ae" opacity={0.6} />
			{Array.from({length: 40}, (_, i) => {
				const t = random(`pt${i}`);
				if (k < t) {
					return null;
				}
				const r = 6 + 16 * random(`pr${i}`) * Math.min(1, (k - t) * 4);
				return <circle key={i} cx={280 + random(`px${i}`) * 1360} cy={400 + random(`py${i}`) * 280} r={r} fill="#3b2a1d" stroke="#0b0d0f" strokeWidth={2} />;
			})}
			{lab(240, 340, 'THE TUBE’S OUTER WALL', ink, 1)}
		</svg>
	);
};

// ---------------------------------------------------------------- 306 grows to 392 (S147–S148)
const lattice = (n: number): [number, number][] => {
	const pts: [number, number][] = [];
	for (let i = -13; i < 13; i++) {
		for (let j = -13; j < 13; j++) {
			pts.push([i + 0.5, j + 0.5]);
		}
	}
	return pts.sort((a, b) => Math.hypot(...a) - Math.hypot(...b) || a[0] - b[0] || a[1] - b[1]).slice(0, n);
};
const L392 = lattice(392);
export const FaceGrow: React.FC<{growA: number; growB: number}> = ({growA, growB}) => {
	const f = useCurrentFrame();
	const n = tw(f, growA, growB, 306, 392, ez.sweep);
	const pitch = 36;
	const R = pitch * (10.2 + 1.3 * tw(f, growA, growB, 0, 1, ez.sweep));
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<circle cx={960} cy={540} r={R + 30} fill="#15181b" stroke="#4a525a" strokeWidth={4} />
			{L392.map(([x, y], i) => {
				const on = Math.max(0, Math.min(1, n - i));
				const isNew = i >= 306;
				return <circle key={i} cx={960 + x * pitch} cy={540 + y * pitch} r={pitch * 0.38} fill={isNew ? C.flask : '#9aa5ae'} opacity={isNew ? on : 1} stroke="#0b0d0f" strokeWidth={2} />;
			})}
		</svg>
	);
};

// ---------------------------------------------------------------- the dry gas, the drop, the damp, the alarm (S150–S153)
export const GasAlarm: React.FC<{dropAt: number; alarmAt: number}> = ({dropAt, alarmAt}) => {
	const f = useCurrentFrame();
	const damp = tw(f, dropAt + 10, dropAt + 60, 0, 1);
	const alarm = f >= alarmAt ? 0.5 + 0.5 * Math.sin(((f - alarmAt) / 12) * Math.PI) : 0;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={200} y={360} width={1520} height={360} rx={40} fill="#5d6a75" stroke="#0b0d0f" strokeWidth={4} />
			<rect x={230} y={390} width={1460} height={300} rx={30} fill="#16222a" />
			<rect x={200} y={470} width={1520} height={140} rx={20} fill="url(#hotG)" stroke="#0b0d0f" strokeWidth={3} />
			<defs>
				<linearGradient id="hotG" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#f6b24a" />
					<stop offset="1" stopColor="#c96a1a" />
				</linearGradient>
			</defs>
			{/* gas flowing in the gap */}
			{Array.from({length: 36}, (_, i) => {
				const x = 240 + ((random(`g${i}`) * 1440 + f * 3) % 1440);
				const top = i % 2 === 0;
				const y = top ? 410 + random(`gy${i}`) * 50 : 630 + random(`gy${i}`) * 50;
				return <circle key={i} cx={x} cy={y} r={6} fill={damp > 0.5 ? '#9fd3ff' : '#c9d2d9'} opacity={0.7} />;
			})}
			{/* the drop that leaks in */}
			{f >= dropAt ? <circle cx={960} cy={tw(f, dropAt, dropAt + 20, 612, 660)} r={14} fill={C.water} /> : null}
			{/* dew on the walls */}
			{Array.from({length: 30}, (_, i) =>
				damp > random(`dw${i}`) ? <ellipse key={i} cx={260 + random(`dx${i}`) * 1400} cy={random(`dt${i}`) < 0.5 ? 396 : 684} rx={6} ry={8} fill="#e9f4ff" opacity={0.8} /> : null,
			)}
			{/* the alarm lamp */}
			<circle cx={1680} cy={230} r={50} fill={C.fail} opacity={0.2 + 0.8 * alarm} />
			<circle cx={1680} cy={230} r={120} fill={C.fail} opacity={0.25 * alarm} style={{filter: 'blur(20px)'}} />
			{lab(240, 330, 'DRY GAS AROUND THE TUBE', '#c9d2d9', 1 - damp, 44)}
			{lab(240, 330, 'DAMP', C.water, damp, 52)}
			{lab(1580, 245, 'ALARM', C.fail, f >= alarmAt ? 1 : 0, 52, 'end')}
		</svg>
	);
};

// ---------------------------------------------------------------- 3 out of every 100 units (S164)
export const HundredBulbs: React.FC<{litAt: number}> = ({litAt}) => {
	const f = useCurrentFrame();
	const lit = tw(f, litAt, litAt + 24, 0, 1, ez.arrive);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{Array.from({length: 100}, (_, i) => {
				const x = 560 + (i % 10) * 84;
				const y = 170 + Math.floor(i / 10) * 74;
				const on = i < 3 ? lit : 0;
				const show = tw(f, i * 0.6, i * 0.6 + 10, 0, 1);
				return (
					<g key={i} opacity={show}>
						<circle cx={x} cy={y} r={24} fill={on ? '#ffd76a' : '#2a3036'} stroke="#0b0d0f" strokeWidth={2} />
						{on ? <circle cx={x} cy={y} r={44} fill="#ffcf6a" opacity={0.3 * on} style={{filter: 'blur(8px)'}} /> : null}
					</g>
				);
			})}
			{lab(1420, 230, '3 IN 100', C.flask, lit, 72)}
			{lab(1420, 290, 'FROM NUCLEAR', ink, lit, 40)}
		</svg>
	);
};

// ---------------------------------------------------------------- 2010 first concrete → 2020 critical (S167–S168)
export const TenYears: React.FC<{aAt: number; bAt: number}> = ({aAt, bAt}) => {
	const f = useCurrentFrame();
	const a = tw(f, aAt, aAt + 20, 0, 1, ez.arrive);
	const run = tw(f, bAt - 40, bAt, 0, 1, ez.sweep);
	const x = (y: number) => 300 + ((y - 2010) / 10) * 1320;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<path d={`M${x(2010)} 560H${x(2020)}`} stroke="#3b4147" strokeWidth={16} strokeLinecap="round" />
			<path d={`M${x(2010)} 560H${x(2010) + 1320 * run}`} stroke={C.stress} strokeWidth={16} strokeLinecap="round" opacity={a} />
			{Array.from({length: 11}, (_, i) => (
				<text key={i} x={x(2010 + i)} y={640} textAnchor="middle" fontFamily={F.mono} fontWeight={700} fontSize={30} fill={C.dim} opacity={a}>
					{`'${String(10 + i).padStart(2, '0')}`}
				</text>
			))}
			{lab(x(2010), 500, '2010 · FIRST CONCRETE', ink, a, 46)}
			{lab(x(2020), 500, 'CRITICAL · 2020', C.green, tw(f, bAt, bAt + 16, 0, 1), 46, 'end')}
		</svg>
	);
};

// ---------------------------------------------------------------- ten more, as one fleet (S169)
export const TenDomes: React.FC<{at: number}> = ({at}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<path d="M120 760H1800" stroke="#3b4147" strokeWidth={6} />
			{Array.from({length: 10}, (_, i) => {
				const p = tw(f, at + i * 6, at + i * 6 + 18, 0, 1, ez.arrive);
				const x = 230 + i * 162;
				return (
					<g key={i} opacity={p} transform={`translate(0 ${(1 - p) * 40})`}>
						<path d={`M${x - 60} 760V640A60 60 0 0 1 ${x + 60} 640V760Z`} fill="#c9d2d9" stroke="#0b0d0f" strokeWidth={3} />
						<rect x={x - 70} y={740} width={140} height={20} fill="#9aa5ae" />
					</g>
				);
			})}
			{lab(960, 560, 'TEN MORE · ONE FLEET', ink, tw(f, at + 40, at + 60, 0, 1), 56, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- the file opens again: trading (S171–S175)
export const TradeAgain: React.FC<{openAt: number; sheetAt: number}> = ({openAt, sheetAt}) => {
	const f = useCurrentFrame();
	const open = tw(f, openAt, openAt + 30, 0, 1, ez.sweep);
	const sh = useSpring(sheetAt, 140, 18);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'relative', width: 980, height: 680, transform: 'translate(120px, 40px) rotate(-4deg)', perspective: 2000}}>
				<div style={{position: 'absolute', inset: 0, background: C.paper, boxShadow: '0 40px 90px rgba(0,0,0,0.7)', padding: '70px 80px', fontFamily: F.label, color: C.pencil}}>
					<div style={{fontWeight: 800, fontSize: 52, letterSpacing: 4}}>CANADA → INDIA</div>
					<div style={{fontWeight: 700, fontSize: 40, letterSpacing: 2, marginTop: 8, color: '#5a6470'}}>URANIUM CONCENTRATE</div>
					<div style={{marginTop: 60, opacity: sh, transform: `translateY(${(1 - sh) * 30}px)`}}>
						<div style={{fontFamily: F.mono, fontWeight: 700, fontSize: 64, color: C.pencil}}>≈ 10,000 TONNES</div>
						<div style={{fontFamily: F.mono, fontWeight: 700, fontSize: 48, color: '#5a6470', marginTop: 16}}>2027 – 2035</div>
					</div>
				</div>
				<div style={{position: 'absolute', inset: 0, background: '#c8a875', transformOrigin: '0% 50%', transform: `rotateY(${-178 * open}deg)`, backfaceVisibility: 'hidden', boxShadow: '0 30px 70px rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F.label, fontWeight: 800, fontSize: 60, color: '#5a4426', letterSpacing: 6}}>
					CLOSED · 1974
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the question, typed (S186–S187)
export const TypedQuestion: React.FC<{at: number; text: string}> = ({at, text}) => {
	const f = useCurrentFrame();
	const n = Math.round(tw(f, at, at + text.length * 2.2, 0, text.length, (t) => t));
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{maxWidth: 1400, fontFamily: F.label, fontWeight: 800, fontSize: 76, color: ink, textAlign: 'center', lineHeight: 1.2, textShadow: '0 6px 30px rgba(0,0,0,0.9)'}}>
				{text.slice(0, n)}
				<span style={{opacity: Math.floor(f / 15) % 2 ? 1 : 0, color: C.flask}}>|</span>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the end card (the channel's mark; lower half clear for the end screen)
export const EndCard: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	const logo = useSpring(10);
	return (
		<AbsoluteFill style={{alignItems: 'center', paddingTop: 80}}>
			<Img src={staticFile('brand/logo_square.png')} style={{width: 220, height: 220, opacity: logo, borderRadius: 20, transform: `scale(${(0.9 + 0.1 * logo) * (1 + 0.05 * tw(f, 0, dur, 0, 1, (t) => t))})`}} />
			<div style={{marginTop: 24, fontFamily: F.label, fontWeight: 800, fontSize: 52, color: ink, letterSpacing: 2, opacity: logo}}>BE PRACTICAL WITH KISHORE</div>
			<div style={{marginTop: 10, fontFamily: F.label, fontWeight: 700, fontSize: 40, color: C.flask, letterSpacing: 2, opacity: tw(f, 40, 70, 0, 1)}}>STAY PRACTICAL</div>
		</AbsoluteFill>
	);
};
