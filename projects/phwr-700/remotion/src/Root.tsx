import React from 'react';
import {Composition} from 'remotion';
import {Film, type Part} from './Film';
import {p1} from './scenes/p1_open_ch1';
import {DURATION, FPS, s0} from './timing';

const parts: Part[] = [p1];
const P1_END = s0(45); // chapter 2 starts at S45

const Whole: React.FC = () => <Film parts={parts} />;
const Part1: React.FC = () => <Film parts={parts} from={0} to={P1_END} />;

export const Root: React.FC = () => (
	<>
		<Composition id="phwr" component={Whole} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
		<Composition id="p1" component={Part1} durationInFrames={P1_END} fps={FPS} width={1920} height={1080} />
	</>
);
