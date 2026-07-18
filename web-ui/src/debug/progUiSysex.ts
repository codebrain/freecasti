import { diffByteOffsets } from "@/debug/change";
import type { ProgUiRuntime } from "@/prog/uiState";
import {
  buildProgramDump,
  type ProgSerializeState,
} from "@/sysex/serialize";
import type { SpecField } from "@/spec/types";

/** Offsets patched by ``applyProgUiBytes`` (menu navigation / edit cursor). */
export const PROG_MENU_UI_OFFSETS = [92, 98, 99, 146, 147] as const;

export function diffProgSerializeStates(
  before: ProgSerializeState,
  after: ProgSerializeState,
  fields: SpecField[],
  template: Uint8Array,
  progUi: ProgUiRuntime | null,
): number[] {
  const prev = buildProgramDump(before, fields, template, progUi);
  const next = buildProgramDump(after, fields, template, progUi);
  return diffByteOffsets(prev, next);
}

export function progMenuUiOffsetsInDiff(
  diff: readonly number[],
): number[] {
  const menu = new Set<number>(PROG_MENU_UI_OFFSETS);
  return diff.filter((offset) => menu.has(offset));
}
