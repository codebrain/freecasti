import { describe, expect, it } from "vitest";import {
  base64ToBytes,
  bytesToBase64,
  downloadSyx,
  parseSyxBytes,
  readSyxFromBuffer,
  suggestSyxFilename,
} from "@/sysex/syxIo";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

describe("syxIo", () => {  it("parseSyxBytes accepts valid program skeleton", () => {
    const raw = loadSerializeSkeletons().prog;
    const bytes = parseSyxBytes(raw);
    expect(bytes.length).toBe(157);
    expect(bytes[0]).toBe(0xf0);
    expect(bytes[bytes.length - 1]).toBe(0xf7);
  });

  it("parseSyxBytes rejects invalid framing", () => {
    expect(() => parseSyxBytes(new Uint8Array([0x00]))).toThrow(/F0/);
  });

  it("readSyxFromBuffer roundtrips", () => {
    const raw = loadSerializeSkeletons().system;
    const bytes = readSyxFromBuffer(raw);
    expect(bytes.length).toBe(77);
  });

  it("base64 roundtrip preserves bytes", () => {
    const raw = new Uint8Array([0xf0, 0x00, 0x62, 0xf7]);
    expect(base64ToBytes(bytesToBase64(raw))).toEqual(raw);
  });

  it("suggestSyxFilename sanitizes program name", () => {
    expect(suggestSyxFilename("prog", "Large Hall")).toBe("Large Hall.syx");
    expect(suggestSyxFilename("system")).toBe("m7-system.syx");
  });

  it("downloadSyx invokes link click with blob url", () => {
    const clicks: string[] = [];
    downloadSyx({
      bytes: new Uint8Array([0xf0, 0xf7]),
      filename: "test.syx",
      createObjectURL: () => "blob:test",
      revokeObjectURL: () => {},
      createAnchor: () =>
        ({ href: "", download: "" }) as HTMLAnchorElement,
      clickLink: (a) => clicks.push(`${a.download}:${a.href}`),
    });
    expect(clicks).toEqual(["test.syx:blob:test"]);
  });
});
