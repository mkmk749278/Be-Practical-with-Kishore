import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {loadFont} from '@remotion/fonts';
import {continueRender, delayRender} from 'remotion';
import {Atmos, ez, tw} from './parts/kit';
import {C} from './theme';
import {AUDIO, DURATION} from './timing';

// The film as one list of shots (each runs until the next one starts) plus overlays (labels, counters) on their own
// frames. A shot fades in over LEAD frames (0.2 s dissolve, §9.3) unless it is a designed hard cut.
export type Shot = {
	at: number; // the frame the shot is fully on (its word or sentence)
	name: string;
	hard?: boolean;
	el: (dur: number, lead: number) => React.ReactNode; // dur includes the lead-in
	fixed?: React.ReactNode; // honesty tag and credit, drawn outside the reframing
};
export type Overlay = {from: number; to: number; name: string; el: React.ReactNode};
export type Part = {shots: Shot[]; overlays: Overlay[]};

export const LEAD = 12;

let fontsStarted = false;
const loadFonts = () => {
	if (fontsStarted) {
		return;
	}
	fontsStarted = true;
	const h = delayRender('fonts');
	Promise.all([
		...['600', '700', '800'].map((w) => loadFont({family: 'Inter Tight', url: staticFile(`fonts/inter-tight-latin-${w}-normal.woff2`), weight: w})),
		loadFont({family: 'Inter Tight', url: staticFile('fonts/inter-tight-latin-ext-800-normal.woff2'), weight: '800', unicodeRange: 'U+0100-024F, U+20A0-20CF'}),
		loadFont({family: 'JetBrains Mono', url: staticFile('fonts/jetbrains-mono-latin-700-normal.woff2'), weight: '700'}),
	]).then(() => continueRender(h));
};

const FadeIn: React.FC<{lead: number; children: React.ReactNode}> = ({lead, children}) => {
	const f = useCurrentFrame();
	return <AbsoluteFill style={{opacity: lead > 0 ? tw(f, 0, lead, 0, 1, ez.sweep) : 1}}>{children}</AbsoluteFill>;
};

const OverlayFade: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
	const f = useCurrentFrame();
	return <AbsoluteFill style={{opacity: tw(f, dur - 10, dur, 1, 0, ez.leave)}}>{children}</AbsoluteFill>;
};

export const Film: React.FC<{parts: Part[]; from?: number; to?: number; audio?: boolean}> = ({parts, from = 0, to = DURATION, audio = true}) => {
	loadFonts();
	const shots = parts.flatMap((p) => p.shots).sort((a, b) => a.at - b.at);
	const overlays = parts.flatMap((p) => p.overlays);
	return (
		<AbsoluteFill style={{background: C.night}}>
			{shots.map((s, i) => {
				const lead = i === 0 || s.hard ? 0 : LEAD;
				const start = s.at - lead;
				const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
				if (end <= from || start >= to) {
					return null;
				}
				const dur = end - start;
				return (
					<Sequence key={s.name + i} from={start - from} durationInFrames={dur} name={s.name}>
						<FadeIn lead={lead}>
							{s.el(dur, lead)}
							{s.fixed}
						</FadeIn>
					</Sequence>
				);
			})}
			{overlays.map((o, i) =>
				o.to <= from || o.from >= to ? null : (
					<Sequence key={o.name + i} from={o.from - from} durationInFrames={Math.max(1, o.to - o.from)} name={o.name}>
						<OverlayFade dur={o.to - o.from}>{o.el}</OverlayFade>
					</Sequence>
				),
			)}
			<Atmos />
			{audio ? <Audio src={staticFile('assets/vo/phwr_vo_full.wav')} startFrom={from} /> : null}
		</AbsoluteFill>
	);
};
