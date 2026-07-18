import type { ControlDef } from "@/spec/controls";
import {
  arrowKeyDelta,
  isTypingTarget,
  stepControlEncoded,
} from "@/spec/stepControl";
import { stepControlTempoEncoded } from "@/tempo/tempo";
import { isProgBrowseUiForParameter } from "@/prog/applyFieldChange";
import type { ProgUiState } from "@/prog/uiState";
import type { ActiveTab } from "./useSysexOutput";

export interface ControlKeyDownInput {
  key: string;
  target: EventTarget | null;
  selectedFieldId: string | null;
  activeTab: ActiveTab;
  progEncoded: Record<string, number> | null;
  progUiState?: ProgUiState | null;
  sysEncoded: Record<string, number> | null;
  progControls: Map<string, ControlDef>;
  sysControls: Map<string, ControlDef>;
  isProgParamActive: (parameter: string | undefined) => boolean;
  tempoModeFields?: ReadonlySet<string>;
  tempoBpm?: number;
}

export type ControlKeyDownResult =
  | { action: "none" }
  | { action: "clear" }
  | { action: "step"; family: ActiveTab; fieldId: string; encoded: number };

export function resolveControlKeyDown(
  input: ControlKeyDownInput,
): ControlKeyDownResult {
  const {
    key,
    target,
    selectedFieldId,
    activeTab,
    progEncoded,
    progUiState = null,
    sysEncoded,
    progControls,
    sysControls,
    isProgParamActive,
    tempoModeFields = new Set(),
    tempoBpm = 0,
  } = input;

  if (!selectedFieldId) return { action: "none" };
  if (isTypingTarget(target)) return { action: "none" };

  if (key === "Escape") return { action: "clear" };

  const delta = arrowKeyDelta(key);
  if (delta === null) return { action: "none" };

  const controlMap = activeTab === "prog" ? progControls : sysControls;
  const encodedState = activeTab === "prog" ? progEncoded : sysEncoded;
  const control = controlMap.get(selectedFieldId);
  if (!control || !encodedState) return { action: "none" };

  if (
    activeTab === "prog" &&
    control.parameter &&
    !isProgParamActive(control.parameter)
  ) {
    return { action: "none" };
  }

  const current = encodedState[selectedFieldId] ?? control.entries[0]?.encoded;
  let next: number | null = null;
  if (
    activeTab === "prog" &&
    tempoModeFields.has(selectedFieldId) &&
    tempoBpm > 0
  ) {
    next = stepControlTempoEncoded(control, current, delta, tempoBpm);
  }
  if (next === null) {
    next = stepControlEncoded(control, current, delta);
  }
  if (next === null) return { action: "none" };

  if (
    activeTab === "prog" &&
    next === current &&
    control.parameter &&
    isProgBrowseUiForParameter(progUiState ?? undefined, control.parameter)
  ) {
    return {
      action: "step",
      family: "prog",
      fieldId: selectedFieldId,
      encoded: next,
    };
  }

  if (next === current) return { action: "none" };

  return {
    action: "step",
    family: activeTab,
    fieldId: selectedFieldId,
    encoded: next,
  };
}

export function shouldClearSelectionOnPointerDown(
  target: EventTarget | null,
  hasSelection: boolean,
): boolean {
  if (!hasSelection) return false;
  if (
    !target ||
    typeof (target as Element).closest !== "function"
  ) {
    return true;
  }
  return (target as Element).closest("[data-param-control]") === null;
}
