import { describe, expect, it } from "vitest";

import { groupPresetsByBank, findPreset, presetSelectorStateFromProg, resolveProgramBankIndex } from "./catalog";
import type { PresetCatalog } from "./types";

const catalog: PresetCatalog = {
  generated: "2026-01-01",
  dump_count: 5,
  presets: [
    {
      bank: "Halls",
      preset: "Large Hall",
      name_field: "Large Hall",
      bank_index: 0,
      program_slot: 0,
      parameters: {},
    },
    {
      bank: "Halls",
      preset: "Small Hall",
      name_field: "Small Hall",
      bank_index: 0,
      program_slot: 1,
      parameters: {},
    },
    {
      bank: "Halls 2",
      preset: "Concert A",
      name_field: "Concert A",
      bank_index: 6,
      program_slot: 0,
      parameters: {},
    },
    {
      bank: "Ambience",
      preset: "Small Ambience",
      name_field: "Small Ambience",
      bank_index: 4,
      program_slot: 0,
      parameters: {},
    },
    {
      bank: "NonLin",
      preset: "Shimmer",
      name_field: "Shimmer",
      bank_index: 10,
      program_slot: 3,
      parameters: {},
    },
  ],
};

describe("groupPresetsByBank", () => {
  it("sorts banks by name with NonLin last and presets by slot", () => {
    const banks = groupPresetsByBank(catalog);
    expect(banks.map((b) => b.name)).toEqual([
      "Ambience",
      "Halls",
      "Halls 2",
      "NonLin",
    ]);
    const halls = banks.find((b) => b.name === "Halls")!;
    expect(halls.presets.map((p) => p.program_slot)).toEqual([0, 1]);
  });

  it("suffixes only algorithms that exist in more than one version", () => {
    const banks = groupPresetsByBank(catalog);
    expect(banks.map((b) => b.displayName)).toEqual([
      "Ambience",
      "Halls v1",
      "Halls v2",
      "NonLin",
    ]);
  });
});

describe("findPreset", () => {
  it("finds a preset by bank name and slot", () => {
    expect(findPreset(catalog, "Halls", 1)?.preset).toBe("Small Hall");
    expect(findPreset(catalog, "Halls", 99)).toBeUndefined();
  });
});

describe("presetSelectorStateFromProg", () => {
  const banks = groupPresetsByBank(catalog);

  it("maps bank_index and program_slot to list indices", () => {
    expect(
      presetSelectorStateFromProg(banks, {
        bank_index: 0,
        program_slot: 1,
      }),
    ).toEqual({ bankIdx: 1, presetSlot: 1 });
  });

  it("resolves NonLin bank index to the correct list row", () => {
    expect(
      presetSelectorStateFromProg(banks, {
        bank_index: 10,
        program_slot: 3,
      }),
    ).toEqual({ bankIdx: 3, presetSlot: 3 });
  });
});

describe("resolveProgramBankIndex", () => {
  const banks = groupPresetsByBank(catalog);

  it("prefers the UI bank list index over stale encoded bank_index", () => {
    const nonLinIdx = banks.findIndex((b) => b.name === "NonLin");
    expect(nonLinIdx).toBe(3);
    expect(
      resolveProgramBankIndex(banks, nonLinIdx, { bank_index: 0, program_slot: 0 }),
    ).toBe(10);
  });

  it("falls back to encoded bank_index when banks are unavailable", () => {
    expect(resolveProgramBankIndex([], 0, { bank_index: 10 })).toBe(10);
  });
});
