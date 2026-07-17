import { describe, expect, it } from "vitest";
import type { ControlDef } from "./controls";
import { arrowKeyDelta, stepControlEncoded } from "./stepControl";

const knob: ControlDef = {
  fieldId: "size",
  label: "size",
  parameter: "size",
  encoding: "raw_u8",
  offsets: [0],
  entries: [
    { encoded: 0, label: "a" },
    { encoded: 1, label: "b" },
    { encoded: 2, label: "c" },
  ],
  widget: "knob",
  entryIndex: (enc) => Math.max(0, enc),
};

describe("stepControlEncoded", () => {
  it("steps within entry range", () => {
    expect(stepControlEncoded(knob, 1, 1)).toBe(2);
    expect(stepControlEncoded(knob, 1, -1)).toBe(0);
    expect(stepControlEncoded(knob, 0, -1)).toBeNull();
    expect(stepControlEncoded(knob, 2, 1)).toBeNull();
  });
});

describe("arrowKeyDelta", () => {
  it("maps arrow keys to deltas", () => {
    expect(arrowKeyDelta("ArrowUp")).toBe(1);
    expect(arrowKeyDelta("ArrowRight")).toBe(1);
    expect(arrowKeyDelta("ArrowDown")).toBe(-1);
    expect(arrowKeyDelta("ArrowLeft")).toBe(-1);
    expect(arrowKeyDelta("Enter")).toBeNull();
  });
});
