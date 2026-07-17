import type { ControlDef } from "@/spec/controls";
import { buildParamChange, type ParamChange } from "@/debug/change";
import type { ProgSerializeState } from "@/sysex/serialize";
import { snapControlToTempo } from "@/tempo/tempo";

export type ProgFieldChangeResult =
  | { kind: "noop" }
  | {
      kind: "change";
      state: ProgSerializeState;
      change: ParamChange;
    };

export interface ProgFieldChangeOptions {
  isParameterActive?: (parameter: string | undefined) => boolean;
  tempoModeFields?: ReadonlySet<string>;
  tempoBpm?: number;
}

export function applyProgFieldChange(
  state: ProgSerializeState,
  fieldId: string,
  encoded: number,
  control: ControlDef | undefined,
  {
    isParameterActive = () => true,
    tempoModeFields = new Set(),
    tempoBpm = 0,
  }: ProgFieldChangeOptions = {},
): ProgFieldChangeResult {
  if (!control || !isParameterActive(control.parameter)) {
    return { kind: "noop" };
  }

  const beforeEncoded = state.encoded[fieldId];
  const nextEncoded =
    tempoModeFields.has(fieldId) && tempoBpm > 0
      ? snapControlToTempo(control, encoded, tempoBpm)
      : encoded;

  if (beforeEncoded === nextEncoded) {
    return { kind: "noop" };
  }

  return {
    kind: "change",
    state: {
      ...state,
      encoded: { ...state.encoded, [fieldId]: nextEncoded },
    },
    change: buildParamChange(control, beforeEncoded ?? nextEncoded, nextEncoded),
  };
}

export type SysFieldChangeResult =
  | { kind: "noop" }
  | {
      kind: "change";
      state: Record<string, number>;
      change: ParamChange;
    };

export function applySysFieldChange(
  state: Record<string, number>,
  fieldId: string,
  encoded: number,
  control: ControlDef | undefined,
): SysFieldChangeResult {
  if (!control) return { kind: "noop" };

  const beforeEncoded = state[fieldId] ?? encoded;
  if (beforeEncoded === encoded) return { kind: "noop" };

  return {
    kind: "change",
    state: { ...state, [fieldId]: encoded },
    change: buildParamChange(control, beforeEncoded, encoded),
  };
}
