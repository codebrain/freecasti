import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { applyPreset } from "@/presets/applyPreset";
import { expandPresetCatalog } from "@/presets/compact";
import { groupPresetsByBank } from "@/presets/catalog";
import {
  createInitialAbStore,
  type ProgAbStore,
} from "@/presets/progAbSlot";
import {
  patchActiveSlotWithFactoryPreset,
  patchActiveSlotWithProgState,
} from "@/presets/loadPresetIntoSlot";
import { allProgControls, buildParameterToFieldId } from "@/spec/controls";
import { PROG_PARAM_ORDER } from "@/spec/param-order";
import type { DumpSpec } from "@/spec/types";
import { hydrateProgramFromBytes } from "@/sysex/hydrate";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { readSyxFromBuffer } from "@/sysex/syxIo";

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
  const presets = presetsFull.presets.map((entry) => [
    entry.bank_index,
    entry.program_slot,
    entry.name_field,
    ...PROG_PARAM_ORDER.map((name) => entry.parameters[name].encoded),
  ]);
  return expandPresetCatalog({
    banks,
    params: [...PROG_PARAM_ORDER],
    presets,
  });
}

function fixtureCatalog() {
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
  const banks = groupPresetsByBank(catalog);
  const map = buildParameterToFieldId(spec);
  return { catalog, banks, map, spec };
}

function storeWithLockedReverbTime(
  banks: ReturnType<typeof groupPresetsByBank>,
  catalog: ReturnType<typeof compactFromFull>,
  map: Map<string, string>,
  lockedValue: number,
): { store: ProgAbStore; rtField: string } {
  const store = createInitialAbStore(banks, catalog, map);
  const rtField = map.get("reverb time")!;
  const active = store[store.active];
  store[store.active] = {
    ...active,
    state: {
      ...active.state,
      encoded: { ...active.state.encoded, [rtField]: lockedValue },
    },
  };
  return { store, rtField };
}

describe("loadPresetIntoSlot", () => {
  it("patchActiveSlotWithFactoryPreset keeps locked fields on catalog preset change", () => {
    const { catalog, banks, map } = fixtureCatalog();
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const { store, rtField } = storeWithLockedReverbTime(
      banks,
      catalog,
      map,
      42,
    );
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    const next = patchActiveSlotWithFactoryPreset(
      store,
      smallHall,
      map,
      new Set([rtField]),
      bankIdx,
      smallHall.program_slot,
    );
    const active = next[next.active];
    expect(active.state.programName).toBe("Small Hall");
    expect(active.state.encoded[rtField]).toBe(42);
    expect(active.state.encoded[map.get("size")!]).toBe(
      smallHall.parameters["size"],
    );
    expect(active.bankIdx).toBe(bankIdx);
    expect(active.presetSlot).toBe(smallHall.program_slot);
  });

  it("patchActiveSlotWithFactoryPreset updates all fields when nothing is locked", () => {
    const { catalog, banks, map } = fixtureCatalog();
    const largeHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Large Hall",
    )!;
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const store = createInitialAbStore(banks, catalog, map);
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    store[store.active] = {
      ...store[store.active],
      state: applyPreset(largeHall, map),
      bankIdx,
      presetSlot: largeHall.program_slot,
    };
    const rtField = map.get("reverb time")!;
    const next = patchActiveSlotWithFactoryPreset(
      store,
      smallHall,
      map,
      new Set(),
      bankIdx,
      smallHall.program_slot,
    );
    expect(next[next.active].state.encoded[rtField]).toBe(
      smallHall.parameters["reverb time"],
    );
  });

  it("patchActiveSlotWithProgState keeps locked fields when loading hydrated bytes", () => {
    const { catalog, banks, map, spec } = fixtureCatalog();
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const { store, rtField } = storeWithLockedReverbTime(
      banks,
      catalog,
      map,
      55,
    );
    const skeletons = loadSerializeSkeletons();
    const progBytes = readSyxFromBuffer(skeletons.prog);
    const hydrated = hydrateProgramFromBytes(
      progBytes,
      spec,
      allProgControls(spec),
    );
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    const next = patchActiveSlotWithProgState(
      store,
      hydrated,
      new Set([rtField]),
      { bankIdx, presetSlot: smallHall.program_slot },
    );
    const active = next[next.active];
    expect(active.state.encoded[rtField]).toBe(55);
    expect(active.state.programName).toBe(hydrated.programName);
    expect(active.bankIdx).toBe(bankIdx);
    expect(active.presetSlot).toBe(smallHall.program_slot);
  });

  it("does not mutate the incoming store", () => {
    const { catalog, banks, map } = fixtureCatalog();
    const smallHall = catalog.presets.find(
      (p) => p.bank === "Halls" && p.preset === "Small Hall",
    )!;
    const { store, rtField } = storeWithLockedReverbTime(
      banks,
      catalog,
      map,
      11,
    );
    const beforeName = store[store.active].state.programName;
    const bankIdx = banks.findIndex((b) => b.name === "Halls");
    patchActiveSlotWithFactoryPreset(
      store,
      smallHall,
      map,
      new Set([rtField]),
      bankIdx,
      smallHall.program_slot,
    );
    expect(store[store.active].state.programName).toBe(beforeName);
    expect(store[store.active].state.encoded[rtField]).toBe(11);
  });
});
