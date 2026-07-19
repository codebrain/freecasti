import { describe, expect, it } from "vitest";
import {
  crc16Arc,
  packU16BeNibbles,
  programDumpChecksum,
  verifyProgramDumpChecksum,
  verifySystemDumpChecksum,
  bytesToHex,
} from "@/sysex/frame";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

describe("frame checksum helpers", () => {
  it("packs u16 values into big-endian nibbles", () => {
    expect(Array.from(packU16BeNibbles(0x1234))).toEqual([0x1, 0x2, 0x3, 0x4]);
  });

  it("computes stable CRC16 ARC", () => {
    const crc = crc16Arc(new Uint8Array([0x70, 0x08, 0x01]));
    expect(crc).toBeGreaterThan(0);
    expect(crc16Arc(new Uint8Array([0x70, 0x08, 0x01]))).toBe(crc);
  });

  it("verifies skeleton program and system checksums", () => {
    const skeletons = loadSerializeSkeletons();
    expect(verifyProgramDumpChecksum(skeletons.prog)).toBe(true);
    expect(verifySystemDumpChecksum(skeletons.system)).toBe(true);
  });

  it("detects corrupted program checksum", () => {
    const skeletons = loadSerializeSkeletons();
    const corrupt = new Uint8Array(skeletons.prog);
    corrupt[corrupt.length - 5] ^= 0x0f;
    expect(verifyProgramDumpChecksum(corrupt)).toBe(false);
    expect(programDumpChecksum(corrupt)).not.toEqual(
      corrupt.subarray(corrupt.length - 5, corrupt.length - 1),
    );
  });

  it("formats bytes as uppercase hex", () => {
    expect(bytesToHex(new Uint8Array([0xf0, 0x0a]))).toBe("F0 0A");
  });
});
