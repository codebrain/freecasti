import type { BankInfo } from "@/presets/types";

/** Pick a program slot when the user switches banks in the preset list. */
export function resolvePresetSlotOnBankChange(
  bank: BankInfo | undefined,
  currentSlot: number,
): number | null {
  if (!bank?.presets.length) return null;
  return (
    bank.presets.find((p) => p.program_slot === currentSlot)?.program_slot ??
    bank.presets[0].program_slot
  );
}
