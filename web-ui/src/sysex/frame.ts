export const SYSEX_START = 0xf0;
export const SYSEX_END = 0xf7;
export const BRICASTI_MFR_ID = [0x00, 0x62, 0x63] as const;
export const PROGRAM_DUMP_HEADER = [0x70, 0x08, 0x01, 0x00] as const;
export const SYSTEM_DUMP_HEADER = [0x70, 0x08, 0x02, 0x00] as const;

export const NAME_OFFSET = 8;
export const PROGRAM_NAME_LENGTH = 16;
/** Manual/UI editable label length (14-character location display). */
export const PROGRAM_NAME_EDITABLE_LENGTH = 14;
export const REGISTER_BASIS_BLOB_OFFSET = 24;
export const REGISTER_BASIS_BLOB_LENGTH = 64;
/** Factory space-padded window (name + trailing spaces through 87). */
export const NAME_REGION_LENGTH =
  PROGRAM_NAME_LENGTH + REGISTER_BASIS_BLOB_LENGTH;
/** @deprecated Prefer PROGRAM_NAME_LENGTH for display name; NAME_REGION_LENGTH for factory window. */
export const NAME_LENGTH = NAME_REGION_LENGTH;
export const DATA_OFFSET = NAME_OFFSET + NAME_REGION_LENGTH;
export const PROGRAM_MESSAGE_LENGTH = 157;

export const SYSTEM_PAYLOAD_OFFSET = 8;
export const SYSTEM_MESSAGE_LENGTH = 77;
export const SYSTEM_CHECKSUM_COVER_START = SYSTEM_PAYLOAD_OFFSET;
export const SYSTEM_CHECKSUM_COVER_END = 72;

export const CHECKSUM_NIBBLE_COUNT = 4;
export const CHECKSUM_COVER_START = NAME_OFFSET;

export function crc16Arc(data: Uint8Array | number[]): number {
  let crc = 0x0000;
  for (const byte of data) {
    crc ^= byte;
    for (let i = 0; i < 8; i++) {
      if (crc & 0x0001) {
        crc = (crc >> 1) ^ 0xa001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc & 0xffff;
}

export function packU16BeNibbles(value: number): Uint8Array {
  const v = value & 0xffff;
  return new Uint8Array([
    (v >> 12) & 0x0f,
    (v >> 8) & 0x0f,
    (v >> 4) & 0x0f,
    v & 0x0f,
  ]);
}

export function programDumpChecksum(raw: Uint8Array): Uint8Array {
  const checksumStart = raw.length - 1 - CHECKSUM_NIBBLE_COUNT;
  const cover = raw.subarray(CHECKSUM_COVER_START, checksumStart);
  return packU16BeNibbles(crc16Arc(cover));
}

export function writeProgramDumpChecksum(buf: Uint8Array): void {
  const checksumStart = buf.length - 1 - CHECKSUM_NIBBLE_COUNT;
  buf.set(programDumpChecksum(buf), checksumStart);
}

export function verifyProgramDumpChecksum(raw: Uint8Array): boolean {
  const checksumStart = raw.length - 1 - CHECKSUM_NIBBLE_COUNT;
  const actual = raw.subarray(checksumStart, checksumStart + CHECKSUM_NIBBLE_COUNT);
  const expected = programDumpChecksum(raw);
  return actual.every((b, i) => b === expected[i]);
}

export function systemDumpChecksum(raw: Uint8Array): Uint8Array {
  const cover = raw.subarray(
    SYSTEM_CHECKSUM_COVER_START,
    SYSTEM_CHECKSUM_COVER_END,
  );
  return packU16BeNibbles(crc16Arc(cover));
}

export function writeSystemDumpChecksum(buf: Uint8Array): void {
  buf.set(
    systemDumpChecksum(buf),
    SYSTEM_CHECKSUM_COVER_END,
  );
}

export function verifySystemDumpChecksum(raw: Uint8Array): boolean {
  const actual = raw.subarray(
    SYSTEM_CHECKSUM_COVER_END,
    SYSTEM_CHECKSUM_COVER_END + CHECKSUM_NIBBLE_COUNT,
  );
  const expected = systemDumpChecksum(raw);
  return actual.every((b, i) => b === expected[i]);
}

export function bytesToHex(data: Uint8Array, sep = " "): string {
  return Array.from(data, (b) => b.toString(16).toUpperCase().padStart(2, "0")).join(sep);
}
