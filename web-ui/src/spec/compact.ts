import type { DumpSpec, SpecField, ValueMapEntry } from "./types";

const ENCODING_EXPAND: Record<string, string> = {
  nh: "nibble_hilo",
  nl: "nibble_lohi",
  u8: "raw_u8",
  as: "ascii_space_padded",
  rb: "raw_bytes",
};

export interface CompactSpec {
  n: number;
  f: CompactField[];
}

interface CompactField {
  id: string;
  s: number;
  e?: string;
  p?: string;
  z?: number;
  m?: [number, string][];
}

function spanBytes(encoding: string, size?: number): number {
  switch (encoding) {
    case "nibble_hilo":
    case "nibble_lohi":
      return 2;
    case "raw_u8":
      return 1;
    case "ascii_space_padded":
    case "raw_bytes":
      return size ?? 1;
    default:
      return 1;
  }
}

function expandField(raw: CompactField): SpecField {
  const encoding = raw.e ? ENCODING_EXPAND[raw.e] ?? raw.e : null;
  const sized =
    encoding === "ascii_space_padded" || encoding === "raw_bytes"
      ? raw.z
      : undefined;
  const end =
    sized != null
      ? raw.s + sized - 1
      : raw.s + spanBytes(encoding ?? "raw_u8", raw.z) - 1;
  const field: SpecField = {
    id: raw.id,
    label: raw.p ?? raw.id,
    parameter: raw.p,
    offsets:
      encoding === "ascii_space_padded" || encoding === "raw_bytes"
        ? Array.from({ length: end - raw.s + 1 }, (_, i) => raw.s + i)
        : Array.from({ length: end - raw.s + 1 }, (_, i) => raw.s + i),
    start: raw.s,
    end,
    encoding,
    kind: encoding === "ascii_space_padded" ? "string" : undefined,
    size: raw.z,
  };
  if (raw.m?.length) {
    const entries: ValueMapEntry[] = raw.m.map(([encoded, label]) => ({
      encoded,
      label,
    }));
    field.value_map = { entries };
  }
  return field;
}

export function expandCompactSpec(raw: CompactSpec): DumpSpec {
  return {
    format: "compact",
    version: 1,
    message_length: raw.n,
    fields: raw.f.map(expandField),
  };
}

export function isCompactSpec(data: unknown): data is CompactSpec {
  return (
    typeof data === "object" &&
    data !== null &&
    "n" in data &&
    "f" in data &&
    Array.isArray((data as CompactSpec).f)
  );
}
