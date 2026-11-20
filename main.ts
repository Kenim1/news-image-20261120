// News-image entry for 20 November 2026 (Node 22, standard library only).
// The image is drawn by draw.py and shipped as entry.png beside this file;
// the program copies it to /output/entry.png, deterministically, twice.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const entry = new URL('./entry.png', import.meta.url);
if (!existsSync(entry)) {
  throw new Error('entry.png is missing beside main.ts');
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(entry, join(outDir, 'entry.png'));
