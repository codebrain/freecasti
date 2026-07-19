import type { PresetCatalog, BankInfo, PresetEntry } from "./types";

const NONLIN_BANK = "NonLin";

/** Strip a trailing " 2" (v2 marker) so "Halls 2" and "Halls" share a base. */
function baseBankName(name: string): string {
  return name.replace(/\s*2$/, "").trim();
}

export function groupPresetsByBank(catalog: PresetCatalog): BankInfo[] {
  const byBank = new Map<string, PresetEntry[]>();
  for (const preset of catalog.presets) {
    const list = byBank.get(preset.bank) ?? [];
    list.push(preset);
    byBank.set(preset.bank, list);
  }

  const grouped: Array<{ name: string; base: string; bankIndex: number; presets: PresetEntry[] }> = [];
  for (const [, presets] of byBank) {
    presets.sort((a, b) => a.program_slot - b.program_slot);
    const name = presets[0].bank;
    grouped.push({
      name,
      base: baseBankName(name),
      bankIndex: presets[0].bank_index,
      presets,
    });
  }

  // Only algorithms that exist in more than one version get a v1/v2 suffix;
  // single-version algorithms (Ambience, Chambers, NonLin, …) keep their name.
  const versionCounts = new Map<string, number>();
  for (const bank of grouped) {
    versionCounts.set(bank.base, (versionCounts.get(bank.base) ?? 0) + 1);
  }

  const banks: BankInfo[] = grouped.map((bank) => {
    const multiVersion = (versionCounts.get(bank.base) ?? 0) > 1;
    const displayName = multiVersion
      ? `${bank.base} ${bank.bankIndex <= 5 ? "v1" : "v2"}`
      : bank.base;
    return { name: bank.name, displayName, bankIndex: bank.bankIndex, presets: bank.presets };
  });

  banks.sort((a, b) => {
    const aNon = a.name === NONLIN_BANK;
    const bNon = b.name === NONLIN_BANK;
    if (aNon !== bNon) return aNon ? 1 : -1;
    return a.displayName.localeCompare(b.displayName);
  });
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
