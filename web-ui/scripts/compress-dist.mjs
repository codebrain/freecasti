import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { brotliCompressSync, gzipSync } from "node:zlib";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../dist");
const MIN_SIZE = 256;
const EXT_RE = /\.(html|css|js|json|syx)$/i;
const LEGACY_DIST_ROOTS = ["spec", "presets", "templates"];
const LEGACY_DIST_FILES = ["sync-manifest.json"];

function walk(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (fs.statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

function pruneLegacyDist() {
  let removed = 0;
  for (const name of LEGACY_DIST_ROOTS) {
    const p = path.join(dist, name);
    if (fs.existsSync(p)) {
      fs.rmSync(p, { recursive: true, force: true });
      removed += 1;
    }
  }
  for (const name of LEGACY_DIST_FILES) {
    const p = path.join(dist, name);
    if (fs.existsSync(p)) {
      fs.rmSync(p, { force: true });
      removed += 1;
    }
  }
  return removed;
}

if (!fs.existsSync(dist)) {
  console.error("dist/ not found");
  process.exit(1);
}

const pruned = pruneLegacyDist();
if (pruned > 0) {
  console.log(`removed ${pruned} legacy path(s) from dist/`);
}

let count = 0;
for (const file of walk(dist)) {
  if (!EXT_RE.test(file) || file.endsWith(".gz") || file.endsWith(".br")) continue;
  const buf = fs.readFileSync(file);
  if (buf.length < MIN_SIZE) continue;
  fs.writeFileSync(`${file}.gz`, gzipSync(buf));
  fs.writeFileSync(`${file}.br`, brotliCompressSync(buf));
  count += 2;
}
console.log(`wrote ${count} precompressed files (.gz / .br) under dist/`);
