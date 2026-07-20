import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

function decodeBase64(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) {
    out[i] = bin.charCodeAt(i);
  }
  return out;
}

let cached: { prog: Uint8Array; system: Uint8Array } | null = null;

/** Load the spec-derived serialize skeletons from the runtime bundle. */
export function loadSerializeSkeletons(): {
  prog: Uint8Array;
  system: Uint8Array;
} {
  if (cached) return cached;
  const raw = JSON.parse(
    fs.readFileSync(
      path.join(repo, "web-ui/public/m7-runtime.json"),
      "utf8",
    ),
  ) as { tpl: { p: string; s: string } };
  cached = {
    prog: decodeBase64(raw.tpl.p),
    system: decodeBase64(raw.tpl.s),
  };
  return cached;
}
