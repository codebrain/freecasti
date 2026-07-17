import { useEffect } from "react";
import type { ControlDef } from "@/spec/controls";
import {
  resolveControlKeyDown,
  shouldClearSelectionOnPointerDown,
} from "./controlKeyboardAction";
import type { ActiveTab } from "./useSysexOutput";

interface UseControlKeyboardOptions {
  selectedFieldId: string | null;
  activeTab: ActiveTab;
  progEncoded: Record<string, number> | null;
  sysEncoded: Record<string, number> | null;
  progControls: Map<string, ControlDef>;
  sysControls: Map<string, ControlDef>;
  isProgParamActive: (parameter: string | undefined) => boolean;
  onProgStep: (fieldId: string, encoded: number) => void;
  onSysStep: (fieldId: string, encoded: number) => void;
  onClearSelection: () => void;
  tempoModeFields?: ReadonlySet<string>;
  tempoBpm?: number;
}

export function useControlKeyboard({
  selectedFieldId,
  activeTab,
  progEncoded,
  sysEncoded,
  progControls,
  sysControls,
  isProgParamActive,
  onProgStep,
  onSysStep,
  onClearSelection,
  tempoModeFields = new Set(),
  tempoBpm = 0,
}: UseControlKeyboardOptions) {
  useEffect(() => {
    if (!selectedFieldId) return;

    const onKeyDown = (e: KeyboardEvent) => {
      const result = resolveControlKeyDown({
        key: e.key,
        target: e.target,
        selectedFieldId,
        activeTab,
        progEncoded,
        sysEncoded,
        progControls,
        sysControls,
        isProgParamActive,
        tempoModeFields,
        tempoBpm,
      });

      if (result.action === "none") return;

      e.preventDefault();
      if (result.action === "clear") {
        onClearSelection();
      } else if (result.action === "step") {
        if (result.family === "prog") {
          onProgStep(result.fieldId, result.encoded);
        } else {
          onSysStep(result.fieldId, result.encoded);
        }
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [
    selectedFieldId,
    activeTab,
    progEncoded,
    sysEncoded,
    progControls,
    sysControls,
    isProgParamActive,
    onProgStep,
    onSysStep,
    onClearSelection,
    tempoModeFields,
    tempoBpm,
  ]);

  useEffect(() => {
    if (!selectedFieldId) return;

    const onPointerDown = (e: PointerEvent) => {
      if (!shouldClearSelectionOnPointerDown(e.target, true)) return;
      onClearSelection();
    };

    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [selectedFieldId, onClearSelection]);
}
