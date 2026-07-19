import { describe, expect, it } from "vitest";

import type { ControlDef } from "@/spec/controls";
import { allProgControls } from "@/spec/controls";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import {
  dialValueMarkersForControl,
  dialUniformMarkers,
  formatDialMarkerLabel,
  hasUnevenNumericGaps,
  incrementBreakpoints,
} from "./dialValueMarkers";

function controlWithLabels(
  labels: string[],
  parameter = "reverb time",
): ControlDef {
  const entries = labels.map((label, i) => ({ encoded: i, label }));
  return {
    fieldId: "test",
    label: parameter,
    parameter,
    encoding: "nibble_hilo",
    offsets: [0, 1],
    entries,
    widget: "knob",
    entryIndex: (encoded) =>
      Math.max(
        0,
        entries.findIndex((e) => e.encoded === encoded),
      ),
  };
}

describe("incrementBreakpoints", () => {
  it("finds no breakpoints in evenly spaced values", () => {
    expect(incrementBreakpoints([1, 2, 3, 4, 5, 6])).toEqual([]);
  });

  it("finds the junction index where the step size changes", () => {
    // 0.05 steps up to 2, then 0.1 steps: junction at index 4 (value 2).
    expect(incrementBreakpoints([1.9, 1.95, 2, 2.1, 2.2])).toEqual([2]);
  });
});

describe("hasUnevenNumericGaps", () => {
  it("rejects evenly spaced values", () => {
    expect(hasUnevenNumericGaps([1, 2, 3, 4, 5, 6])).toBe(false);
  });

  it("detects reverb-like widening steps", () => {
    const values = [
      0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 3, 5, 10, 20, 30,
    ];
    expect(hasUnevenNumericGaps(values)).toBe(true);
  });
});

describe("formatDialMarkerLabel", () => {
  it("strips units from marker labels", () => {
    expect(formatDialMarkerLabel("0.2", "reverb time")).toBe("0.2");
    expect(formatDialMarkerLabel("2.2", "reverb time")).toBe("2.2");
    expect(formatDialMarkerLabel("30", "reverb time")).toBe("30");
    expect(formatDialMarkerLabel("500 ms", "predelay")).toBe("500");
    expect(formatDialMarkerLabel("4800 Hz", "rolloff")).toBe("4.8k");
    expect(formatDialMarkerLabel("0.5", "lf rt multiply")).toBe("0.5");
    expect(formatDialMarkerLabel("3.0", "lf rt multiply")).toBe("3");
    expect(formatDialMarkerLabel("4.0", "lf rt multiply")).toBe("4");
  });
});

describe("dialUniformMarkers", () => {
  it("labels the perfect middle when one exists", () => {
    expect(dialUniformMarkers(["1/32", "1/16", "1/8"])).toEqual([
      { pct: 0, label: "1/32" },
      { pct: 0.5, label: "1/16" },
      { pct: 1, label: "1/8" },
    ]);
  });

  it("falls back to 4 equally spaced labels without a perfect middle", () => {
    expect(dialUniformMarkers(["1/32", "1/16", "1/8", "1/4"])).toEqual([
      { pct: 0, label: "1/32" },
      { pct: 1 / 3, label: "1/16" },
      { pct: 2 / 3, label: "1/8" },
      { pct: 1, label: "1/4" },
    ]);
  });

  it("stays extremes-only for two labels", () => {
    expect(dialUniformMarkers(["1/32", "1/4"])).toEqual([
      { pct: 0, label: "1/32" },
      { pct: 1, label: "1/4" },
    ]);
  });

  it("needs at least two labels", () => {
    expect(dialUniformMarkers([])).toEqual([]);
    expect(dialUniformMarkers(["1/4"])).toEqual([]);
  });
});

