// @vitest-environment happy-dom

import { describe, expect, it } from "vitest";
import type { ControlDef } from "@/spec/controls";
import { isTypingTarget } from "@/spec/stepControl";
import {
  resolveControlKeyDown,
  shouldClearSelectionOnPointerDown,
} from "./controlKeyboardAction";

const predelay: ControlDef = {
  fieldId: "predelay",
  label: "predelay",
  parameter: "predelay",
  encoding: "nh",
  offsets: [104, 105],
  entries: [
    { encoded: 0, label: "0 ms" },
    { encoded: 1, label: "2 ms" },
    { encoded: 62, label: "500 ms" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

const size: ControlDef = {
  fieldId: "size",
  label: "size",
  parameter: "size",
  encoding: "nh",
  offsets: [102, 103],
  entries: [
    { encoded: 0, label: "0" },
    { encoded: 1, label: "1" },
    { encoded: 2, label: "2" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

const wetGain: ControlDef = {
  fieldId: "wet_gain",
  label: "wet gain",
  parameter: "wet gain",
  encoding: "nh",
  offsets: [10, 11],
  entries: [
    { encoded: 0, label: "off" },
    { encoded: 1, label: "-1 dB" },
    { encoded: 2, label: "full" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

const progControls = new Map([
  [predelay.fieldId, predelay],
  [size.fieldId, size],
]);
const sysControls = new Map([[wetGain.fieldId, wetGain]]);

const baseInput = {
  selectedFieldId: "predelay",
  activeTab: "prog" as const,
  progEncoded: { predelay: 1, size: 1 },
  sysEncoded: { wet_gain: 1 },
  progControls,
  sysControls,
  isProgParamActive: () => true,
  tempoModeFields: new Set<string>(),
  tempoBpm: 120,
};

describe("resolveControlKeyDown", () => {
  const panel = { tagName: "DIV" } as EventTarget;

  it("clears selection on Escape", () => {
    expect(
      resolveControlKeyDown({ ...baseInput, key: "Escape", target: panel }),
    ).toEqual({ action: "clear" });
  });

  it("ignores keys when nothing is selected", () => {
    expect(
      resolveControlKeyDown({
        ...baseInput,
        selectedFieldId: null,
        key: "ArrowUp",
        target: panel,
      }),
    ).toEqual({ action: "none" });
  });

  it("ignores keys when focus is in an input", () => {
    const input = document.createElement("input");
    expect(isTypingTarget(input)).toBe(true);
    expect(
      resolveControlKeyDown({ ...baseInput, key: "ArrowUp", target: input }),
    ).toEqual({ action: "none" });
  });

  it("steps a program control with arrow keys", () => {
    expect(
      resolveControlKeyDown({ ...baseInput, key: "ArrowUp", target: panel }),
    ).toEqual({
      action: "step",
      family: "prog",
      fieldId: "predelay",
      encoded: 62,
    });
  });

  it("steps a system control on the system tab", () => {
    expect(
      resolveControlKeyDown({
        ...baseInput,
        selectedFieldId: "wet_gain",
        activeTab: "system",
        key: "ArrowUp",
        target: panel,
      }),
    ).toEqual({
      action: "step",
      family: "system",
      fieldId: "wet_gain",
      encoded: 2,
    });
  });

  it("uses tempo stepping when tempo mode is enabled", () => {
    expect(
      resolveControlKeyDown({
        ...baseInput,
        progEncoded: { predelay: 59 },
        tempoModeFields: new Set(["predelay"]),
        key: "ArrowUp",
        target: panel,
      }),
    ).toEqual({
      action: "step",
      family: "prog",
      fieldId: "predelay",
      encoded: 62,
    });
  });

  it("does not step inactive program parameters", () => {
    expect(
      resolveControlKeyDown({
        ...baseInput,
        selectedFieldId: "size",
        key: "ArrowUp",
        target: panel,
        isProgParamActive: (param) => param !== "size",
      }),
    ).toEqual({ action: "none" });
  });

  it("steps in browse mode when encoded value would not change", () => {
    const duplicateStep: ControlDef = {
      fieldId: "dup",
      label: "dup",
      parameter: "size",
      encoding: "nh",
      offsets: [102, 103],
      entries: [
        { encoded: 1, label: "1" },
        { encoded: 2, label: "2a" },
        { encoded: 2, label: "2b" },
      ],
      widget: "knob",
      entryIndex: (enc) => enc,
    };
    expect(
      resolveControlKeyDown({
        ...baseInput,
        selectedFieldId: "dup",
        progEncoded: { dup: 2 },
        progUiState: { mode: "browse", parameter: "size" },
        progControls: new Map([["dup", duplicateStep]]),
        key: "ArrowUp",
        target: panel,
      }),
    ).toEqual({
      action: "step",
      family: "prog",
      fieldId: "dup",
      encoded: 2,
    });
  });
});

describe("shouldClearSelectionOnPointerDown", () => {
  it("does nothing without a selection", () => {
    expect(shouldClearSelectionOnPointerDown(null, false)).toBe(false);
  });

  it("clears when clicking outside a control", () => {
    const outside = { closest: () => null };
    expect(shouldClearSelectionOnPointerDown(outside, true)).toBe(true);
  });

  it("keeps selection when clicking inside a control", () => {
    const inside = { closest: (sel: string) => (sel === "[data-param-control]" ? {} : null) };
    expect(shouldClearSelectionOnPointerDown(inside, true)).toBe(false);
  });

  it("keeps selection when clicking a preserve-selection element", () => {
    const preserve = {
      closest: (sel: string) => (sel === "[data-preserve-selection]" ? {} : null),
    };
    expect(shouldClearSelectionOnPointerDown(preserve, true)).toBe(false);
  });
});
