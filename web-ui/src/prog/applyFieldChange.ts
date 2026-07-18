import type { ControlDef } from "@/spec/controls";
import { buildParamChange, type ParamChange } from "@/debug/change";
import type { ProgSerializeState } from "@/sysex/serialize";
import { snapControlToTempo } from "@/tempo/tempo";
import type { ProgUiState } from "@/prog/uiState";
import { withProgUiIdle } from "@/prog/uiState";

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

/** Ensure browse UI before a single-parameter edit (dial onSelect, keyboard, typed value, …). */
export function prepareProgUiForIndividualEdit(
  state: ProgSerializeState,
  control: ControlDef | undefined,
): ProgSerializeState {
  const parameter = control?.parameter;
  if (!parameter) return state;

  const ui = state.ui;
  if (
    (ui?.mode === "browse" || ui?.mode === "edit") &&
    ui.parameter === parameter
  ) {
    return state;
  }

  return { ...state, ui: { mode: "browse", parameter } };
}

export function isProgBrowseUiForParameter(
  ui: ProgUiState | undefined,
  parameter: string,
): boolean {
  return ui?.mode === "browse" && ui.parameter === parameter;
}

/**
 * Single entry point for one program parameter value change (dial, keyboard, buttons,
 * typed commit, tempo snap, …). Patches encoded value and edit UI for outgoing SysEx.
 */
export function commitProgIndividualFieldChange(
  state: ProgSerializeState,
  fieldId: string,
  encoded: number,
  control: ControlDef | undefined,
  options: ProgFieldChangeOptions = {},
): ProgFieldChangeResult {
  const prepared = prepareProgUiForIndividualEdit(state, control);
  return applyProgFieldChange(prepared, fieldId, encoded, control, options);
}

/**
 * Bulk program changes (preset load, import, MIDI receive, …) always emit
 * idle / no-menu UI bytes in outgoing SysEx.
 */
export function commitProgBulkChange(
  state: ProgSerializeState,
): ProgSerializeState {
  return withProgUiIdle(state);
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
  if (
    !control ||
    !control.parameter ||
    !isParameterActive(control.parameter)
  ) {
    return { kind: "noop" };
  }

  const parameter = control.parameter;

  const beforeEncoded = state.encoded[fieldId];
  const nextEncoded =
    tempoModeFields.has(fieldId) && tempoBpm > 0
      ? snapControlToTempo(control, encoded, tempoBpm)
      : encoded;

  const editUi = { mode: "edit" as const, parameter };
  const alreadyEditing =
    state.ui?.mode === "edit" && state.ui.parameter === parameter;

  if (beforeEncoded === nextEncoded) {
    if (alreadyEditing) {
      return { kind: "noop" };
    }
    return {
      kind: "change",
      state: {
        ...state,
        ui: editUi,
      },
      change: buildParamChange(
        control,
        beforeEncoded ?? nextEncoded,
        nextEncoded,
      ),
    };
  }

  return {
    kind: "change",
    state: {
      ...state,
      encoded: { ...state.encoded, [fieldId]: nextEncoded },
      ui: editUi,
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