describe("dialValueMarkersForControl", () => {
  it("labels extremes and the perfect middle for odd uniform tables", () => {
    const labels = Array.from({ length: 21 }, (_, i) => String(i));
    const markers = dialValueMarkersForControl(
      controlWithLabels(labels, "size"),
    );
    expect(markers).toEqual([
      { index: 0, pct: 0, label: "0" },
      { index: 10, pct: 0.5, label: "10" },
      { index: 20, pct: 1, label: "20" },
    ]);
  });

  it("uses 4 equally spaced labels for even uniform tables", () => {
    const labels = Array.from({ length: 22 }, (_, i) => String(i));
    const markers = dialValueMarkersForControl(
      controlWithLabels(labels, "size"),
    );
    expect(markers.map((m) => m.index)).toEqual([0, 7, 14, 21]);
    expect(markers[0]?.pct).toBe(0);
    expect(markers[3]?.pct).toBe(1);
  });

  it("labels step-size breakpoints on changing-increment tables", () => {
    // 0.1 steps to 1, then 0.25 steps to 2, then 0.5 steps to 4.
    const labels: string[] = [];
    for (let v = 2; v <= 10; v++) labels.push((v / 10).toFixed(1));
    for (let v = 5; v <= 8; v++) labels.push((v / 4).toFixed(2));
    for (let v = 5; v <= 8; v++) labels.push((v / 2).toFixed(1));
    const markers = dialValueMarkersForControl(
      controlWithLabels(labels, "reverb time"),
    );
    expect(markers.map((m) => m.label)).toEqual(["0.2", "1", "2", "4"]);
    expect(markers[0]?.pct).toBe(0);
    expect(markers[markers.length - 1]?.pct).toBe(1);
  });

  it("marks the real reverb time control at its breakpoints", () => {
    const runtime = loadRuntimeFixture();
    const reverb = allProgControls(runtime.prog).find(
      (c) => c.parameter === "reverb time",
    );
    expect(reverb).toBeTruthy();
    const markers = dialValueMarkersForControl(reverb!);
    // 0.05 → 0.1 → 0.2 → 0.5 → 1.0 second steps.
    expect(markers.map((m) => m.label)).toEqual([
      "0.2",
      "3",
      "6",
      "10",
      "20",
      "30",
    ]);
    expect(markers[0]?.pct).toBe(0);
    expect(markers[markers.length - 1]?.pct).toBe(1);
  });

  it("marks lf rt multiply only where its step size changes", () => {
    const runtime = loadRuntimeFixture();
    const multiply = allProgControls(runtime.prog).find(
      (c) => c.parameter === "lf rt multiply",
    );
    expect(multiply).toBeTruthy();
    // 0.05 steps to 2, then 0.1 steps to 4.
    expect(dialValueMarkersForControl(multiply!).map((m) => m.label)).toEqual([
      "0.2",
      "2",
      "4",
    ]);
  });

  it("keeps non-numeric extremes labeled around a numeric core", () => {
    const runtime = loadRuntimeFixture();
    const rolloff = allProgControls(runtime.prog).find(
      (c) => c.parameter === "rolloff",
    );
    expect(rolloff).toBeTruthy();
    const labels = dialValueMarkersForControl(rolloff!).map((m) => m.label);
    expect(labels[0]).toBe("80");
    expect(labels[labels.length - 1]).toBe("Full");
    // Breakpoints where 40 Hz steps become 80, 200, then 400 Hz steps.
    expect(labels).toContain("400");
    expect(labels).toContain("800");
    expect(labels).toContain("2k");
  });

  it("gives every prog dial labeled extremes", () => {
    const runtime = loadRuntimeFixture();
    for (const control of allProgControls(runtime.prog)) {
      if (control.widget !== "knob") continue;
      if (control.entries.length < 2) continue;
      const markers = dialValueMarkersForControl(control);
      expect(markers.length).toBeGreaterThanOrEqual(2);
      expect(markers.length).toBeLessThanOrEqual(8);
      expect(markers[0]?.pct).toBe(0);
      expect(markers[markers.length - 1]?.pct).toBe(1);
      expect(markers[0]?.label.length).toBeGreaterThan(0);
      expect(markers[markers.length - 1]?.label.length).toBeGreaterThan(0);
      for (let i = 1; i < markers.length; i++) {
        expect(markers[i]!.pct).toBeGreaterThan(markers[i - 1]!.pct);
      }
    }
    const byParam = new Map(
      allProgControls(runtime.prog).map((c) => [
        c.parameter,
        dialValueMarkersForControl(c).map((m) => m.label),
      ]),
    );
    expect(byParam.get("size")).toEqual(["Small", "15", "Large"]);
    expect(byParam.get("predelay")).toEqual(["0", "40", "100", "500"]);
  });
});
