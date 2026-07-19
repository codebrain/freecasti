import type { ProgSerializeState } from "@/sysex/serialize";
import { applyPreset } from "./applyPreset";
import { presetSelectorStateFromProg } from "./catalog";
import type { BankInfo, PresetCatalog, PresetEntry } from "./types";

export type AbSide = "a" | "b";

export interface ProgAbSlot {
  state: ProgSerializeState;
  bankIdx: number;
  presetSlot: number;
}

export interface ProgAbStore {
  a: ProgAbSlot;
  b: ProgAbSlot;
  active: AbSide;
}

/** First bank / first program in sorted bank list. */
export function firstCatalogPresetEntry(
  banks: BankInfo[],
  catalog: PresetCatalog,
): PresetEntry {
  const entry = banks[0]?.presets[0];
  if (entry) return entry;
  const fallback = catalog.presets[0];
  if (!fallback) {
    throw new Error("preset catalog is empty");
  }
  return fallback;
}

export function createAbSlotFromEntry(
  banks: BankInfo[],
  entry: PresetEntry,
  parameterToFieldId: Map<string, string>,
): ProgAbSlot {
  const { bankIdx, presetSlot } = presetSelectorStateFromProg(banks, {
    bank_index: entry.bank_index,
    program_slot: entry.program_slot,
  });
  return {
    state: applyPreset(entry, parameterToFieldId),
    bankIdx,
    presetSlot,
  };
}

export function createInitialAbStore(
  banks: BankInfo[],
  catalog: PresetCatalog,
  parameterToFieldId: Map<string, string>,
  seedState?: ProgSerializeState | null,
): ProgAbStore {
  const defaultSlot = createAbSlotFromEntry(
    banks,
    firstCatalogPresetEntry(banks, catalog),
    parameterToFieldId,
  );

  const slotA = seedState
    ? {
        state: seedState,
        ...presetSelectorStateFromProg(banks, seedState.encoded),
      }
    : defaultSlot;

  const slotB = createAbSlotFromEntry(
    banks,
    firstCatalogPresetEntry(banks, catalog),
    parameterToFieldId,
  );

  return { a: slotA, b: slotB, active: "a" };
}

export function abSlotSelectorFromState(
  banks: BankInfo[],
  state: ProgSerializeState,
): Pick<ProgAbSlot, "bankIdx" | "presetSlot"> {
  return presetSelectorStateFromProg(banks, state.encoded);
}

export function patchAbStoreActive(
  store: ProgAbStore,
  patch: Partial<ProgAbSlot> | ((slot: ProgAbSlot) => ProgAbSlot),
): ProgAbStore {
  const current = store[store.active];
  const next =
    typeof patch === "function"
      ? patch(current)
      : { ...current, ...patch };
  return { ...store, [store.active]: next };
}

export function activeAbSlot(store: ProgAbStore): ProgAbSlot {
  return store[store.active];
}

function isAbSlot(value: unknown): value is ProgAbSlot {
  if (!value || typeof value !== "object") return false;
  const slot = value as ProgAbSlot;
  return (
    typeof slot.bankIdx === "number" &&
    typeof slot.presetSlot === "number" &&
    !!slot.state &&
    typeof slot.state === "object" &&
    typeof slot.state.programName === "string" &&
    !!slot.state.encoded &&
    typeof slot.state.encoded === "object"
  );
}

/** Parse persisted A/B store from localStorage JSON. */
export function parseStoredAbStore(raw: unknown): ProgAbStore | null {
  if (!raw || typeof raw !== "object") return null;
  const store = raw as ProgAbStore;
  if (store.active !== "a" && store.active !== "b") return null;
  if (!isAbSlot(store.a) || !isAbSlot(store.b)) return null;
  return store;
}

export function selectAbSide(store: ProgAbStore, side: AbSide): ProgAbStore {
  return { ...store, active: side };
}

/** Swap the underlying data of slots A and B; the active side letter is kept. */
export function swapAbSlots(store: ProgAbStore): ProgAbStore {
  return { ...store, a: store.b, b: store.a };
}

/** Hover tooltip for an A/B compare slot button. */
export function abCompareSlotTooltip({
  side,
  active,
  programName,
  bankName,
}: {
  side: AbSide;
  active: AbSide;
  programName: string;
  bankName?: string;
}): string {
  const letter = side.toUpperCase();
  const identity = bankName ? `${programName} · ${bankName}` : programName;
  if (active === side) {
    return `Slot ${letter} (active) — ${identity}. Preset picks and parameter edits apply here; MIDI send and the debug panel use this slot.`;
  }
  return `Switch to slot ${letter} — ${identity}. Compare two presets side by side; each slot keeps its own bank, program, and tweaks. Only the active slot receives edits.`;
}
