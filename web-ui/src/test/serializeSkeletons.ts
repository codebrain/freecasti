import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

interface SerializeSkeletonEntry {
  message_length: number;
  b64: string;
}

interface SerializeSkeletonsFile {
  prog: SerializeSkeletonEntry;
  system: SerializeSkeletonEntry;
}

function decodeBase64(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) {
    out[i] = bin.charCodeAt(i);
  }
  return out;
}

let cached: { prog: Uint8Array; system: Uint8Array } | null = null;

/** Load committed serialize skeletons from specification/ (no sysex corpus). */
export function loadSerializeSkeletons(): {
  prog: Uint8Array;
  system: Uint8Array;
} {
  if (cached) return cached;
  const raw = JSON.parse(
    fs.readFileSync(
      path.join(repo, "specification/web_serialize_skeletons.json"),
      "utf8",
    ),
  ) as SerializeSkeletonsFile;
  const prog = decodeBase64(raw.prog.b64);
  const system = decodeBase64(raw.system.b64);
  if (prog.length !== raw.prog.message_length) {
    throw new Error("prog skeleton length mismatch");
  }
  if (system.length !== raw.system.message_length) {
    throw new Error("system skeleton length mismatch");
  }
  cached = { prog, system };
  return cached;
}
