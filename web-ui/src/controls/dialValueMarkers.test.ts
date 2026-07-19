import { describe, expect, it } from "vitest";

import type { ControlDef } from "@/spec/controls";
import { allProgControls } from "@/spec/controls";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import {
  dialValueMarkersForControl,
  dialExtremeMarkers,
  formatDialMarkerLabel,
  hasUnevenNumericGaps,
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
  });
});

describe("dialExtremeMarkers", () => {
  it("labels first and last only", () => {
    expect(dialExtremeMarkers(["1/32", "1/16", "1/8", "1/4"])).toEqual([
      { pct: 0, label: "1/32" },
      { pct: 1, label: "1/4" },
    ]);
  });

  it("needs at least two labels", () => {
    expect(dialExtremeMarkers([])).toEqual([]);
    expect(dialExtremeMarkers(["1/4"])).toEqual([]);
  });
});

describe("dialValueMarkersForControl", () => {
  it("shows extreme labels for even integer steps", () => {
    const labels = Array.from({ length: 21 }, (_, i) => String(i));
    const markers = dialValueMarkersForControl(
      controlWithLabels(labels, "size"),
    );
    expect(markers).toEqual([
      { index: 0, pct: 0, label: "0" },
      { index: 20, pct: 1, label: "20" },
    ]);
  });

  it("places labeled markers on uneven reverb-time style tables", () => {
    // Sparse stand-in for the real non-linear reverb time table.
    const labels = [
      "0.2",
      "0.25",
      "0.3",
      "0.4",
      "0.5",
      "0.6",
      "0.8",
      "1",
      "1.5",
      "2",
      "2.5",
      "3",
      "4",
      "5",
      "6",
      "8",
      "10",
      "15",
      "20",
      "25",
      "30",
    ];
    const markers = dialValueMarkersForControl(
      controlWithLabels(labels, "reverb time"),
    );
    expect(markers.length).toBeGreaterThanOrEqual(4);
    expect(markers.length).toBeLessThanOrEqual(7);
    expect(markers[0]?.label).toBe("0.2");
    expect(markers[markers.length - 1]?.label).toBe("30");
    expect(markers[0]?.pct).toBe(0);
    expect(markers[markers.length - 1]?.pct).toBe(1);
    // Landmark values should appear somewhere on the ring.
    const texts = markers.map((m) => m.label);
    expect(texts.some((t) => t === "1" || t === "2" || t === "5" || t === "10")).toBe(
      true,
    );
    // Positions must be strictly increasing.
    for (let i = 1; i < markers.length; i++) {
      expect(markers[i]!.pct).toBeGreaterThan(markers[i - 1]!.pct);
    }
  });

  it("marks the real reverb time control from the runtime fixture", () => {
    const runtime = loadRuntimeFixture();
    const reverb = allProgControls(runtime.prog).find(
      (c) => c.parameter === "reverb time",
    );
    expect(reverb).toBeTruthy();
    const markers = dialValueMarkersForControl(reverb!);
    expect(markers.length).toBeGreaterThanOrEqual(4);
    expect(markers[0]?.pct).toBe(0);
    expect(markers[markers.length - 1]?.pct).toBe(1);
    expect(markers[markers.length - 1]?.label).toBe("30");
  });

  it("gives every prog dial extreme labels; uneven ones get more", () => {
    const runtime = loadRuntimeFixture();
    for (const control of allProgControls(runtime.prog)) {
      if (control.widget !== "knob") continue;
      if (control.entries.length < 2) continue;
      const markers = dialValueMarkersForControl(control);
      expect(markers.length).toBeGreaterThanOrEqual(2);
      expect(markers[0]?.pct).toBe(0);
      expect(markers[markers.length - 1]?.pct).toBe(1);
      expect(markers[0]?.label.length).toBeGreaterThan(0);
      expect(markers[markers.length - 1]?.label.length).toBeGreaterThan(0);
    }
    const byParam = new Map(
      allProgControls(runtime.prog).map((c) => [
        c.parameter,
        dialValueMarkersForControl(c).map((m) => m.label),
      ]),
    );
    expect(byParam.get("reverb time")?.length ?? 0).toBeGreaterThanOrEqual(4);
    expect(byParam.get("reverb time")).toContain("1");
    expect(byParam.get("reverb time")).toContain("10");
    expect(byParam.get("size")?.length).toBe(2);
    expect(byParam.get("size")?.[0]).toBeTruthy();
    expect(byParam.get("size")?.at(-1)).toBeTruthy();
  });
});
