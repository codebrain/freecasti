import { describe, expect, it } from "vitest";
import { buildParameterToFieldId } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { expandPresetCatalog } from "@/presets/compact";
import { groupPresetsByBank } from "./catalog";
import {
  activeAbSlot,
  abSlotSelectorFromState,
  abCompareSlotTooltip,
  createAbSlotFromEntry,
  createInitialAbStore,
  firstCatalogPresetEntry,
  parseStoredAbStore,
  patchAbStoreActive,
  selectAbSide,
} from "./progAbSlot";

const catalog = expandPresetCatalog({
  // Index-positioned banks: bank_index 10 (NonLin) matches the real runtime catalog.
  banks: [
    "Halls",
    "Plates",
    "Rooms",
    "Chambers",
    "Ambience",
    "Spaces",
    "Halls 2",
    "Plates 2",
    "Rooms 2",
    "Spaces 2",
    "NonLin",
  ],
  params: ["reverb time", "size"],
  presets: [
    [0, 0, "Large Hall", 40, 28],
    [0, 1, "Small Hall", 35, 20],
    [10, 0, "Nonlin A", 0, 7],
  ],
});

const spec: DumpSpec = {
  format: "test",
  version: 1,
  message_length: 157,
  fields: [
    {
      id: "bank_index",
      label: "bank",
      offsets: [88, 89],
      start: 88,
      end: 89,
      encoding: "nibble_hilo",
    },
    {
      id: "program_slot",
      label: "slot",
      offsets: [90, 91],
      start: 90,
      end: 91,
      encoding: "nibble_hilo",
    },
    {
      id: "reverb_time",
      label: "reverb time",
      parameter: "reverb time",
      offsets: [100, 101],
      start: 100,
      end: 101,
      encoding: "nibble_hilo",
      value_map: { entries: [{ encoded: 40, label: "1" }] },
    },
    {
      id: "size",
      label: "size",
      parameter: "size",
      offsets: [102, 103],
      start: 102,
      end: 103,
      encoding: "nibble_hilo",
      value_map: { entries: [{ encoded: 28, label: "med" }] },
    },
  ],
};

describe("progAbSlot", () => {
  const banks = groupPresetsByBank(catalog);
  const paramMap = buildParameterToFieldId(spec);

  it("initialises A and B with the first bank and program", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    const first = firstCatalogPresetEntry(banks, catalog);
    expect(store.a.state.programName).toBe(first.name_field);
    expect(store.b.state.programName).toBe(first.name_field);
    expect(store.a.bankIdx).toBe(0);
    expect(store.b.bankIdx).toBe(0);
    expect(store.a.presetSlot).toBe(first.program_slot);
    expect(store.active).toBe("a");
  });

  it("patches only the active slot", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    const halls2 = createAbSlotFromEntry(banks, banks[0].presets[1], paramMap);
    const next = patchAbStoreActive(
      { ...store, active: "b" },
      halls2,
    );
    expect(next.b.state.programName).toBe("Small Hall");
    expect(next.a.state.programName).toBe("Large Hall");
  });

  it("returns the active slot and switches sides without changing slot data", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    expect(activeAbSlot(store).state.programName).toBe("Large Hall");

    const onB = selectAbSide(store, "b");
    expect(onB.active).toBe("b");
    expect(activeAbSlot(onB).state.programName).toBe("Large Hall");
    expect(onB.a).toEqual(store.a);
    expect(onB.b).toEqual(store.b);
  });

  it("derives bank and preset indices from encoded state", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    const nonLin = createAbSlotFromEntry(banks, banks[1].presets[0], paramMap);
    const patched = patchAbStoreActive(store, nonLin);
    const selector = abSlotSelectorFromState(banks, patched.a.state);
    expect(selector.bankIdx).toBe(1);
    expect(selector.presetSlot).toBe(0);
  });

  it("seeds slot A from restored state while B stays on the default preset", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    const seed = {
      ...store.a.state,
      programName: "Restored",
      encoded: { ...store.a.state.encoded, bank_index: 10, program_slot: 0 },
    };
    const restored = createInitialAbStore(banks, catalog, paramMap, seed);
    expect(restored.a.state.programName).toBe("Restored");
    expect(restored.a.bankIdx).toBe(1);
    expect(restored.b.state.programName).toBe("Large Hall");
    expect(restored.active).toBe("a");
  });

  it("parses valid persisted A/B JSON", () => {
    const store = createInitialAbStore(banks, catalog, paramMap);
    expect(parseStoredAbStore(store)).toEqual(store);
  });

  it("rejects invalid persisted A/B JSON", () => {
    expect(parseStoredAbStore(null)).toBeNull();
    expect(parseStoredAbStore({ active: "c", a: {}, b: {} })).toBeNull();
    expect(
      parseStoredAbStore({
        active: "a",
        a: { bankIdx: 0, presetSlot: 0, state: { programName: "x" } },
        b: storeSlot(),
      }),
    ).toBeNull();
  });
});

function storeSlot() {
  return {
    bankIdx: 0,
    presetSlot: 0,
    state: { programName: "Large Hall", encoded: { bank_index: 0, program_slot: 0 } },
  };
}

describe("abCompareSlotTooltip", () => {
  it("describes the active slot and what edits apply to", () => {
    const text = abCompareSlotTooltip({
      side: "a",
      active: "a",
      programName: "Large Hall",
      bankName: "Halls",
    });
    expect(text).toContain("Slot A (active)");
    expect(text).toContain("Large Hall · Halls");
    expect(text).toContain("MIDI send");
  });

  it("describes switching to an inactive slot for comparison", () => {
    const text = abCompareSlotTooltip({
      side: "b",
      active: "a",
      programName: "Small Hall",
      bankName: "Halls",
    });
    expect(text).toContain("Switch to slot B");
    expect(text).toContain("Small Hall · Halls");
    expect(text).toContain("Compare two presets");
  });
});
