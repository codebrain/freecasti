import { describe, expect, it } from "vitest";
import { resolvePresetSlotOnBankChange } from "@/app/bankChange";
import type { BankInfo } from "@/presets/types";

const bank: BankInfo = {
  name: "Halls",
  displayName: "Halls v1",
  bankIndex: 0,
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
      program_slot: 2,
      parameters: {},
    },
  ],
};

describe("resolvePresetSlotOnBankChange", () => {
  it("keeps the current slot when it exists in the new bank", () => {
    expect(resolvePresetSlotOnBankChange(bank, 2)).toBe(2);
  });

  it("falls back to the first preset when the slot is missing", () => {
    expect(resolvePresetSlotOnBankChange(bank, 99)).toBe(0);
  });

  it("returns null for an empty bank", () => {
    expect(resolvePresetSlotOnBankChange(undefined, 0)).toBeNull();
  });
});
