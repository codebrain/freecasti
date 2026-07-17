import type { ProgSerializeState } from "@/sysex/serialize";
import {
  applyPresetPreservingLocks,
  mergeLockedProgFields,
} from "./applyPreset";
import type { ProgAbSlot, ProgAbStore } from "./progAbSlot";
import type { PresetEntry } from "./types";

/** Load a factory catalog preset into the active A/B slot, respecting padlocks. */
export function patchActiveSlotWithFactoryPreset(
  store: ProgAbStore,
  entry: PresetEntry,
  parameterToFieldId: Map<string, string>,
  lockedFieldIds: ReadonlySet<string>,
  bankIdx: number,
  presetSlot: number,
): ProgAbStore {
  const current = store[store.active];
  const state = applyPresetPreservingLocks(
    entry,
    parameterToFieldId,
    current.state,
    lockedFieldIds,
  );
  return {
    ...store,
    [store.active]: { state, bankIdx, presetSlot },
  };
}

/** Load hydrated program state into the active A/B slot, respecting padlocks. */
export function patchActiveSlotWithProgState(
  store: ProgAbStore,
  next: ProgSerializeState,
  lockedFieldIds: ReadonlySet<string>,
  selector: Pick<ProgAbSlot, "bankIdx" | "presetSlot">,
): ProgAbStore {
  const current = store[store.active];
  const state = mergeLockedProgFields(next, current.state, lockedFieldIds);
  return {
    ...store,
    [store.active]: { state, ...selector },
  };
}
