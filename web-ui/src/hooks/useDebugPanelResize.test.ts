import { describe, expect, it } from "vitest";
import {
  clampDebugPanelWidth,
  DEFAULT_DEBUG_PANEL_WIDTH,
  MAX_DEBUG_PANEL_WIDTH,
  MIN_DEBUG_PANEL_WIDTH,
} from "@/hooks/useDebugPanelResize";

describe("clampDebugPanelWidth", () => {
  it("clamps to min, max, and viewport fraction", () => {
    expect(clampDebugPanelWidth(100, 1280)).toBe(MIN_DEBUG_PANEL_WIDTH);
    expect(clampDebugPanelWidth(9999, 1280)).toBe(MAX_DEBUG_PANEL_WIDTH);
    expect(clampDebugPanelWidth(400, 400)).toBe(Math.floor(400 * 0.92));
  });

  it("keeps values inside the allowed range", () => {
    expect(clampDebugPanelWidth(DEFAULT_DEBUG_PANEL_WIDTH, 1280)).toBe(
      DEFAULT_DEBUG_PANEL_WIDTH,
    );
  });
});
