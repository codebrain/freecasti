// @vitest-environment happy-dom

import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { resolveControlKeyDown } from "@/hooks/controlKeyboardAction";
import {
  commitProgIndividualFieldChange,
  prepareProgUiForIndividualEdit,
} from "@/prog/applyFieldChange";
import { computeSysexOutput } from "@/sysex/computeSysexOutput";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";
import { applyPreset } from "@/presets/applyPreset";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { hydrateSystemFromBytes } from "@/sysex/hydrate";
import { PROG_MENU_UI_OFFSETS } from "@/debug/progUiSysex";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "../..");

function nextEncodedForControl(
  state: ReturnType<typeof applyPreset>,
  fieldId: string,
  control: { entries: { encoded: number }[] },
) {
  const current = state.encoded[fieldId]!;
  return (
    control.entries.find((e) => e.encoded !== current)?.encoded ??
    control.entries[1]!.encoded
  );
}

function sysexProgBytes(
  state: ReturnType<typeof applyPreset>,
  runtime: ReturnType<typeof loadRuntimeFixture>,
  skeletons: ReturnType<typeof loadSerializeSkeletons>,
) {
  const sysState = hydrateSystemFromBytes(
    skeletons.system,
    buildSystemControls(runtime.system),
  );
  return computeSysexOutput(
    state,
    sysState,
    "prog",
    runtime.prog,
    runtime.system,
    skeletons.prog,
    skeletons.system,
    runtime.progUi,
  ).progBytes!;
}

describe("commitProgIndividualFieldChange", () => {
  const runtime = loadRuntimeFixture();
  const skeletons = loadSerializeSkeletons();
  const progUi = runtime.progUi!;
  const { catalog, paramMap, spec } = loadPresetCatalogFixture();
  const baseState = applyPreset(catalog.presets[0]!, paramMap);

  it("is the single commit path wired from ProgramPanel and App keyboard handler", () => {
    const programPanel = readFileSync(
      join(repoRoot, "src/components/ProgramPanel.tsx"),
      "utf8",
    );
    const app = readFileSync(join(repoRoot, "src/App.tsx"), "utf8");
    expect(programPanel).toContain("commitProgIndividualFieldChange");
    expect(programPanel).not.toMatch(/\bapplyProgFieldChange\s*\(/);
    expect(app).toContain("commitProgIndividualFieldChange");
    expect(app).not.toMatch(/\bapplyProgFieldChange\s*\(/);
  });

  it("promotes idle UI to browse then edit for any individual value change", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const nextEncoded = nextEncodedForControl(baseState, size.fieldId, size);
    const result = commitProgIndividualFieldChange(
      baseState,
      size.fieldId,
      nextEncoded,
      size,
    );
    expect(result.kind).toBe("change");
    if (result.kind !== "change") return;
    expect(result.state.ui).toEqual({ mode: "edit", parameter: "size" });
    expect(result.state.encoded[size.fieldId]).toBe(nextEncoded);
  });

  it("patches menu UI bytes in outgoing SysEx for idle → edit", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const idleBytes = sysexProgBytes(baseState, runtime, skeletons);
    const nextEncoded = nextEncodedForControl(baseState, size.fieldId, size);
    const result = commitProgIndividualFieldChange(
      baseState,
      size.fieldId,
      nextEncoded,
      size,
    );
    expect(result.kind).toBe("change");
    if (result.kind !== "change") return;

    const editedBytes = sysexProgBytes(result.state, runtime, skeletons);
    const changedMenuOffsets = PROG_MENU_UI_OFFSETS.filter(
      (offset) => editedBytes[offset] !== idleBytes[offset],
    );
    expect(changedMenuOffsets.length).toBeGreaterThan(0);
    expect(editedBytes[92]).toBe(2);
    expect(editedBytes[99]).toBe(1);
    expect(editedBytes[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
  });

  it("patches menu UI bytes when stepping from browse via keyboard resolution", () => {
    const panel = { tagName: "DIV" } as unknown as EventTarget;
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browseState = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const key = resolveControlKeyDown({
      key: "ArrowUp",
      target: panel,
      selectedFieldId: size.fieldId,
      activeTab: "prog",
      progEncoded: browseState.encoded,
      progUiState: browseState.ui,
      sysEncoded: {},
      progControls: new Map([[size.fieldId, size]]),
      sysControls: new Map(),
      isProgParamActive: () => true,
    });
    expect(key.action).toBe("step");
    if (key.action !== "step") return;

    const result = commitProgIndividualFieldChange(
      browseState,
      size.fieldId,
      key.encoded,
      size,
    );
    expect(result.kind).toBe("change");
    if (result.kind !== "change") return;

    const bytes = sysexProgBytes(result.state, runtime, skeletons);
    expect(bytes[92]).toBe(2);
    expect(bytes[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
  });

  it("enters edit UI from browse without changing encoded value", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browseState = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const current = browseState.encoded[size.fieldId]!;
    const result = commitProgIndividualFieldChange(
      browseState,
      size.fieldId,
      current,
      size,
    );
    expect(result.kind).toBe("change");
    if (result.kind !== "change") return;
    expect(result.state.ui).toEqual({ mode: "edit", parameter: "size" });
    expect(result.state.encoded[size.fieldId]).toBe(current);
  });

  it("does not reset edit UI when changing another parameter", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const predelay = allProgControls(spec).find((c) => c.parameter === "predelay")!;
    const editSize = commitProgIndividualFieldChange(
      baseState,
      size.fieldId,
      nextEncodedForControl(baseState, size.fieldId, size),
      size,
    );
    expect(editSize.kind).toBe("change");
    if (editSize.kind !== "change") return;

    const editPredelay = commitProgIndividualFieldChange(
      editSize.state,
      predelay.fieldId,
      nextEncodedForControl(editSize.state, predelay.fieldId, predelay),
      predelay,
    );
    expect(editPredelay.kind).toBe("change");
    if (editPredelay.kind !== "change") return;
    expect(editPredelay.state.ui).toEqual({
      mode: "edit",
      parameter: "predelay",
    });
  });

  it("prepareProgUiForIndividualEdit is idempotent for browse and edit", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browse = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const edit = {
      ...baseState,
      ui: { mode: "edit" as const, parameter: "size" },
    };
    expect(prepareProgUiForIndividualEdit(browse, size)).toBe(browse);
    expect(prepareProgUiForIndividualEdit(edit, size)).toBe(edit);
    expect(prepareProgUiForIndividualEdit(baseState, size).ui).toEqual({
      mode: "browse",
      parameter: "size",
    });
  });
});
