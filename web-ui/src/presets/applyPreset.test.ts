import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { applyPreset, applyPresetPreservingLocks, mergeLockedProgFields } from "@/presets/applyPreset";
import { expandPresetCatalog, type CompactPresetRow } from "@/presets/compact";
import { buildParameterToFieldId } from "@/spec/controls";
import { PROG_PARAM_ORDER } from "@/spec/param-order";
import type { DumpSpec } from "@/spec/types";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

interface FullPresetDump {
  presets: Array<{
    bank: string;
    preset: string;
    name_field: string;
    bank_index: number;
    program_slot: number;
    parameters: Record<string, { encoded: number }>;
  }>;
}

function compactFromFull(presetsFull: FullPresetDump) {
  const byIndex: Record<number, string> = {};
  for (const entry of presetsFull.presets) {
    byIndex[entry.bank_index] = entry.bank;
  }
  const banks = Object.keys(byIndex)
    .map(Number)
    .sort((a, b) => a - b)
    .map((i) => byIndex[i]);
  const presets = presetsFull.presets.map(
    (entry): CompactPresetRow => [
      entry.bank_index,
      entry.program_slot,
      entry.name_field,
      ...PROG_PARAM_ORDER.map((name) => entry.parameters[name].encoded),
    ],
  );
  return expandPresetCatalog({
    banks,
    params: [...PROG_PARAM_ORDER],
    presets,
  });
}

describe("applyPreset", () => {
  it("hydrates Large Hall encoded parameters", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const entry = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const fullEntry = presetsFull.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const state = applyPreset(entry, map);
    expect(state.programName).toBe("Large Hall");
    expect(state.ui).toEqual({ mode: "idle" });
    expect(state.encoded.bank_index).toBe(0);
    const rtField = map.get("reverb time")!;
    expect(state.encoded[rtField]).toBe(
      fullEntry.parameters["reverb time"].encoded,
    );
  });

  it("preserves locked fields from previous state", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const largeHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const previous = applyPreset(largeHall, map);
    previous.encoded[map.get("reverb time")!] = 99;

    const next = applyPresetPreservingLocks(
      smallHall,
      map,
      previous,
      new Set([map.get("reverb time")!]),
    );
    expect(next.programName).toBe("Small Hall");
    expect(next.encoded[map.get("reverb time")!]).toBe(99);
    expect(next.encoded[map.get("size")!]).toBe(
      smallHall.parameters["size"],
    );
  });

  it("returns preset unchanged when no locks are set", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const largeHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const previous = applyPreset(largeHall, map);
    previous.encoded[map.get("reverb time")!] = 99;

    const next = applyPresetPreservingLocks(smallHall, map, previous, new Set());
    expect(next.encoded[map.get("reverb time")!]).toBe(
      smallHall.parameters["reverb time"],
    );
  });

  it("preserves multiple locked fields", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const largeHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const rt = map.get("reverb time")!;
    const size = map.get("size")!;
    const previous = applyPreset(largeHall, map);
    previous.encoded[rt] = 88;
    previous.encoded[size] = 77;

    const next = applyPresetPreservingLocks(
      smallHall,
      map,
      previous,
      new Set([rt, size]),
    );
    expect(next.encoded[rt]).toBe(88);
    expect(next.encoded[size]).toBe(77);
    expect(next.programName).toBe("Small Hall");
  });

  it("mergeLockedProgFields does not mutate next when copying locks", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const largeHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const previous = applyPreset(largeHall, map);
    const rt = map.get("reverb time")!;
    previous.encoded[rt] = 66;
    const next = applyPreset(smallHall, map);
    const beforeRt = next.encoded[rt];

    const merged = mergeLockedProgFields(next, previous, new Set([rt]));
    expect(merged.encoded[rt]).toBe(66);
    expect(next.encoded[rt]).toBe(beforeRt);
    expect(merged).not.toBe(next);
  });

  it("ignores locks when previous state is null", () => {
    const presetsFull: FullPresetDump = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/presets/presets.json"),
        "utf8",
      ),
    );
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const catalog = compactFromFull(presetsFull);
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const map = buildParameterToFieldId(spec);
    const next = applyPresetPreservingLocks(
      smallHall,
      map,
      null,
      new Set([map.get("reverb time")!]),
    );
    expect(next.programName).toBe("Small Hall");
    expect(next.encoded[map.get("reverb time")!]).toBe(
      smallHall.parameters["reverb time"],
    );
  });
});
