import { describe, expect, it } from "vitest";
import { buildParamChange, diffByteOffsets, labelForEncoded, rowTouchesChangedOffsets } from "@/debug/change";
import { buildSystemControls } from "@/spec/controls";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("diffByteOffsets", () => {
  it("returns indices where bytes differ", () => {
    const prev = new Uint8Array([0xf0, 0x00, 0x62, 0x63]);
    const next = new Uint8Array([0xf0, 0x01, 0x62, 0x63]);
    expect(diffByteOffsets(prev, next)).toEqual([1]);
  });
});

describe("rowTouchesChangedOffsets", () => {
  it("matches rows that overlap changed offsets", () => {
    const row = { offsets: [10, 11, 12] };
    expect(rowTouchesChangedOffsets(row, [11])).toBe(true);
    expect(rowTouchesChangedOffsets(row, [20])).toBe(false);
  });
});

describe("buildParamChange", () => {
  it("captures before/after labels for a system control", () => {
    const runtime = loadRuntimeFixture();
    const wet = buildSystemControls(runtime.system).find(
      (c) => c.parameter === "wet gain",
    )!;
    const before = wet.entries[0].encoded;
    const after = wet.entries[1]?.encoded ?? before;
    const change = buildParamChange(wet, before, after);
    expect(change.fieldId).toBe(wet.fieldId);
    expect(change.beforeLabel).toBe(labelForEncoded(wet, before));
    expect(change.afterLabel).toBe(labelForEncoded(wet, after));
  });
});

