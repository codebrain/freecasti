import { describe, expect, it } from "vitest";
import {
  clampTempoBpm,
  commitTempoBpmDraft,
  sanitizeTempoDraft,
} from "./tempoBpm";

describe("tempoInput", () => {
  it("sanitizeTempoDraft strips non-digits", () => {
    expect(sanitizeTempoDraft("12a3")).toBe("123");
    expect(sanitizeTempoDraft(" 85 ")).toBe("85");
  });

  it("commitTempoBpmDraft allows multi-digit entry before clamp", () => {
    expect(commitTempoBpmDraft("1", 120)).toBe(20);
    expect(commitTempoBpmDraft("12", 120)).toBe(20);
    expect(commitTempoBpmDraft("120", 120)).toBe(120);
    expect(commitTempoBpmDraft("85", 120)).toBe(85);
  });

  it("commitTempoBpmDraft clamps extremes", () => {
    expect(commitTempoBpmDraft("999", 120)).toBe(300);
    expect(commitTempoBpmDraft("5", 120)).toBe(20);
  });

  it("commitTempoBpmDraft falls back on empty", () => {
    expect(commitTempoBpmDraft("", 96)).toBe(96);
    expect(commitTempoBpmDraft("   ", 96)).toBe(96);
  });

  it("clampTempoBpm bounds", () => {
    expect(clampTempoBpm(0)).toBe(20);
    expect(clampTempoBpm(400)).toBe(300);
    expect(clampTempoBpm(120)).toBe(120);
  });
});
