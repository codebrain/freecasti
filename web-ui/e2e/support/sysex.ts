/**
 * Minimal, independent checks that a byte buffer is a well-formed Bricasti M7
 * SysEx dump. Deliberately re-implemented here (rather than importing app
 * code) so the tests stay an outside observer of the editor's output.
 */

const SYSEX_START = 0xf0;
const SYSEX_END = 0xf7;
const BRICASTI_MFR_ID = [0x00, 0x62, 0x63];
const PROGRAM_DUMP_HEADER = [0x70, 0x08, 0x01, 0x00];
const SYSTEM_DUMP_HEADER = [0x70, 0x08, 0x02, 0x00];
const PROGRAM_MESSAGE_LENGTH = 157;
const SYSTEM_MESSAGE_LENGTH = 77;

function crc16Arc(data: Uint8Array): number {
  let crc = 0x0000;
  for (const byte of data) {
    crc ^= byte;
    for (let i = 0; i < 8; i++) {
      crc = crc & 0x0001 ? (crc >> 1) ^ 0xa001 : crc >> 1;
    }
  }
  return crc & 0xffff;
}

function nibblesOf(value: number): number[] {
  return [(value >> 12) & 0x0f, (value >> 8) & 0x0f, (value >> 4) & 0x0f, value & 0x0f];
}

function hasHeader(bytes: Uint8Array, header: number[]): boolean {
  if (bytes[0] !== SYSEX_START || bytes[bytes.length - 1] !== SYSEX_END) return false;
  const expected = [...BRICASTI_MFR_ID, ...header];
  return expected.every((b, i) => bytes[i + 1] === b);
}

export function isProgramDump(bytes: Uint8Array): boolean {
  return bytes.length === PROGRAM_MESSAGE_LENGTH && hasHeader(bytes, PROGRAM_DUMP_HEADER);
}

export function isSystemDump(bytes: Uint8Array): boolean {
  return bytes.length === SYSTEM_MESSAGE_LENGTH && hasHeader(bytes, SYSTEM_DUMP_HEADER);
}

export function programChecksumValid(bytes: Uint8Array): boolean {
  const checksumStart = bytes.length - 5;
  const cover = bytes.subarray(8, checksumStart);
  const expected = nibblesOf(crc16Arc(cover));
  return expected.every((b, i) => bytes[checksumStart + i] === b);
}

export function systemChecksumValid(bytes: Uint8Array): boolean {
  const cover = bytes.subarray(8, 72);
  const expected = nibblesOf(crc16Arc(cover));
  return expected.every((b, i) => bytes[72 + i] === b);
}

export function bytesEqual(a: Uint8Array, b: Uint8Array): boolean {
  return a.length === b.length && a.every((byte, i) => byte === b[i]);
}
