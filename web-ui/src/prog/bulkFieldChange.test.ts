import { describe, expect, it } from "vitest";

import { parseMidiReceive } from "@/app/midiReceive";
import { commitProgBulkChange } from "@/prog/applyFieldChange";
import { computeSysexOutput } from "@/sysex/computeSysexOutput";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import {
  applyPreset,
  applyPresetPreservingLocks,
  mergeLockedProgFields,
} from "@/presets/applyPreset";
import {
  patchActiveSlotWithFactoryPreset,
  patchActiveSlotWithProgState,
} from "@/presets/loadPresetIntoSlot";
import { createInitialAbStore } from "@/presets/progAbSlot";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { hydrateSystemFromBytes } from "@/sysex/hydrate";
import { readSyxFromBuffer } from "@/sysex/syxIo";
import { commitProgIndividualFieldChange } from "@/prog/applyFieldChange";
import { loadMenuSyx } from "@/test/menuSyx";

function sysexProgBytes(
  state: Parameters<typeof computeSysexOutput>[0],
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

describe("commitProgBulkChange", () => {
  const runtime = loadRuntimeFixture();
  const skeletons = loadSerializeSkeletons();
  const progUi = runtime.progUi!;
  const { catalog, paramMap, spec, banks } = loadPresetCatalogFixture();
  const largeHall = catalog.presets.find(
    (p) => p.bank === "Halls" && p.preset === "Large Hall",
  )!;
  const smallHall = catalog.presets.find(
    (p) => p.bank === "Halls" && p.preset === "Small Hall",
  )!;

  it("forces idle UI on state", () => {
    const edit = commitProgIndividualFieldChange(
      applyPreset(largeHall, paramMap),
      paramMap.get("size")!,
      5,
      allProgControls(spec).find((c) => c.parameter === "size")!,
    );
    expect(edit.kind).toBe("change");
    if (edit.kind !== "change") return;
    expect(commitProgBulkChange(edit.state).ui).toEqual({ mode: "idle" });
  });

  it("emits no-menu bytes in SysEx after preset load", () => {
    const state = applyPreset(smallHall, paramMap);
    const bytes = sysexProgBytes(state, runtime, skeletons);
    expect(bytes[92]).toBe(progUi.idle["92"]);
    expect(bytes[98]).toBe(progUi.idle["98"]);
    expect(bytes[99]).toBe(progUi.idle["99"]);
    expect(bytes[146]).toBe(progUi.idle["146"]);
    expect(bytes[147]).toBe(progUi.idle["147"]);
  });

  it("clears edit UI when switching factory presets", () => {
    const size = allProgControls(spec).find((c) => c.parameter === "size")!;
    const edited = commitProgIndividualFieldChange(
      applyPreset(largeHall, paramMap),
      size.fieldId,
      size.entries[1]!.encoded,
      size,
    );
    expect(edited.kind).toBe("change");
    if (edited.kind !== "change") return;

    let store = createInitialAbStore(banks, catalog, paramMap);
    store = {
      ...store,
      [store.active]: {
        ...store[store.active],
        state: edited.state,
      },
    };
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    const next = patchActiveSlotWithFactoryPreset(
      store,
      smallHall,
      paramMap,
      new Set(),
      bankIdx,
      smallHall.program_slot,
    );
    const loaded = next[next.active].state;
    expect(loaded.ui).toEqual({ mode: "idle" });
    const bytes = sysexProgBytes(loaded, runtime, skeletons);
    expect(bytes[147]).toBe(progUi.idle["147"]);
  });

  it("mergeLockedProgFields clears UI even when next carried browse state", () => {
    const browse = {
      ...applyPreset(largeHall, paramMap),
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const merged = mergeLockedProgFields(
      applyPreset(smallHall, paramMap),
      browse,
      new Set(),
    );
    expect(merged.ui).toEqual({ mode: "idle" });
  });

  it("hydrate from menu capture still yields idle UI for outgoing SysEx", () => {
    const menuBytes = readSyxFromBuffer(loadMenuSyx("size"));
    const parsed = parseMidiReceive(
      menuBytes,
      runtime.prog,
      allProgControls(runtime.prog),
      buildSystemControls(runtime.system),
      banks,
    );
    expect(parsed?.family).toBe("prog");
    if (parsed?.family !== "prog") return;
    expect(parsed.state.ui).toEqual({ mode: "idle" });
    const bytes = sysexProgBytes(parsed.state, runtime, skeletons);
    expect(bytes[92]).toBe(progUi.idle["92"]);
    expect(bytes[99]).toBe(progUi.idle["99"]);
  });

  it("patchActiveSlotWithProgState yields idle UI after import-style hydrate", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    const parsed = parseMidiReceive(
      readSyxFromBuffer(loadMenuSyx("diffusion")),
      runtime.prog,
      allProgControls(runtime.prog),
      buildSystemControls(runtime.system),
      banks,
    );
    expect(parsed?.family).toBe("prog");
    if (parsed?.family !== "prog") return;
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    const next = patchActiveSlotWithProgState(
      store,
      parsed.state,
      new Set(),
      { bankIdx, presetSlot: largeHall.program_slot },
    );
    expect(next[next.active].state.ui).toEqual({ mode: "idle" });
  });

  it("applyPresetPreservingLocks keeps idle UI with locked fields", () => {
    const rtField = paramMap.get("reverb time")!;
    const previous = applyPreset(largeHall, paramMap);
    const next = applyPresetPreservingLocks(
      smallHall,
      paramMap,
      { ...previous, ui: { mode: "edit", parameter: "reverb time" } },
      new Set([rtField]),
    );
    expect(next.ui).toEqual({ mode: "idle" });
    expect(next.encoded[rtField]).toBe(previous.encoded[rtField]);
  });
});
