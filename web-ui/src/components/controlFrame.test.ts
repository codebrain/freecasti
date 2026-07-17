import { describe, expect, it } from "vitest";
import { controlSelectFrameClass } from "@/components/controlFrame";

describe("controlSelectFrameClass", () => {
  it("dims disabled controls with transparency", () => {
    expect(controlSelectFrameClass(true)).toContain("opacity-45");
    expect(controlSelectFrameClass(true)).toContain("cursor-not-allowed");
  });

  it("keeps enabled controls fully opaque", () => {
    expect(controlSelectFrameClass(false)).toContain("cursor-pointer");
    expect(controlSelectFrameClass(false)).not.toContain("opacity-");
  });
});
