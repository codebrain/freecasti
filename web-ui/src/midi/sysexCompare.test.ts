import { describe, expect, it } from "vitest";

import { sysexByteDiffCount, sysexBytesEqual } from "./sysexCompare";

describe("sysexCompare", () => {
  it("compares equal byte arrays", () => {
    const a = new Uint8Array([0xf0, 1, 2, 0xf7]);
    expect(sysexBytesEqual(a, new Uint8Array(a))).toBe(true);
  });

  it("detects length and byte differences", () => {
    const a = new Uint8Array([0xf0, 1, 2, 0xf7]);
    const b = new Uint8Array([0xf0, 1, 3, 0xf7]);
    expect(sysexBytesEqual(a, b)).toBe(false);
    expect(sysexByteDiffCount(a, b)).toBe(1);
    expect(sysexByteDiffCount(a, new Uint8Array([0xf0, 1]))).toBe(2);
  });
});
