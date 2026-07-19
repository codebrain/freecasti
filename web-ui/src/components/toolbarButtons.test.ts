import { describe, expect, it } from "vitest";
import {
  toolbarButtonClass,
  toolbarSegmentButtonClass,
} from "./toolbarButtons";

describe("toolbarButtons", () => {
  it("applies LED accent styling when active", () => {
    expect(toolbarButtonClass(true)).toContain("color-led");
    expect(toolbarButtonClass(true)).toContain("color-primary");
  });

  it("uses muted chrome when idle", () => {
    expect(toolbarButtonClass(false)).toContain("color-label");
    expect(toolbarButtonClass(false)).not.toContain("color-led");
  });

  it("dims disabled buttons", () => {
    expect(toolbarButtonClass(false, true)).toContain("cursor-not-allowed");
    expect(toolbarButtonClass(true, true)).toContain("opacity-35");
  });

  it("rounds segment edges independently", () => {
    expect(toolbarSegmentButtonClass(true, "start")).toContain("rounded-l");
    expect(toolbarSegmentButtonClass(false, "end")).toContain("rounded-r");
  });
});
