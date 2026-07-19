/**
 * Serialize Kaitai-parsed M7 dump objects back to on-wire SysEx bytes.
 * Mirrors ``m7_sysex.kaitai_encode`` (Python).
 */

import { specIdToParserKey } from "./kaitaiFieldId";
import {
  PROGRAM_MESSAGE_LENGTH,
  SYSTEM_MESSAGE_LENGTH,
  writeProgramDumpChecksum,
  writeSystemDumpChecksum,
} from "./frame";

export interface KaitaiSpecField {
  id: string;
  start: number;
  end: number;
  encoding?: string | null;
  kind?: string;
  size?: number;
  contents?: number[];
}

interface NibblePair {
  hiNibble: number;
  loNibble: number;
}

function asUint8Array(val: unknown): Uint8Array {
  if (val instanceof Uint8Array) return val;
  if (Array.isArray(val)) return Uint8Array.from(val);
  throw new TypeError(`expected byte array, got ${typeof val}`);
}

function isNibblePair(val: unknown): val is NibblePair {
  return (
    typeof val === "object" &&
    val !== null &&
    "hiNibble" in val &&
    "loNibble" in val
  );
}

export function fieldWireBytes(
  parsed: Record<string, unknown>,
  field: KaitaiSpecField,
): Uint8Array {
  const key = specIdToParserKey(field.id);
  const val = parsed[key];

  if (field.contents != null) {
    return Uint8Array.from(field.contents);
  }

  if (field.kind === "checksum") {
    return asUint8Array(parsed.checksum);
  }

  if (field.kind === "string" || field.encoding === "ascii_space_padded") {
    const str = String(val ?? "");
    const size = field.size ?? field.end - field.start + 1;
    const out = new Uint8Array(size).fill(0x20);
    const enc = new TextEncoder().encode(str);
    out.set(enc.subarray(0, size));
    return out;
  }

  if (field.encoding === "nibble_hilo" || isNibblePair(val)) {
    const nibble = val as NibblePair;
    return Uint8Array.from([nibble.hiNibble, nibble.loNibble]);
  }

  if (field.encoding === "nibble_lohi" && isNibblePair(val)) {
    const nibble = val as NibblePair;
    return Uint8Array.from([nibble.loNibble, nibble.hiNibble]);
  }

  if (typeof val === "number") {
    return Uint8Array.from([val & 0xff]);
  }

  if (val instanceof Uint8Array || Array.isArray(val)) {
    return asUint8Array(val);
  }

  // Nested types that wrap raw wire bytes (e.g. register_basis_blob).
  if (
    val &&
    typeof val === "object" &&
    "data" in val &&
    ((val as { data: unknown }).data instanceof Uint8Array ||
      Array.isArray((val as { data: unknown }).data))
  ) {
    return asUint8Array((val as { data: unknown }).data);
  }

  if (val && typeof val === "object" && "value" in val) {
    const inner = (val as { value: unknown }).value;
    if (typeof inner === "number") {
      return Uint8Array.from([inner & 0xff]);
    }
    if (isNibblePair(inner)) {
      return Uint8Array.from([inner.hiNibble, inner.loNibble]);
    }
  }

  throw new TypeError(
    `cannot extract wire bytes for field ${field.id}: ${typeof val}`,
  );
}

export function serializeParsedDump(
  parsed: Record<string, unknown>,
  fields: KaitaiSpecField[],
  options: { system?: boolean; messageLength?: number } = {},
): Uint8Array {
  const system = options.system ?? false;
  const messageLength =
    options.messageLength ??
    (system ? SYSTEM_MESSAGE_LENGTH : PROGRAM_MESSAGE_LENGTH);

  const buf = new Uint8Array(messageLength);
  for (const field of fields) {
    if (field.kind === "checksum") continue;
    const wire = fieldWireBytes(parsed, field);
    const start = field.start;
    const end = field.end;
    const span = end - start + 1;
    if (wire.length !== span) {
      throw new Error(
        `field ${field.id}: wire length ${wire.length} != span ${span}`,
      );
    }
    buf.set(wire, start);
  }

  if (system) {
    writeSystemDumpChecksum(buf);
  } else {
    writeProgramDumpChecksum(buf);
  }
  return buf;
}
