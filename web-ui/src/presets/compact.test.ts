import { describe, expect, it } from "vitest";
import { expandPresetCatalog } from "@/presets/compact";

describe("expandPresetCatalog", () => {
  it("expands tuple rows into PresetEntry objects", () => {
    const catalog = expandPresetCatalog({
      banks: ["Halls"],
      params: ["reverb time", "size"],
      presets: [[0, 0, "Large Hall", 40, 28]],
    });
    expect(catalog.dump_count).toBe(1);
    expect(catalog.presets[0]).toEqual({
      bank: "Halls",
      preset: "Large Hall",
      name_field: "Large Hall",
      bank_index: 0,
      program_slot: 0,
      parameters: { "reverb time": 40, size: 28 },
    });
  });
});
