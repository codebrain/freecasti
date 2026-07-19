import type { ProgSerializeState } from "@/sysex/serialize";
import { withProgUiIdle } from "@/prog/uiState";
import type { PresetEntry } from "./types";

export function applyPreset(
  entry: PresetEntry,
  parameterToFieldId: Map<string, string>,
): ProgSerializeState {
  const encoded: Record<string, number> = {
    bank_index: entry.bank_index,
    program_slot: entry.program_slot,
    bank_index_mirror: entry.bank_index & 0x0f,
  };

  for (const [param, enc] of Object.entries(entry.parameters)) {
    const fieldId = parameterToFieldId.get(param);
    if (fieldId) {
      encoded[fieldId] = enc;
    }
  }

  return withProgUiIdle({
    programName: entry.name_field,
    encoded,
  });
}

/** Copy locked encoded fields from `previous` onto `next`. */
export function mergeLockedProgFields(
  next: ProgSerializeState,
  previous: ProgSerializeState | null,
  lockedFieldIds: ReadonlySet<string>,
): ProgSerializeState {
  if (!previous || lockedFieldIds.size === 0) return next;

  const encoded = { ...next.encoded };
  for (const fieldId of lockedFieldIds) {
    const value = previous.encoded[fieldId];
    if (value !== undefined) {
      encoded[fieldId] = value;
    }
  }
  return withProgUiIdle({ ...next, encoded });
}

/** Apply a factory preset but keep locked parameter values from `previous`. */
export function applyPresetPreservingLocks(
  entry: PresetEntry,
  parameterToFieldId: Map<string, string>,
  previous: ProgSerializeState | null,
  lockedFieldIds: ReadonlySet<string>,
): ProgSerializeState {
  return mergeLockedProgFields(
    applyPreset(entry, parameterToFieldId),
    previous,
    lockedFieldIds,
  );
}
