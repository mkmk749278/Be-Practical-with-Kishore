import React from 'react';
import {Composition} from 'remotion';
import {Film, type Part} from './Film';
import {p1} from './scenes/p1_open_ch1';
import {p2} from './scenes/p2_ch2';
import {p3} from './scenes/p3_ch3';
import {p4} from './scenes/p4_ch4_end';
import {DURATION, FPS, s0} from './timing';

const parts: Part[] = [p1, p2, p3, p4];
const P1_END = s0(45); // chapter 2 starts at S45
const P2_END = s0(80); // chapter 3 starts at S80
const P3_END = s0(122); // chapter 4 starts at S122

const Whole: React.FC = () => <Film parts={parts} />;
const Part1: React.FC = () => <Film parts={parts} from={0} to={P1_END} />;
const Part2: React.FC = () => <Film parts={parts} from={P1_END} to={P2_END} />;
const Part3: React.FC = () => <Film parts={parts} from={P2_END} to={P3_END} />;
const Part4: React.FC = () => <Film parts={parts} from={P3_END} to={DURATION} />;

export const Root: React.FC = () => (
	<>
		<Composition id="phwr" component={Whole} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
		<Composition id="p1" component={Part1} durationInFrames={P1_END} fps={FPS} width={1920} height={1080} />
		<Composition id="p2" component={Part2} durationInFrames={P2_END - P1_END} fps={FPS} width={1920} height={1080} />
		<Composition id="p3" component={Part3} durationInFrames={P3_END - P2_END} fps={FPS} width={1920} height={1080} />
		<Composition id="p4" component={Part4} durationInFrames={DURATION - P3_END} fps={FPS} width={1920} height={1080} />
	</>
);
