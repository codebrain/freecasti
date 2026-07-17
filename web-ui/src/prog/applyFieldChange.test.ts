import { describe, expect, it } from "vitest";
import { applyProgFieldChange, applySysFieldChange } from "@/prog/applyFieldChange";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";
import { applyPreset } from "@/presets/applyPreset";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("applyFieldChange", () => {
  const { catalog, paramMap, spec } = loadPresetCatalogFixture();
  const entry = catalog.presets[0]!;
  const state = applyPreset(entry, paramMap);
  const control = allProgControls(spec).find((c) => c.parameter === "size")!;

  it("returns noop for inactive parameters", () => {
    const result = applyProgFieldChange(state, control.fieldId, 5, control, {
      isParameterActive: () => false,
    });
    expect(result.kind).toBe("noop");
  });

  it("applies encoded changes with param change metadata", () => {
    const nextEncoded = control.entries[1]?.encoded ?? 1;
    const result = applyProgFieldChange(state, control.fieldId, nextEncoded, control);
    expect(result.kind).toBe("change");
    if (result.kind === "change") {
      expect(result.state.encoded[control.fieldId]).toBe(nextEncoded);
      expect(result.change.fieldId).toBe(control.fieldId);
      expect(result.change.beforeEncoded).not.toBe(result.change.afterEncoded);
    }
  });

  it("applies system field changes", () => {
    const runtime = loadRuntimeFixture();
    const sysControls = buildSystemControls(runtime.system);
    const wet = sysControls.find((c) => c.parameter === "wet gain")!;
    const sysState = { [wet.fieldId]: wet.entries[0].encoded };
    const next = wet.entries[1]?.encoded ?? wet.entries[0].encoded;
    const result = applySysFieldChange(sysState, wet.fieldId, next, wet);
    expect(result.kind).toBe("change");
    if (result.kind === "change") {
      expect(result.state[wet.fieldId]).toBe(next);
    }
  });
});
