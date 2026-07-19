import { describe, expect, it } from "vitest";
import {
  decodeAtOffsets,
  encodeAtOffsets,
  nibbleHilo,
  nibbleLohi,
} from "@/sysex/encodings";

describe("encodings", () => {
  it("nibble_hilo roundtrip", () => {
    expect(nibbleHilo(0x03, 0x0a)).toBe(0x3a);
    const wire = encodeAtOffsets(0x3a, "nibble_hilo", 2);
    expect(decodeAtOffsets(new Uint8Array(wire), [0, 1], "nibble_hilo")).toBe(
      0x3a,
    );
  });

  it("nibble_lohi roundtrip", () => {
    const enc = 0x3a;
    const wire = encodeAtOffsets(enc, "nibble_lohi", 2);
    expect(decodeAtOffsets(new Uint8Array(wire), [0, 1], "nibble_lohi")).toBe(
      enc,
    );
  });

  it("raw_u8 roundtrip", () => {
    const wire = encodeAtOffsets(7, "raw_u8", 1);
    expect(wire).toEqual([7]);
  });

  it("nibble_hilo pack matches corpus style", () => {
    expect(encodeAtOffsets(0x3a, "nibble_hilo", 2)).toEqual([0x03, 0x0a]);
    expect(encodeAtOffsets(70, "nibble_hilo", 2)).toEqual([0x04, 0x06]);
  });

  it("nibble_lohi identity", () => {
    expect(nibbleLohi(0x0a, 0x03)).toBe(0x3a);
  });
});
