import { describe, expect, it } from "vitest";

import { dialTickMarkers } from "./Knob";

describe("dialTickMarkers", () => {
  it("returns one marker for a single-step control", () => {
    const ticks = dialTickMarkers(1, 25, 0);
    expect(ticks).toHaveLength(1);
    expect(ticks[0]?.active).toBe(true);
  });

  it("uses every step when count is within the cap", () => {
    expect(dialTickMarkers(5, 25, 0.5)).toHaveLength(5);
  });

  it("caps dense controls with even angular spacing", () => {
    const ticks = dialTickMarkers(27, 25, 0.5);
    expect(ticks).toHaveLength(25);
    const gaps = ticks.slice(1).map((t, i) => t.angle - ticks[i]!.angle);
    for (const gap of gaps) {
      expect(gap).toBeCloseTo(gaps[0]!, 5);
    }
  });

  it("lights markers up to the current value position", () => {
    const ticks = dialTickMarkers(10, 25, 0.5);
    const activeCount = ticks.filter((t) => t.active).length;
    expect(activeCount).toBeGreaterThan(0);
    expect(activeCount).toBeLessThan(ticks.length);
  });
});
