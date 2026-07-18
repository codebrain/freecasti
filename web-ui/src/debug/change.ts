import type { ControlDef } from "@/spec/controls";
import { displayParameterLabel, formatValueLabel } from "@/spec/labels";
import type { ActiveTab } from "@/hooks/useSysexOutput";

export interface ParamChange {
  fieldId: string;
  parameter: string;
  label: string;
  beforeEncoded: number;
  afterEncoded: number;
  beforeLabel: string;
  afterLabel: string;
}

export type ChangeRecord =
  | ({ kind: "param"; family: ActiveTab } & ParamChange)
  | { kind: "action"; family: ActiveTab; message: string };

export interface ByteHighlight {
  family: ActiveTab;
  offsets: number[];
}

export function labelForEncoded(control: ControlDef, encoded: number): string {
  const entry = control.entries.find((e) => e.encoded === encoded);
  return formatValueLabel(entry?.label ?? String(encoded), control.parameter);
}

export function buildParamChange(
  control: ControlDef,
  beforeEncoded: number,
  afterEncoded: number,
): ParamChange {
  return {
    fieldId: control.fieldId,
    parameter: control.parameter ?? control.label,
    label: displayParameterLabel(control.parameter, control.label),
    beforeEncoded,
    afterEncoded,
    beforeLabel: labelForEncoded(control, beforeEncoded),
    afterLabel: labelForEncoded(control, afterEncoded),
  };
}

export function diffByteOffsets(prev: Uint8Array, next: Uint8Array): number[] {
  const len = Math.max(prev.length, next.length);
  const offsets: number[] = [];
  for (let i = 0; i < len; i++) {
    if ((prev[i] ?? 0) !== (next[i] ?? 0)) offsets.push(i);
  }
  return offsets;
}

export function rowTouchesChangedOffsets(
  row: { offsets: number[] },
  changedOffsets: Iterable<number>,
): boolean {
  const changed = new Set(changedOffsets);
  return row.offsets.some((offset) => changed.has(offset));
}
