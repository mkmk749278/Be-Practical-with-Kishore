// Frames from the locked audio (vo/timing.json, lock ecbfc8f52df9). Scenes never type a frame by hand (§10.2).
import T from '../../vo/timing.json';

type Word = {s: number; w: string; startFrame: number; endFrame: number};
type Sent = {id: number; text: string; startFrame: number; endFrame: number};
const sentences = T.sentences as Sent[];
const words = T.words as Word[];

export const FPS = T.fps;
export const DURATION = T.durationInFrames;
export const VO_FRAMES = T.voDurationInFrames;
export const AUDIO = T.audio;

const norm = (t: string): string => t.toLowerCase().replace(/[^a-z0-9]+/g, '');

/** first frame of sentence `id` */
export const s0 = (id: number): number => sentences[id].startFrame;
/** last frame of sentence `id` */
export const s1 = (id: number): number => sentences[id].endFrame;
/** the sentence's text (checks in the shot list) */
export const sText = (id: number): string => sentences[id].text;

const find = (id: number, word: string, nth: number): Word => {
	const q = word.split(' ').map(norm);
	const ws = words.filter((w) => w.s === id);
	let seen = 0;
	for (let i = 0; i + q.length <= ws.length; i++) {
		if (q.every((p, k) => norm(ws[i + k].w) === p)) {
			if (seen === nth) {
				return {...ws[i], endFrame: ws[i + q.length - 1].endFrame};
			}
			seen++;
		}
	}
	throw new Error(`timing: no "${word}" (#${nth}) in S${id} "${sentences[id].text}"`);
};
/** start frame of `word` (or a phrase) in sentence `id` */
export const w0 = (id: number, word: string, nth = 0): number => find(id, word, nth).startFrame;
/** end frame of `word` (or a phrase) in sentence `id` */
export const w1 = (id: number, word: string, nth = 0): number => find(id, word, nth).endFrame;
