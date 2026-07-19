import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../dist");

function walk(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (fs.statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

if (!fs.existsSync(dist)) {
  console.error("dist/ not found — run npm run build first");
  process.exit(1);
}

const files = walk(dist).filter(
  (f) => !f.endsWith(".gz") && !f.endsWith(".br"),
);
let rawTotal = 0;
let gzipTotal = 0;

const rows = files.map((file) => {
  const buf = fs.readFileSync(file);
  const rel = path.relative(dist, file);
  const gz = gzipSync(buf).length;
  rawTotal += buf.length;
  gzipTotal += gz;
  return { rel, raw: buf.length, gzip: gz };
});

rows.sort((a, b) => b.raw - a.raw);
console.log("dist/ size report\n");
for (const { rel, raw, gzip } of rows.slice(0, 20)) {
  console.log(
    `${String(raw).padStart(9)} B  (${String(gzip).padStart(7)} gzip)  ${rel}`,
  );
}
if (rows.length > 20) console.log(`... ${rows.length - 20} more files`);
console.log(
  `\nTotal: ${rawTotal} B raw, ${gzipTotal} B gzip (${rows.length} files, excl. precompressed .gz/.br)`,
);
