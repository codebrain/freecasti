import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { M7ProgramDump, M7SystemDump } from "@/generated/sysex-parsers/index.js";
import type { KaitaiSpecField } from "@/sysex/kaitaiEncode";
import { fieldWireBytes } from "@/sysex/kaitaiEncode";
import {
  programDumpChecksum,
  systemDumpChecksum,
  verifyProgramDumpChecksum,
  verifySystemDumpChecksum,
} from "@/sysex/frame";

const require = createRequire(import.meta.url);
const BinaryStream = require(
  path.join(
    path.dirname(fileURLToPath(import.meta.url)),
    "../shims/binary-stream.umd.cjs",
  ),
);

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

export function loadSpecFields(
  family: "prog" | "system",
): KaitaiSpecField[] {
  const file =
    family === "prog"
      ? "specification/prog/m7_program_dump.spec.json"
      : "specification/system/m7_system_dump.spec.json";
  const spec = JSON.parse(
    fs.readFileSync(path.join(repo, file), "utf8"),
  ) as { fields: KaitaiSpecField[] };
  return spec.fields;
}

function toArrayBuffer(bytes: Uint8Array): ArrayBuffer {
  return bytes.buffer.slice(
    bytes.byteOffset,
    bytes.byteOffset + bytes.byteLength,
  ) as ArrayBuffer;
}

export function parseProgDump(bytes: Uint8Array): Record<string, unknown> {
  return new M7ProgramDump(new BinaryStream(toArrayBuffer(bytes))) as Record<
    string,
    unknown
  >;
}

export function parseSystemDump(bytes: Uint8Array): Record<string, unknown> {
  return new M7SystemDump(new BinaryStream(toArrayBuffer(bytes))) as Record<
    string,
    unknown
  >;
}

export function assertMessageRoundtrip(
  parsed: Record<string, unknown>,
  raw: Uint8Array,
  fields: KaitaiSpecField[],
  label?: string,
): void {
  const suffix = label ? ` (${label})` : "";
  for (const field of fields) {
    const wire = fieldWireBytes(parsed, field);
    const expected = raw.subarray(field.start, field.end + 1);
    if (wire.length !== expected.length || !wire.every((b, i) => b === expected[i])) {
      throw new Error(
        `${field.id}${suffix}: parsed [${[...wire].map((b) => b.toString(16)).join(" ")}] != raw [${[...expected].map((b) => b.toString(16)).join(" ")}] at [${field.start}, ${field.end}]`,
      );
    }
  }
}

export function assertChecksumMatchesNative(
  parsed: Record<string, unknown>,
  raw: Uint8Array,
  family: "prog" | "system",
): void {
  const expected =
    family === "system" ? systemDumpChecksum(raw) : programDumpChecksum(raw);
  const actual = parsed.checksum as Uint8Array;
  if (!actual || actual.length !== expected.length) {
    throw new Error("checksum field missing or wrong length");
  }
  for (let i = 0; i < expected.length; i++) {
    if (actual[i] !== expected[i]) {
      throw new Error(
        `checksum mismatch at nibble ${i}: parsed ${actual[i]} != native ${expected[i]}`,
      );
    }
  }
}

export function verifyChecksum(
  raw: Uint8Array,
  family: "prog" | "system",
): boolean {
  return family === "system"
    ? verifySystemDumpChecksum(raw)
    : verifyProgramDumpChecksum(raw);
}

/** Split a file that may contain multiple F0…F7 messages. */
export function splitSysexMessages(data: Uint8Array): Uint8Array[] {
  const msgs: Uint8Array[] = [];
  let i = 0;
  while (i < data.length) {
    if (data[i] === 0xf0) {
      let j = i + 1;
      while (j < data.length && data[j] !== 0xf7) {
        j += 1;
      }
      if (j < data.length) {
        msgs.push(data.subarray(i, j + 1));
        i = j + 1;
        continue;
      }
    }
    i += 1;
  }
  return msgs;
}
