import {p1} from './scenes/p1_open_ch2';
import {p2} from './scenes/p2_ch3_ch4';
import {p3} from './scenes/p3_ch5_end';
import {DURATION} from './timing';
const shots = [...p1, ...p2, ...p3].flatMap((p) => p.shots).sort((a, b) => a.at - b.at);
shots.forEach((s, i) => {
	const end = i + 1 < shots.length ? shots[i + 1].at : DURATION;
	console.log([(s.at / 60).toFixed(2), ((end - s.at) / 60).toFixed(2), s.name].join('\t'));
});
