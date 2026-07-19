import { describe, expect, it } from "vitest";
import { computeDialWheelStepIndex } from "@/controls/dialWheel";

describe("computeDialWheelStepIndex", () => {
  it("steps up on negative deltaY", () => {
    expect(computeDialWheelStepIndex(10, -100, 100, false)).toBeGreaterThan(10);
  });

  it("steps down on positive deltaY", () => {
    expect(computeDialWheelStepIndex(10, 100, 100, false)).toBeLessThan(10);
  });

  it("returns null when clamped at boundary", () => {
    expect(computeDialWheelStepIndex(0, 100, 100, false)).toBeNull();
    expect(computeDialWheelStepIndex(100, -100, 100, false)).toBeNull();
  });

  it("uses single-step magnitude with shift key", () => {
    expect(computeDialWheelStepIndex(5, -100, 100, true)).toBe(6);
    expect(computeDialWheelStepIndex(5, 100, 100, true)).toBe(4);
  });
});
