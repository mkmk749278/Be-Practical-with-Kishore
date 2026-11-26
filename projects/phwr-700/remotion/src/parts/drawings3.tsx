import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {ez, tw, useSpring} from './kit';

// Chapter 3 drawings (word_map.md S80–S121). H4, the old tube's journey (plan §8), is drawn in the same section
// language as H3 (drawings2.tsx Channel), decided 26 NOV: one visual grammar for the inside of a channel.

const ink = C.ink;
const lab = (x: number, y: number, text: string, color: string, o: number, size = 46, anchor: 'start' | 'middle' | 'end' = 'start') => (
	<text x={x} y={y} textAnchor={anchor} fontFamily={F.label} fontWeight={800} fontSize={size} fill={color} opacity={o} stroke="#0b0d0f" strokeWidth={7} paintOrder="stroke" letterSpacing={1}>
		{text}
	</text>
);

// ---------------------------------------------------------------- the owners' club: a round table, India's seat (S82)
export const ClubTable: React.FC<{indiaAt: number}> = ({indiaAt}) => {
	const f = useCurrentFrame();
	const draw = tw(f, 0, 30, 0, 1, ez.arrive);
	const ind = tw(f, indiaAt, indiaAt + 20, 0, 1, ez.arrive);
	const seats = 8;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<ellipse cx={960} cy={560} rx={420} ry={230} fill="#3a2c1d" stroke="#0b0d0f" strokeWidth={5} opacity={draw} />
			<ellipse cx={960} cy={548} rx={400} ry={215} fill="#5a4329" opacity={draw} />
			{Array.from({length: seats}, (_, i) => {
				const a = (i / seats) * Math.PI * 2 + Math.PI / 2;
				const x = 960 + 520 * Math.cos(a);
				const y = 560 + 300 * Math.sin(a);
				const isIndia = i === 0;
				return (
					<g key={i} opacity={draw}>
						<rect x={x - 46} y={y - 30} width={92} height={60} rx={12} fill={isIndia ? C.flask : '#3b4147'} opacity={isIndia ? 0.3 + 0.7 * ind : 0.9} stroke="#0b0d0f" strokeWidth={3} />
					</g>
				);
			})}
			{lab(960, 560 + 300 + 100, 'INDIA', C.flask, ind, 56, 'middle')}
			{lab(960, 250, 'CANDU OWNERS GROUP', ink, draw, 52, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- the dose meter swings into the red (S89–S90)
export const DoseMeter: React.FC<{swingAt: number}> = ({swingAt}) => {
	const f = useCurrentFrame();
	const v = tw(f, swingAt, swingAt + 40, 0.1, 0.97, ez.arrive) + (f > swingAt + 40 ? 0.015 * Math.sin(f / 3) : 0);
	const ang = -120 + 240 * v;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<rect x={620} y={240} width={680} height={600} rx={40} fill="#c9a23a" stroke="#0b0d0f" strokeWidth={6} />
			<circle cx={960} cy={560} r={250} fill="#e9e2d0" stroke="#2a3036" strokeWidth={10} />
			<path d={describeArc(960, 560, 215, 60, 120)} stroke={C.fail} strokeWidth={34} fill="none" />
			{Array.from({length: 11}, (_, i) => {
				const a = ((-120 + 24 * i - 90) * Math.PI) / 180;
				return <path key={i} d={`M${960 + 200 * Math.cos(a)} ${560 + 200 * Math.sin(a)}L${960 + 235 * Math.cos(a)} ${560 + 235 * Math.sin(a)}`} stroke="#2a3036" strokeWidth={5} />;
			})}
			<text x={960} y={680} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={42} fill="#2a3036" letterSpacing={4}>
				DOSE
			</text>
			<g transform={`rotate(${ang} 960 560)`}>
				<path d="M954 560L960 340L966 560Z" fill="#111" />
			</g>
			<circle cx={960} cy={560} r={20} fill="#2a3036" />
		</svg>
	);
};
const describeArc = (cx: number, cy: number, r: number, a0: number, a1: number) => {
	const p = (a: number) => [cx + r * Math.cos(((a - 90) * Math.PI) / 180), cy + r * Math.sin(((a - 90) * Math.PI) / 180)];
	const [x0, y0] = p(a0);
	const [x1, y1] = p(a1);
	return `M${x0} ${y0}A${r} ${r} 0 0 1 ${x1} ${y1}`;
};

// ---------------------------------------------------------------- a blank sheet that fills with a tool drawing (S92–S93)
export const ToolSheet: React.FC<{fillAt: number}> = ({fillAt}) => {
	const f = useCurrentFrame();
	const k = tw(f, fillAt, fillAt + 90, 0, 1, ez.sweep);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'relative', width: 1300, height: 840, transform: 'rotate(-3deg)', background: '#dfe6ea', boxShadow: '0 50px 100px rgba(0,0,0,0.7)'}}>
				<svg width={1300} height={840} style={{position: 'absolute'}}>
					<rect x={30} y={30} width={1240} height={780} fill="none" stroke="#2e4a66" strokeWidth={3} />
					<g stroke="#2e4a66" strokeWidth={3} fill="none">
						{/* a long-reach cutting tool: a tube with a head, a cutter wheel, a drive at the back */}
						<path pathLength={1} strokeDasharray={`${k} 1`} d="M140 420H900M140 470H900M140 420V470" />
						<path pathLength={1} strokeDasharray={`${k} 1`} d="M900 395H1060V495H900Z" />
						<circle cx={1000} cy={445} r={36} pathLength={1} strokeDasharray={`${k} 1`} />
						<path pathLength={1} strokeDasharray={`${k} 1`} d="M960 445H1040M1000 405V485" />
						<path pathLength={1} strokeDasharray={`${k} 1`} d="M100 360H240V530H100Z" />
						<path pathLength={1} strokeDasharray={`${k} 1`} d="M140 600H1060M140 585V615M1060 585V615" strokeWidth={2} />
					</g>
				</svg>
				<div style={{position: 'absolute', right: 50, bottom: 50, opacity: tw(f, fillAt + 60, fillAt + 90, 0, 1), fontFamily: F.label, fontWeight: 800, fontSize: 40, color: '#1d3550', letterSpacing: 3, border: '3px solid #2e4a66', padding: '10px 22px', background: '#dfe6ea'}}>
					DESIGNED IN INDIA
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- H4: the old tube's journey (S94–S99)
/** cutAt: the tool reaches in, both ends cut; drawA..drawB: the tube slides into the yellow flask; carryA..carryB: the
 *  flask rolls away to the vault door; the room has no person in it. */
export const TubeJourney: React.FC<{cutAt: number; drawA: number; drawB: number; carryA: number; carryB: number}> = ({cutAt, drawA, drawB, carryA, carryB}) => {
	const f = useCurrentFrame();
	const tool = tw(f, cutAt - 30, cutAt, 0, 1, ez.cam);
	const cut = tw(f, cutAt, cutAt + 24, 0, 1);
	const pull = tw(f, drawA, drawB, 0, 1, ez.cam);
	const carry = tw(f, carryA, carryB, 0, 1, ez.cam);
	const TUBE = 800;
	const fx = 880 + carry * 1100; // the flask's mouth; the old tube rides inside it
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{/* the reactor: a wall of the end shield with the channel opening */}
			<rect x={120} y={260} width={160} height={560} fill="#2a3036" stroke="#0b0d0f" strokeWidth={4} />
			<rect x={-200} y={420} width={480} height={120} fill="#14232c" />
			{/* the old tube, grey and stained */}
			<g transform={`translate(${pull * 1420 + carry * 1100} 0)`}>
				<rect x={-420} y={448} width={TUBE} height={64} rx={10} fill="#7b6f63" stroke="#0b0d0f" strokeWidth={3} />
				{[-300, -40, 220].map((x) => (
					<rect key={x} x={x} y={448} width={60} height={64} fill="#5b4f45" opacity={0.6} />
				))}
			</g>
			{/* the cut: two sparks at the ends */}
			{cut > 0 && cut < 1 ? <circle cx={282} cy={480} r={26 * (1 - cut)} fill={C.amber} opacity={0.9} /> : null}
			{/* the tool reaching in from the flask side */}
			<rect x={300 + (1 - tool) * 560} y={466} width={200} height={28} fill="#9aa5ae" opacity={1 - pull} stroke="#0b0d0f" strokeWidth={2} />
			{/* the yellow flask on its carriage */}
			<g transform={`translate(${fx} 0)`}>
				<rect x={0} y={390} width={1000} height={180} rx={24} fill={C.flask} stroke="#0b0d0f" strokeWidth={5} />
				{[220, 500, 780].map((x) => (
					<rect key={x} x={x} y={390} width={18} height={180} fill="#1b1d20" />
				))}
				<rect x={30} y={570} width={940} height={40} fill="#3b4147" />
				{[90, 910].map((x) => (
					<circle key={x} cx={x} cy={626} r={26} fill="#1b1d20" />
				))}
			</g>
			{/* the vault door at the right */}
			<rect x={1720} y={300} width={200} height={420} fill="#1b1d20" stroke="#4b525a" strokeWidth={6} opacity={tw(f, carryA - 30, carryA, 0, 1)} />
			<path d="M0 680H1920" stroke="#3b4147" strokeWidth={6} />
			{lab(200, 230, 'THE REACTOR', C.dim, 1 - carry, 40, 'middle')}
			{lab(1380, 360, 'STEEL FLASK', C.flask, tw(f, drawA - 30, drawA, 0, 1) * (1 - carry), 44, 'middle')}
			{lab(1820, 270, 'VAULT', ink, tw(f, carryA, carryA + 30, 0, 1), 44, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- the cost: ₹250 crore vs more than ₹1,000 crore (S104–S106)
export const CostStacks: React.FC<{indiaAt: number; canadaAt: number}> = ({indiaAt, canadaAt}) => {
	const f = useCurrentFrame();
	const a = tw(f, indiaAt, indiaAt + 40, 0, 1, ez.sweep);
	const b = tw(f, canadaAt, canadaAt + 60, 0, 1, ez.sweep);
	const unit = 150; // px per ₹250 crore
	const stack = (x: number, h: number, k: number, color: string) => (
		<g>
			{Array.from({length: Math.ceil((h * k) / 22)}, (_, i) => (
				<rect key={i} x={x} y={860 - (i + 1) * 22} width={240} height={20} rx={3} fill={color} stroke="#0b0d0f" strokeWidth={2} />
			))}
		</g>
	);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{stack(560, unit, a, C.green)}
			{stack(1120, unit * 4.25, b, C.stress)}
			{lab(680, 860 - unit * a - 30, '₹250 CRORE', C.green, a, 56, 'middle')}
			{lab(680, 930, 'INDIA PLANNED', ink, a, 40, 'middle')}
			{lab(1240, 860 - unit * 4.25 * b - 30, '₹1,000+ CRORE', C.stress, b, 56, 'middle')}
			{lab(1240, 930, 'CANADA SPENT', ink, b, 40, 'middle')}
		</svg>
	);
};

// ---------------------------------------------------------------- 1995, 1996, 1997: no power (S109)
export const NoPowerYears: React.FC<{at: number}> = ({at}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{['1995', '1996', '1997'].map((y, i) => {
				const p = tw(f, at + i * 14, at + i * 14 + 18, 0, 1, ez.arrive);
				const x = 340 + i * 440;
				return (
					<g key={y} opacity={p} transform={`translate(0 ${(1 - p) * -60})`}>
						<rect x={x} y={300} width={360} height={420} fill={C.paper} stroke="#0b0d0f" strokeWidth={3} />
						<rect x={x} y={300} width={360} height={56} fill="#8c2f24" />
						<text x={x + 180} y={440} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={92} fill={C.pencil}>
							{y}
						</text>
						<path d={`M${x + 40} 600H${x + 320}`} stroke={C.fail} strokeWidth={8} />
						<text x={x + 180} y={580} textAnchor="middle" fontFamily={F.mono} fontWeight={700} fontSize={34} fill="#6b6355">
							POWER: 0
						</text>
					</g>
				);
			})}
		</svg>
	);
};

// ---------------------------------------------------------------- first and second in the world (S111–S112), NPCIL
export const FirstSecond: React.FC<{secondAt: number; firstAt: number}> = ({secondAt, firstAt}) => {
	const s = useSpring(secondAt, 160, 16);
	const fi = useSpring(firstAt, 160, 16);
	const plate = (x: number, n: string, place: string, color: string, p: number) => (
		<g opacity={p} transform={`translate(0 ${(1 - p) * 40})`}>
			<rect x={x} y={380} width={620} height={300} rx={14} fill="#1b1f24" stroke={color} strokeWidth={6} />
			<text x={x + 310} y={500} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={96} fill={color}>
				{n}
			</text>
			<text x={x + 310} y={600} textAnchor="middle" fontFamily={F.label} fontWeight={800} fontSize={48} fill={ink} letterSpacing={2}>
				{place}
			</text>
		</g>
	);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			{plate(260, '1ST', 'CANADA', C.steel, fi)}
			{plate(1040, '2ND', 'RAWATBHATA', C.flask, s)}
		</svg>
	);
};

// ---------------------------------------------------------------- the radio with its back off (S115–S116)
export const OpenRadio: React.FC<{openAt: number}> = ({openAt}) => {
	const f = useCurrentFrame();
	const o = tw(f, openAt, openAt + 30, 0, 1, ez.cam);
	const glow = 0.5 + 0.5 * Math.sin(f / 14);
	return (
		<svg width={1920} height={1080} style={{position: 'absolute'}}>
			<AbsoluteFillShadow />
			{/* the cabinet, seen from behind */}
			<rect x={560} y={300} width={800} height={480} rx={36} fill="#5a3a20" stroke="#0b0d0f" strokeWidth={6} />
			<rect x={600} y={340} width={720} height={400} rx={20} fill="#1b130c" />
			{/* valves and the chassis inside */}
			{[700, 820, 940, 1060, 1180].map((x, i) => (
				<g key={x}>
					<rect x={x - 26} y={470} width={52} height={120} rx={26} fill="#c9b79a" opacity={0.85} />
					<rect x={x - 26} y={470} width={52} height={120} rx={26} fill={C.amber} opacity={0.35 * glow * o * (i % 2 ? 1 : 0.7)} />
				</g>
			))}
			<rect x={640} y={600} width={640} height={60} fill="#3b4147" />
			{/* the back panel lifts away */}
			<g transform={`translate(${o * 520} ${o * 140}) rotate(${o * 14} 960 540)`}>
				<rect x={590} y={330} width={740} height={420} rx={20} fill="#7a5a36" stroke="#0b0d0f" strokeWidth={5} opacity={0.98} />
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<rect key={i} x={680 + i * 100} y={420} width={40} height={240} rx={14} fill="#4a3420" />
				))}
			</g>
			{/* the screwdriver */}
			<g transform={`translate(${1300 - o * 80} 860) rotate(-12)`}>
				<rect x={0} y={-14} width={180} height={28} rx={10} fill={C.fail} />
				<rect x={180} y={-5} width={200} height={10} fill="#c0c6cb" />
			</g>
		</svg>
	);
};
const AbsoluteFillShadow: React.FC = () => <ellipse cx={960} cy={800} rx={480} ry={40} fill="#000" opacity={0.45} />;
