import path from 'path';
import {Config} from '@remotion/cli/config';

// phwr-700 (PLAYBOOK §10.2): 1920×1080, 60 fps, Remotion 4.0.534. lib/remotion resolves its imports from this
// film's node_modules.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setConcurrency(2);
Config.setChromiumOpenGlRenderer('swangle');
Config.overrideWebpackConfig((c) => ({
	...c,
	resolve: {...c.resolve, modules: [path.resolve(__dirname, 'node_modules'), 'node_modules']},
}));
