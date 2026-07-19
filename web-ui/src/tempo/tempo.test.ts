import { describe, expect, it } from "vitest";
import type { ControlDef } from "@/spec/controls";
import {
  computeTimingDiscrepancies,
  formatControlTempoValue,
  formatDivisionLabel,
  isTempoParameter,
  MUSICAL_DIVISION_SPECS,
  nearestTempoDivision,
  parseTimeMs,
  snapControlToTempo,
  stepControlTempoEncoded,
  tempoDivisions,
  tempoStepsForControl,
  tempoStepIndexForEncoded,
} from "./tempo";

const predelay: ControlDef = {
  fieldId: "predelay",
  label: "predelay",
  parameter: "predelay",
  encoding: "nh",
  offsets: [104, 105],
  entries: [
    { encoded: 0, label: "0 ms" },
    { encoded: 1, label: "2 ms" },
    { encoded: 59, label: "484 ms" },
    { encoded: 62, label: "500 ms" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

const reverbTime: ControlDef = {
  fieldId: "reverb_time",
  label: "reverb time",
  parameter: "reverb time",
  encoding: "nh",
  offsets: [100, 101],
  entries: [
    { encoded: 0, label: "0.2" },
    { encoded: 40, label: "2.2" },
    { encoded: 136, label: "30" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

const delayTime: ControlDef = {
  fieldId: "delay_time",
  label: "delay time",
  parameter: "delay time",
  encoding: "nh",
  offsets: [120, 121],
  entries: [
    { encoded: 0, label: "100 mSec" },
    { encoded: 1, label: "108 mSec" },
    { encoded: 62, label: "500 mSec" },
  ],
  widget: "knob",
  entryIndex: (enc) => enc,
};

describe("isTempoParameter", () => {
  it("matches time-based program parameters", () => {
    expect(isTempoParameter("predelay")).toBe(true);
    expect(isTempoParameter("reverb time")).toBe(true);
    expect(isTempoParameter("delay time")).toBe(true);
    expect(isTempoParameter("size")).toBe(false);
  });
});

describe("parseTimeMs", () => {
  it("parses ms and seconds", () => {
    expect(parseTimeMs("500 ms")).toBe(500);
    expect(parseTimeMs("100 mSec")).toBe(100);
    expect(parseTimeMs("2.2 s")).toBe(2200);
  });

  it("parses bare seconds for reverb time", () => {
    expect(parseTimeMs("0.2", "reverb time")).toBe(200);
    expect(parseTimeMs("2.2", "reverb time")).toBe(2200);
    expect(parseTimeMs("30", "reverb time")).toBe(30_000);
    expect(parseTimeMs("2.2")).toBeNull();
  });
});

describe("tempoDivisions", () => {
  it("includes straight, triplet, and dotted names at 120 bpm", () => {
    const names = tempoDivisions(120, 2000).map((d) => d.name);
    expect(names).toContain("1/4");
    expect(names).toContain("1/8");
    expect(names).toContain("1/8T");
    expect(names).toContain("1/8D");
    expect(names).not.toContain("4/4");
    expect(names).not.toContain("2/8");
  });

  it("computes eighth straight, triplet, and dotted at 120 bpm", () => {
    const divisions = tempoDivisions(120, 2000);
    const eighth = divisions.find((d) => d.name === "1/8");
    const eighthT = divisions.find((d) => d.name === "1/8T");
    const eighthD = divisions.find((d) => d.name === "1/8D");
    expect(eighth?.ms).toBeCloseTo(250, 1);
    expect(eighthT?.ms).toBeCloseTo(166.67, 1);
    expect(eighthD?.ms).toBeCloseTo(375, 1);
  });

  it("omits musically awkward whole-note and fine dotted divisions", () => {
    const names = tempoDivisions(120, 30_000).map((d) => d.name);
    expect(names).not.toContain("1/1D");
    expect(names).not.toContain("1/1T");
    expect(names).not.toContain("1/32D");
    expect(names).not.toContain("1/32T");
    expect(names).toContain("1/2D");
    expect(names).toContain("1/2T");
  });

  it("uses an explicit musical division catalog", () => {
    expect(MUSICAL_DIVISION_SPECS.length).toBeGreaterThan(10);
    expect(
      MUSICAL_DIVISION_SPECS.some(
        (s) => s.denom === 1 && s.modifier === "straight" && (s.mult ?? 1) === 1,
      ),
    ).toBe(true);
    expect(
      MUSICAL_DIVISION_SPECS.some(
        (s) => s.denom === 1 && s.modifier === "dotted",
      ),
    ).toBe(false);
    expect(
      MUSICAL_DIVISION_SPECS.some(
        (s) => s.denom === 1 && s.modifier === "triplet",
      ),
    ).toBe(false);
  });

  it("includes whole-bar multiples when range allows", () => {
    const labels = tempoDivisions(120, 30_000).map((d) => d.name);
    expect(labels).toContain("1/1");
    expect(labels).toContain("2/1");
    expect(labels).toContain("4/1");
    expect(labels).toContain("8/1");
    expect(labels).not.toContain("16/1");
  });

  it("formats bar counts for display", () => {
    expect(formatDivisionLabel("1/1")).toBe("1");
    expect(formatDivisionLabel("2/1")).toBe("2");
    expect(formatDivisionLabel("8/1")).toBe("8");
    expect(formatDivisionLabel("1/4")).toBe("1/4");
  });

  it("quarter note at 120 bpm is 500 ms", () => {
    const quarter = tempoDivisions(120).find((d) => d.name === "1/4");
    expect(quarter?.ms).toBeCloseTo(500, 1);
  });
});

describe("nearestTempoDivision", () => {
  it("snaps 480 ms near 1/4 at 120 bpm", () => {
    expect(nearestTempoDivision(480, 120)?.name).toBe("1/4");
  });
});

describe("tempoStepsForControl", () => {
  it("limits steps to control time range and unique encodings", () => {
    const steps = tempoStepsForControl(predelay, 120);
    expect(steps.length).toBeGreaterThan(0);
    expect(steps.length).toBeLessThan(tempoDivisions(120, 500).length);
    expect(new Set(steps.map((s) => s.encoded)).size).toBe(steps.length);
    for (const step of steps) {
      expect(step.division.ms).toBeLessThanOrEqual(500);
    }
  });

  it("builds steps for reverb time with bare-second labels", () => {
    const steps = tempoStepsForControl(reverbTime, 120);
    expect(steps.length).toBeGreaterThan(0);
    expect(steps.every((s) => s.division.ms >= 200 && s.division.ms <= 30_000)).toBe(
      true,
    );
    expect(snapControlToTempo(reverbTime, 40, 120)).toBe(40);
  });
});

describe("tempoStepIndexForEncoded", () => {
  it("resolves encoded value to a step index", () => {
    const steps = tempoStepsForControl(predelay, 120);
    const quarter = steps.find((s) => s.encoded === 62);
    expect(quarter).toBeDefined();
    expect(tempoStepIndexForEncoded(predelay, 62, 120)).toBe(
      steps.indexOf(quarter!),
    );
  });
});

describe("snapControlToTempo", () => {
  it("picks nearest table entry to tempo grid", () => {
    expect(snapControlToTempo(predelay, 59, 120)).toBe(62);
  });
});

describe("stepControlTempoEncoded", () => {
  it("steps through adjacent tempo divisions", () => {
    const steps = tempoStepsForControl(predelay, 120);
    expect(steps.length).toBeGreaterThan(2);
    const mid = Math.floor(steps.length / 2);
    const current = steps[mid].encoded;
    const prev = steps[mid - 1].encoded;
    const next = steps[mid + 1].encoded;
    expect(prev).not.toBe(current);
    expect(next).not.toBe(current);
    expect(stepControlTempoEncoded(predelay, current, -1, 120)).toBe(prev);
    expect(stepControlTempoEncoded(predelay, current, 1, 120)).toBe(next);
  });

  it("returns null at tempo step bounds", () => {
    const steps = tempoStepsForControl(predelay, 120);
    const first = steps[0].encoded;
    expect(stepControlTempoEncoded(predelay, first, -1, 120)).toBeNull();
  });
});

describe("formatControlTempoValue", () => {
  it("formats predelay as nearest division label", () => {
    expect(formatControlTempoValue(predelay, 62, 120)).toBe("1/4");
  });

  it("formats reverb time with bare-second labels", () => {
    expect(formatControlTempoValue(reverbTime, 40, 120)).toBeTruthy();
  });
});

describe("delay time tempo support", () => {
  it("parses mSec labels and builds tempo steps", () => {
    expect(parseTimeMs("500 mSec")).toBe(500);
    const steps = tempoStepsForControl(delayTime, 120);
    expect(steps.length).toBeGreaterThan(0);
    expect(steps.some((s) => s.encoded === 62)).toBe(true);
  });
});

describe("computeTimingDiscrepancies", () => {
  it("reports mismatch between ideal and device value", () => {
    const discrepancies = computeTimingDiscrepancies(
      [predelay],
      { predelay: 59 },
      120,
      new Set(["predelay"]),
    );
    expect(discrepancies).toHaveLength(1);
    expect(discrepancies[0].division).toBe("1/4");
    expect(discrepancies[0].actualLabel).toBe("484 ms");
  });
});
