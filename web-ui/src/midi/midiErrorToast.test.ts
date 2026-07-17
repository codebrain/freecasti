import { describe, expect, it } from "vitest";

import { shouldShowMidiError } from "./midiErrorToast";

describe("shouldShowMidiError", () => {
  it("shows when MIDI is enabled and there is an error", () => {
    expect(shouldShowMidiError(true, "No MIDI output selected")).toBe(true);
  });

  it("hides when MIDI is off even if an error is stored", () => {
    expect(shouldShowMidiError(false, "No MIDI output selected")).toBe(false);
  });

  it("hides when there is no error", () => {
    expect(shouldShowMidiError(true, null)).toBe(false);
  });
});
