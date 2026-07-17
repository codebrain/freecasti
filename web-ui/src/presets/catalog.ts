import type { PresetCatalog, BankInfo, PresetEntry } from "./types";

export function groupPresetsByBank(catalog: PresetCatalog): BankInfo[] {
  const byBank = new Map<string, PresetEntry[]>();
  for (const preset of catalog.presets) {
    const list = byBank.get(preset.bank) ?? [];
    list.push(preset);
    byBank.set(preset.bank, list);
  }

  const banks: BankInfo[] = [];
  for (const [, presets] of byBank) {
    presets.sort((a, b) => a.program_slot - b.program_slot);
    banks.push({
      name: presets[0].bank,
      bankIndex: presets[0].bank_index,
      presets,
    });
  }
  banks.sort((a, b) => a.bankIndex - b.bankIndex);
  return banks;
}

export function findPreset(
  catalog: PresetCatalog,
  bank: string,
  programSlot: number,
): PresetEntry | undefined {
  return catalog.presets.find(
    (p) => p.bank === bank && p.program_slot === programSlot,
  );
}

/**
 * Bank index for algorithm gating (NonLin inactive params).
 * Prefer the preset selector's bank row — encoded `bank_index` can lag after UI bank changes.
 */
export function resolveProgramBankIndex(
  banks: ReadonlyArray<BankInfo>,
  bankListIndex: number,
  encoded: Record<string, number> | undefined,
): number {
  const selected = banks[bankListIndex];
  if (selected) return selected.bankIndex;
  return encoded?.bank_index ?? 0;
}

/** Map program dump identity fields to PresetSelector list indices. */
export function presetSelectorStateFromProg(
  banks: BankInfo[],
  encoded: Record<string, number>,
): { bankIdx: number; presetSlot: number } {
  const loadedBank = encoded.bank_index ?? 0;
  const loadedSlot = encoded.program_slot ?? 0;
  const bankIdx = banks.findIndex((b) => b.bankIndex === loadedBank);
  return {
    bankIdx: bankIdx >= 0 ? bankIdx : 0,
    presetSlot: loadedSlot,
  };
}
