// phwr-700 art direction (word_map.md): warm steel, Rajasthan sandstone, the green of the lake. Caution yellow is
// the flask and the new tubes (the motif); the cold blue of heavy water only inside the tank. Colour means something.
export const C = {
	night: '#05080c', // behind everything
	plate: '#1c1f22', // the steel drafting table
	grid: '#5b6b7c',
	ink: '#eef3f8',
	dim: '#aab4bf',
	flask: '#ffc21a', // caution yellow: the flask, the new tubes, the motif
	amber: '#f2a93b', // heat, pressure, fuel
	stress: '#f0883e', // safety orange: wear, faults, the crack
	fail: '#ff4636', // a FAILED outcome only
	water: '#3aa0d8', // heavy water, inside the tank only
	lake: '#4f8f7a', // Rana Pratap Sagar
	sand: '#c9a36b', // Rajasthan sandstone
	steel: '#8d98a3',
	green: '#3fd27a', // verified, running
	paper: '#e9e2d0', // drafting paper
	pencil: '#2a3440',
} as const;

export const F = {
	label: "'Inter Tight', 'Helvetica Neue', Arial, sans-serif",
	mono: "'JetBrains Mono', 'Courier New', monospace",
} as const;

export const W = 1920;
export const H = 1080;
export const FPS = 60;
