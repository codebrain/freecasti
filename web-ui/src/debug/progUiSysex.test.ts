import { describe, expect, it } from "vitest";
import { buildByteBreakdown } from "@/debug/byteBreakdown";
import {
  diffProgSerializeStates,
  progMenuUiOffsetsInDiff,
  PROG_MENU_UI_OFFSETS,
} from "@/debug/progUiSysex";
import { computeSysexOutput } from "@/sysex/computeSysexOutput";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { commitProgIndividualFieldChange } from "@/prog/applyFieldChange";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";
import { applyPreset } from "@/presets/applyPreset";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { hydrateSystemFromBytes } from "@/sysex/hydrate";
import { buildProgramDump } from "@/sysex/serialize";
import { defaultProgUiState } from "@/prog/uiState";

describe("prog UI sysex diff", () => {
  const runtime = loadRuntimeFixture();
  const skeletons = loadSerializeSkeletons();
  const progUi = runtime.progUi!;
  const { catalog, paramMap, spec } = loadPresetCatalogFixture();
  const baseState = applyPreset(catalog.presets[0]!, paramMap);
  const fields = runtime.prog.fields;
  const template = skeletons.prog;
  const sysState = hydrateSystemFromBytes(
    skeletons.system,
    buildSystemControls(runtime.system),
  );

  it("highlights menu UI bytes when selecting a parameter (idle → browse)", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browseState = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const diff = diffProgSerializeStates(
      baseState,
      browseState,
      fields,
      template,
      progUi,
    );
    const menuDiff = progMenuUiOffsetsInDiff(diff);
    expect(menuDiff).toContain(92);
    expect(menuDiff).toContain(99);
    expect(menuDiff).toEqual(
      expect.arrayContaining([...PROG_MENU_UI_OFFSETS].filter((o) =>
        diff.includes(o),
      )),
    );
    expect(diff).not.toContain(size.offsets[0]!);
  });

  it("highlights menu and parameter bytes when editing after browse", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browseState = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const nextEncoded =
      size.entries.find((e) => e.encoded !== baseState.encoded[size.fieldId])
        ?.encoded ?? size.entries[1]!.encoded;
    const edited = commitProgIndividualFieldChange(
      browseState,
      size.fieldId,
      nextEncoded,
      size,
    );
    expect(edited.kind).toBe("change");
    if (edited.kind !== "change") return;

    const diff = diffProgSerializeStates(
      browseState,
      edited.state,
      fields,
      template,
      progUi,
    );
    expect(progMenuUiOffsetsInDiff(diff)).toContain(146);
    expect(progMenuUiOffsetsInDiff(diff)).not.toContain(92);
    expect(diff).toEqual(expect.arrayContaining(size.offsets));
    expect(diffProgSerializeStates(browseState, edited.state, fields, template, progUi)).not.toEqual([]);
  });

  it("switches browse menu to edit menu without changing encoded value", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const browseState = {
      ...baseState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const current = baseState.encoded[size.fieldId]!;
    const edited = commitProgIndividualFieldChange(
      browseState,
      size.fieldId,
      current,
      size,
    );
    expect(edited.kind).toBe("change");
    if (edited.kind !== "change") return;

    const diff = diffProgSerializeStates(
      browseState,
      edited.state,
      fields,
      template,
      progUi,
    );
    expect(progMenuUiOffsetsInDiff(diff)).toContain(146);
    expect(progMenuUiOffsetsInDiff(diff)).not.toContain(92);
    expect(diff).not.toEqual(expect.arrayContaining(size.offsets));

    const browseBytes = buildProgramDump(browseState, fields, template, progUi);
    const editBytes = buildProgramDump(edited.state, fields, template, progUi);
    expect(browseBytes[92]).toBe(2);
    expect(editBytes[92]).toBe(2);
    expect(editBytes[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
  });

  it("patches edit menu bytes when editing from idle preset state", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const nextEncoded =
      size.entries.find((e) => e.encoded !== baseState.encoded[size.fieldId])
        ?.encoded ?? size.entries[1]!.encoded;
    const edited = commitProgIndividualFieldChange(
      baseState,
      size.fieldId,
      nextEncoded,
      size,
    );
    expect(edited.kind).toBe("change");
    if (edited.kind !== "change") return;

    const out = computeSysexOutput(
      edited.state,
      sysState,
      "prog",
      runtime.prog,
      runtime.system,
      template,
      skeletons.system,
      progUi,
    );
    const idleBytes = computeSysexOutput(
      baseState,
      sysState,
      "prog",
      runtime.prog,
      runtime.system,
      template,
      skeletons.system,
      progUi,
    ).progBytes!;
    const editedBytes = out.progBytes!;
    expect(editedBytes[92]).toBe(2);
    expect(editedBytes[99]).toBe(1);
    expect(editedBytes[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
    expect(editedBytes[146]).not.toBe(idleBytes[146]);

    const diff = diffProgSerializeStates(
      baseState,
      edited.state,
      fields,
      template,
      progUi,
    );
    expect(progMenuUiOffsetsInDiff(diff).length).toBeGreaterThan(0);
    expect(diff).toEqual(expect.arrayContaining(size.offsets));
  });

  it("decodes browse selection in the byte breakdown table", () => {
    const bytes = buildProgramDump(
      {
        ...baseState,
        ui: { mode: "browse", parameter: "size" },
      },
      fields,
      template,
      progUi,
    );
    const rows = buildByteBreakdown(bytes, runtime.prog, "prog", {
      controls: allProgControls(runtime.prog),
      progUi,
    });
    expect(rows.find((r) => r.label === "panel mode flag")?.meaning).toBe(
      "menu highlighted",
    );
    const menuRow = rows.find((r) => r.label === "selected menu index");
    expect(menuRow?.meaning).toContain("size");
    expect(menuRow?.meaning).toContain("browsing");
    const cursorRow = rows.find((r) => r.label === "display");
    expect(cursorRow?.meaning).toBe("29 — browse: size (1)");
  });

  it("decodes edit mode on panel mode flag row", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const nextEncoded =
      size.entries.find((e) => e.encoded !== baseState.encoded[size.fieldId])
        ?.encoded ?? size.entries[1]!.encoded;
    const edited = commitProgIndividualFieldChange(
      baseState,
      size.fieldId,
      nextEncoded,
      size,
    );
    expect(edited.kind).toBe("change");
    if (edited.kind !== "change") return;

    const bytes = buildProgramDump(edited.state, fields, template, progUi);
    const rows = buildByteBreakdown(bytes, runtime.prog, "prog", {
      controls: allProgControls(runtime.prog),
      progUi,
    });
    const flagRow = rows.find((r) => r.label === "panel mode flag");
    expect(flagRow?.meaning).toBe("value edit");
    const menuRow = rows.find((r) => r.label === "selected menu index");
    expect(menuRow?.meaning).toContain("editing");
    expect(menuRow?.meaning).toContain("size");
    const cursorRow = rows.find((r) => r.label === "display");
    expect(cursorRow?.meaning).toBe("210 — edit: size (1)");
  });

  it("decodes idle UI in the byte breakdown table", () => {
    const bytes = buildProgramDump(
      { ...baseState, ui: defaultProgUiState() },
      fields,
      template,
      progUi,
    );
    const rows = buildByteBreakdown(bytes, runtime.prog, "prog", {
      controls: allProgControls(runtime.prog),
      progUi,
    });
    expect(rows.find((r) => r.label === "panel mode flag")?.meaning).toBe(
      "idle",
    );
    expect(
      rows.find((r) => r.label === "selected menu index")?.meaning,
    ).toContain("UI idle");
    const cursorRow = rows.find((r) => r.label === "display");
    expect(cursorRow?.meaning).toBe("28 — idle (no menu)");
  });
});
