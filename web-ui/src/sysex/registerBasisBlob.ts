/**
 * Register basis blob (program-dump offsets 24-87) decoder.
 *
 * Reg-backed hold-EDIT dumps reuse the factory space-pad region as a
 * bit-packed snapshot of the stored register: the low nibble of each byte
 * (4 bits per byte, MSB first) forms a 256-bit stream holding the register
 * name (14 x 6-bit chars), a store-generation counter, and every stored
 * parameter value including the V2 delay block.
 *
 * The layout is never hard-coded here: it ships in `m7-runtime.json` under
 * the `reg_blob` key, generated from `REGISTER_BLOB_FIELDS` in
 * `m7_sysex.prog.register_blob` (single source of truth). Docs:
 * specification/prog/bytes/register-basis-blob.md
 */

export interface RegBlobFieldLayout {
  id: string;
  label: string;
  /** Bit offset within the 256-bit stream. */
  bit: number;
  width: number;
  /** Spec field id of the live payload twin, when one exists. */
  payloadField?: string;
  /** Wire offsets of the payload twin in the 157-byte frame. */
  payloadOffsets?: number[];
}

export interface RegBlobLayout {
  charset: string;
  name_length: number;
  char_bits: number;
  blob_offset: number;
  blob_length: number;
  fields: RegBlobFieldLayout[];
}

export type RegisterBlobKind = "factory_pad" | "register_basis" | "unknown";

export interface DecodedRegisterBasis {
  name: string;
  /** Encoded integer per scalar field id (everything except `name`). */
  values: Record<string, number>;
  storeCounter: number;
}

export interface StoredVsLiveEntry {
  id: string;
  label: string;
  stored: number;
  live: number;
}

export function blobKind(blob: Uint8Array): RegisterBlobKind {
  if (blob.every((b) => b === 0x20)) return "factory_pad";
  if (blob.every((b) => b <= 0x0f)) return "register_basis";
  return "unknown";
}

export function sliceBlob(frame: Uint8Array, layout: RegBlobLayout): Uint8Array {
  return frame.subarray(layout.blob_offset, layout.blob_offset + layout.blob_length);
}

/**
 * Read `width` bits at `bit` from the low-nibble bitstream.
 *
 * Uses arithmetic (not 32-bit bitwise ops) so widths up to 52 bits are safe.
 */
export function extractBits(blob: Uint8Array, bit: number, width: number): number {
  const firstNibble = Math.floor(bit / 4);
  const lastNibble = Math.floor((bit + width - 1) / 4);
  let value = 0;
  for (let i = firstNibble; i <= lastNibble; i++) {
    value = value * 16 + (blob[i]! & 0x0f);
  }
  const dropRight = (lastNibble + 1) * 4 - (bit + width);
  value = Math.floor(value / 2 ** dropRight);
  return value % 2 ** width;
}

export function decodeRegisterName(blob: Uint8Array, layout: RegBlobLayout): string {
  let name = "";
  for (let i = 0; i < layout.name_length; i++) {
    const code = extractBits(blob, i * layout.char_bits, layout.char_bits);
    name += layout.charset[code] ?? "?";
  }
  return name.replace(/ +$/, "");
}

/**
 * Decode a nibble-packed blob. Returns null when the region is the factory
 * space pad (or anything else that is not a register basis snapshot).
 */
export function decodeRegisterBasisBlob(
  frame: Uint8Array,
  layout: RegBlobLayout,
): DecodedRegisterBasis | null {
  const blob = sliceBlob(frame, layout);
  if (blob.length !== layout.blob_length) return null;
  if (blobKind(blob) !== "register_basis") return null;
  const values: Record<string, number> = {};
  for (const field of layout.fields) {
    if (field.id === "name") continue;
    values[field.id] = extractBits(blob, field.bit, field.width);
  }
  return {
    name: decodeRegisterName(blob, layout),
    values,
    storeCounter: values["store_counter"] ?? 0,
  };
}

export function payloadValue(
  frame: Uint8Array,
  field: RegBlobFieldLayout,
): number | null {
  const offs = field.payloadOffsets;
  if (!offs || !offs.length || field.id === "name") return null;
  if (offs.length === 1) return frame[offs[0]!]!;
  return ((frame[offs[0]!]! & 0x0f) << 4) | (frame[offs[1]!]! & 0x0f);
}

/**
 * Blob (stored) vs payload (live edit buffer) mismatches.
 *
 * Non-empty results flag unstored edits: the blob snapshots the register as
 * stored, while payload bytes track the live edit buffer.
 */
export function storedVsLive(
  frame: Uint8Array,
  layout: RegBlobLayout,
): StoredVsLiveEntry[] {
  const basis = decodeRegisterBasisBlob(frame, layout);
  if (!basis) return [];
  const out: StoredVsLiveEntry[] = [];
  for (const field of layout.fields) {
    const live = payloadValue(frame, field);
    if (live == null) continue;
    const stored = basis.values[field.id];
    if (stored != null && stored !== live) {
      out.push({ id: field.id, label: field.label, stored, live });
    }
  }
  return out;
}
