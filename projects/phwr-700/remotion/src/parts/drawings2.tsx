import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {ez, tw, useSpring} from './kit';

// Chapter 2 drawings (word_map.md S45–S79). All on the drafting table; frames are local to the shot.
// H3 ("the ring that slid", plan §8) is drawn here as a section of one channel, not a Blender macro: the physics
// reads more clearly in section and it costs no render time (decided 26 NOV).

const ink = C.ink;
const lab = (x: number, y: number, text: string, color: string, o: number, size = 46, anchor: 'start' | 'middle' | 'end' = 'start') => (
	<text x={x} y={y} textAnchor={anchor} fontFamily={F.label} fontWeight={800} fontSize={size} fill={color} opacity={o} stroke="#0b0d0f" strokeWidth={7} paintOrder="stroke" letterSpacing={1}>
		{text}
	</text>
);

// ---------------------------------------------------------------- one channel in section (S60–S72)
export type ChannelKeys = {
	labelsAt?: number; // the two tubes name themselves
	springsAt?: number; // the springs show
	slipA?: number; // the middle spring slides away
	slipB?: number;
	sagA?: number; // the hot tube sags
	sagB?: number; // …and touches the cold one
	coldAt?: number; // the cold spot goes blue
	hA?: number; // hydrogen creeps to the cold spot
	hB?: number;
	blisterAt?: number;
	crackA?: number;
	crackB?: number;
	splitAt?: number;
};
const X0 = 230;
const X1 = 1690;
const MID = 960;
export const Channel: React.FC<ChannelKeys> = ({labelsAt = 0, springsAt = 0, slipA = 1e9, slipB = 1e9 + 1, sagA = 1e9, sagB = 1e9 + 1, coldAt = 1e9, hA = 1e9, hB = 1e9 + 1, blisterAt = 1e9, crackA = 1e9, crackB = 1e9 + 1, splitAt = 1e9}) => {
	const f = useCurrentFrame();
	const lb = tw(f, labelsAt, labelsAt + 20, 0, 1, ez.arrive);
	const sp = tw(f, springsAt, springsAt + 20, 0, 1, ez.arrive);
	const slip = tw(f, slipA, slipB, 0, 1, ez.cam);
	const sag = tw(f, sagA, sagB, 0, 1, ez.cam);
	const cold = tw(f, coldAt, coldAt + 30, 0, 1);
	const h = tw(f, hA, hB, 0, 1, ez.sweep);
	const blister = tw(f, blisterAt, blisterAt + 50, 0, 1, ez.arrive);
	const crack = tw(f, crackA, crackB, 0, 1, ez.sweep);
	const split = tw(f, splitAt, splitAt + 24, 0, 1, ez.arrive);
	// outer (calandria) tube: inner faces at y 360 and 720; the hot pressure tube runs 440–640, wall 22 px
	const OT = 360;
	const OB = 720;
	const IT = 440;
	const IB = 640;
	const W = 22;
	const drop = 58 * sag; // the sag at mid-span: the bottom wall reaches the outer tube's inner face (640 + 22 + 58 = 720)
	const curve = (y: number) => `M${X0} ${y}Q${MID} ${y + 2 * drop} ${X1} ${y}`;
	const yAt = (y: number, x: number) => {
		const t = (x - X0) / (X1 - X0);
		return y + 4 * drop * t * (1 - t); // the quadratic's height at x (control point at 2×drop gives a peak of drop)
	};
	// springs: ends fixed, the middle one slides off toward the right end
	const springs = [480, MID + slip * 520, 1440];
	const coil = (x: number, y0: number, y1: number, key: string) => (
		<path key={key} d={Array.from({length: 7}, (_, i) => `${i ? 'L' : 'M'}${x - 18 + (i % 2) * 36} ${y0 + ((y1 - y0) * i) / 6}`).join('')} stroke={C.steel} strokeWidth={6} fill="none" strokeLinejoin="round" />
	);
	const contactY = yAt(IB, MID) + W;
	// hydrogen: dots spread through the hot tube's wall that creep to the cold spot
	const dots = Array.from({length: 46}, (_, i) => {
		const x0 = X0 + 80 + random(`hx${i}`) * (X1 - X0 - 160);
		const top = random(`ht${i}`) < 0.35;
		const y0 = top ? IT + 6 + random(`hy${i}`) * (W - 12) : IB + 6 + random(`hy${i}`) * (W - 12);
		const tx = MID + (random(`hd${i}`) - 0.5) * 90;
		const x = x0 + (tx - x0) * h;
		const ty = contactY - W / 2 + (random(`hz${i}`) - 0.5) * 10;
		const yStart = y0 + yAt(0, x0) - 0; // its place in the sagging wall
		return {x, y: yStart + (ty - yStart) * h, i};
	});
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="hot" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#f6b24a" />
					<stop offset="1" stopColor="#c96a1a" />
				</linearGradient>
				<radialGradient id="coldspot">
					<stop offset="0" stopColor={C.water} stopOpacity={0.95} />
					<stop offset="1" stopColor={C.water} stopOpacity={0} />
				</radialGradient>
			</defs>
			{/* the cool calandria tube */}
			<rect x={X0 - 40} y={OT - 26} width={X1 - X0 + 80} height={26} fill="#5d6a75" stroke="#0b0d0f" strokeWidth={3} />
			<rect x={X0 - 40} y={OB} width={X1 - X0 + 80} height={26} fill="#5d6a75" stroke="#0b0d0f" strokeWidth={3} />
			<rect x={X0 - 40} y={OT} width={X1 - X0 + 80} height={OB - OT} fill="#14232c" opacity={0.6} />
			{/* the springs in the gap */}
			<g opacity={sp}>
				{springs.map((x, i) => (
					<g key={i}>
						{coil(x, OT + 2, IT + yAt(0, x) - 2, `t${i}`)}
						{coil(x, yAt(IB, x) + W + 2, OB - 2, `b${i}`)}
					</g>
				))}
			</g>
			{/* the hot pressure tube: two walls following the sag */}
			<path d={`${curve(IT)}L${X1} ${IT + W}Q${MID} ${IT + W + 2 * drop} ${X0} ${IT + W}Z`} fill="url(#hot)" stroke="#0b0d0f" strokeWidth={3} />
			<path d={`${curve(IB)}L${X1} ${IB + W}Q${MID} ${IB + W + 2 * drop} ${X0} ${IB + W}Z`} fill="url(#hot)" stroke="#0b0d0f" strokeWidth={3} />
			<path d={`${curve(IT + W)}L${X1} ${IB}Q${MID} ${IB + 2 * drop} ${X0} ${IB}Z`} fill="#3a1d0a" opacity={0.35} />
			{/* the cold spot where they touch */}
			{cold > 0 ? <ellipse cx={MID} cy={contactY - 6} rx={150 * cold} ry={38 * cold} fill="url(#coldspot)" /> : null}
			{/* hydrogen */}
			{h > 0 || hA < 1e8 ? dots.map((d) => <circle key={d.i} cx={d.x} cy={d.y} r={6} fill="#e9f4ff" stroke="#0b0d0f" strokeWidth={1.5} opacity={f >= hA - 10 ? tw(f, hA - 10, hA + 10, 0, 1) : 0} />) : null}
			{/* blisters */}
			{blister > 0
				? [-50, -10, 34].map((dx, i) => <ellipse key={i} cx={MID + dx} cy={contactY - 12} rx={(14 + i * 3) * blister} ry={9 * blister} fill="#2a2f35" stroke="#0b0d0f" strokeWidth={2} />)
				: null}
			{/* the crack, up through the wall, then the split */}
			{crack > 0 ? (
				<path
					d={`M${MID - 8} ${contactY + 4}l10 -${12 * crack}l-12 -${10 * crack}l14 -${12 * crack}l-8 -${10 * crack}`}
					stroke={C.fail}
					strokeWidth={4}
					fill="none"
					strokeLinejoin="round"
				/>
			) : null}
			{split > 0 ? (
				<g opacity={split}>
					<path d={`M${MID - 30} ${contactY - W}L${MID - 6} ${contactY}L${MID + 22} ${contactY - W}`} fill="#0b0d0f" />
					{[0, 1, 2].map((k) => (
						<ellipse key={k} cx={MID + (k - 1) * 40} cy={contactY - W - 30 - 40 * split - k * 10} rx={40 + 30 * split} ry={24 + 10 * split} fill="#e8eef3" opacity={0.35 * split} />
					))}
				</g>
			) : null}
			{/* labels: what the voice names */}
			{lab(X0, OT - 50, 'COOL TUBE', '#b9c6d1', lb)}
			{lab(X0, IT + W + 70, 'HOT TUBE', C.amber, lb)}
			{lab(springs[1], OB + 90, 'SPRING', C.ink, sp * (slip > 0.02 ? 1 : 0.0) * (1 - tw(f, hA - 20, hA, 0, 1)), 44, 'middle')}
			{lab(MID, contactY + 120, 'COLD SPOT', C.water, cold * (1 - blister), 44, 'middle')}
			{lab(MID, contactY - 90, 'HYDROGEN', '#e9f4ff', tw(f, hA, hA + 20, 0, 1) * (1 - blister), 34, 'middle')}
			{lab(MID, contactY - 90, 'BRITTLE BLISTERS', C.stress, blister * (1 - crack), 34, 'middle')}
			{lab(MID, contactY - 90, 'CRACK', C.fail, crack, 40, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- the tube wall soaking up hydrogen (S54)
export const HydrogenWall: React.FC<{dur: number}> = ({dur}) => {
	const f = useCurrentFrame();
	const n = Math.round(tw(f, 10, dur - 20, 0, 70, (t) => t));
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={260} y={420} width={1400} height={240} fill="url(#hw)" stroke="#0b0d0f" strokeWidth={4} />
			<defs>
				<linearGradient id="hw" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#9aa5ae" />
					<stop offset="1" stopColor="#5d6a75" />
				</linearGradient>
			</defs>
			{Array.from({length: n}, (_, i) => (
				<circle key={i} cx={280 + random(`w${i}`) * 1360} cy={440 + random(`v${i}`) * 200} r={8} fill="#e9f4ff" stroke="#0b0d0f" strokeWidth={2} opacity={tw(f, 10 + i * ((dur - 30) / 70), 20 + i * ((dur - 30) / 70), 0, 1)} />
			))}
			{lab(260, 390, 'THE TUBE WALL', ink, 1)}
			{lab(1660, 720, 'HYDROGEN', '#e9f4ff', tw(f, 20, 40, 0, 1), 52, 'end')}
		</svg>
	);
};

// ---------------------------------------------------------------- 10–12 years on a 30-year ruler (S55)
export const TubeLife: React.FC<{shadeAt: number}> = ({shadeAt}) => {
	const f = useCurrentFrame();
	const draw = tw(f, 0, 40, 0, 1, ez.sweep);
	const sh = tw(f, shadeAt, shadeAt + 40, 0, 1, ez.sweep);
	const x = (y: number) => 260 + (y / 30) * 1400;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={x(0)} y={500} width={1400 * draw} height={80} fill="#2a3036" stroke="#0b0d0f" strokeWidth={3} />
			<rect x={x(0)} y={500} width={(x(10) - x(0)) * sh} height={80} fill={C.amber} opacity={0.9} />
			<rect x={x(10)} y={500} width={(x(12) - x(10)) * sh} height={80} fill={C.stress} />
			{[0, 5, 10, 15, 20, 25, 30].map((y) => (
				<g key={y} opacity={draw}>
					<path d={`M${x(y)} 590V620`} stroke={ink} strokeWidth={3} />
					<text x={x(y)} y={666} textAnchor="middle" fontFamily={F.mono} fontWeight={700} fontSize={38} fill={C.dim}>
						{y}
					</text>
				</g>
			))}
			{lab(x(11), 470, '10–12 YEARS', C.stress, sh, 60, 'middle')}
			{lab(x(30), 740, 'YEARS IN THE REACTOR', C.dim, draw, 36, 'end')}
		</svg>
	);
};

// ---------------------------------------------------------------- a steel tumbler of cold water on a hot day (S66–S67)
export const Tumbler: React.FC<{dropsA: number; dropsB: number}> = ({dropsA, dropsB}) => {
	const f = useCurrentFrame();
	const k = tw(f, dropsA, dropsB, 0, 1, (t) => t);
	const drops = Array.from({length: 60}, (_, i) => ({x: random(`tx${i}`), y: random(`ty${i}`), r: 4 + random(`tr${i}`) * 7, t: random(`tt${i}`)}));
	const slide = (i: number) => (drops[i].r > 9 ? tw(f, dropsA + drops[i].t * (dropsB - dropsA) + 30, dropsB + 60, 0, 120) : 0);
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 60% 50% at 70% 20%, rgba(255,200,120,0.35), transparent 70%)'}} />
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<defs>
					<linearGradient id="steelT" x1="0" y1="0" x2="1" y2="0">
						<stop offset="0" stopColor="#6c7780" />
						<stop offset="0.35" stopColor="#e5ebef" />
						<stop offset="0.6" stopColor="#9aa5ae" />
						<stop offset="1" stopColor="#4c565f" />
					</linearGradient>
				</defs>
				<ellipse cx={960} cy={900} rx={260} ry={34} fill="#000" opacity={0.4} />
				<path d="M720 260L760 890Q960 920 1160 890L1200 260Z" fill="url(#steelT)" stroke="#0b0d0f" strokeWidth={4} />
				<ellipse cx={960} cy={260} rx={240} ry={30} fill="#c9d2d9" stroke="#0b0d0f" strokeWidth={4} />
				<ellipse cx={960} cy={268} rx={222} ry={22} fill="#4f8fb5" opacity={0.8} />
				{drops.map((d, i) =>
					k > d.t ? (
						<ellipse key={i} cx={760 + d.x * 400} cy={330 + d.y * 520 + slide(i)} rx={d.r * 0.8} ry={d.r} fill="#ffffff" opacity={0.75 * tw(f, dropsA + d.t * (dropsB - dropsA), dropsA + d.t * (dropsB - dropsA) + 12, 0, 1)} stroke="#6c7780" strokeWidth={1.5} />
					) : null,
				)}
			</svg>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the power needle eases to a safe stop (S73)
export const SafeStop: React.FC<{stopA: number; stopB: number}> = ({stopA, stopB}) => {
	const f = useCurrentFrame();
	const v = tw(f, stopA, stopB, 1, 0, ez.cam);
	const ang = -120 + 240 * v;
	const ok = tw(f, stopB, stopB + 20, 0, 1, ez.arrive);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<circle cx={960} cy={560} r={300} fill="#e9e2d0" stroke="#2a3036" strokeWidth={16} />
			{Array.from({length: 11}, (_, i) => {
				const a = ((-120 + 24 * i - 90) * Math.PI) / 180;
				return <path key={i} d={`M${960 + 250 * Math.cos(a)} ${560 + 250 * Math.sin(a)}L${960 + 280 * Math.cos(a)} ${560 + 280 * Math.sin(a)}`} stroke="#2a3036" strokeWidth={6} />;
			})}
			<text x={960} y={700} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={48} fill="#2a3036" letterSpacing={4}>
				POWER
			</text>
			<g transform={`rotate(${ang} 960 560)`}>
				<path d="M954 560L960 300L966 560Z" fill={C.fail} />
			</g>
			<circle cx={960} cy={560} r={22} fill="#2a3036" />
			{lab(960, 200, 'SAFELY STOPPED', C.green, ok, 64, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- a quoted line on a typed slip (S76): a quotation, never a facsimile page
export const QuoteSlip: React.FC<{text: string; source: string; litA: number; litB: number}> = ({text, source, litA, litB}) => {
	const f = useCurrentFrame();
	const p = useSpring(0, 140, 18);
	const lit = tw(f, litA, litB, 0, 1, (t) => t);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{width: 1320, background: C.paper, padding: '56px 70px', transform: `rotate(-2deg) translateY(${(1 - p) * 300}px)`, boxShadow: '0 40px 90px rgba(0,0,0,0.7)', fontFamily: F.mono}}>
				<div style={{fontSize: 30, fontWeight: 700, color: '#6b6355', letterSpacing: 3, marginBottom: 26}}>{source}</div>
				<div style={{fontSize: 56, fontWeight: 700, color: C.pencil, lineHeight: 1.3, position: 'relative'}}>
					<span style={{background: `linear-gradient(90deg, rgba(255,194,26,0.55) ${lit * 100}%, transparent ${lit * 100}%)`}}>{text}</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- a calendar page (MAY 1974, AUG 1983)
export const CalendarPage: React.FC<{month: string; year: string}> = ({month, year}) => {
	const p = useSpring(0, 150, 16);
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{width: 640, height: 720, background: C.paper, transform: `rotate(${3 - 2 * tw(f, 0, 200, 0, 1)}deg) translateY(${(1 - p) * -500}px)`, boxShadow: '0 40px 90px rgba(0,0,0,0.7)', display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: F.label, color: C.pencil}}>
				<div style={{width: '100%', height: 70, background: '#8c2f24'}} />
				<div style={{fontWeight: 800, fontSize: 150, marginTop: 50, letterSpacing: 10}}>{month}</div>
				<div style={{fontWeight: 800, fontSize: 130, color: '#8c2f24'}}>{year}</div>
			</div>
		</AbsoluteFill>
	);
};
