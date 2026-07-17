import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { ControlDef } from "@/spec/controls";
import { displayParameterLabel, formatValueLabel } from "@/spec/labels";
import {
  isTempoParameter,
  tempoStepIndexForEncoded,
  tempoStepsForControl,
  formatControlTempoValue,
} from "@/tempo/tempo";
import { computeDialWheelStepIndex } from "@/controls/dialWheel";
import { resolveTypedControlValue } from "@/controls/resolveTypedValue";

interface UseParamDialOptions {
  control: ControlDef;
  encoded: number;
  onChange: (encoded: number) => void;
  onSelect?: () => void;
  label?: string;
  tempoBpm?: number;
  tempoMode?: boolean;
  onToggleTempoMode?: () => void;
  disabled?: boolean;
  locked?: boolean;
}

export function useParamDial({
  control,
  encoded,
  onChange,
  onSelect,
  label,
  tempoBpm = 120,
  tempoMode = false,
  onToggleTempoMode,
  disabled = false,
  locked = false,
}: UseParamDialOptions) {
  const displayLabel = label ?? displayParameterLabel(control.parameter, control.label);
  const showTempo = isTempoParameter(control.parameter) && !!onToggleTempoMode;
  const tempoActive = showTempo && tempoMode && tempoBpm > 0;

  const tempoSteps = useMemo(
    () => (tempoActive ? tempoStepsForControl(control, tempoBpm) : []),
    [tempoActive, control, tempoBpm],
  );

  const idx = control.entryIndex(encoded);
  const entry = control.entries[idx] ?? control.entries[0];
  const max = control.entries.length - 1;
  const stepIdx = tempoActive
    ? tempoStepIndexForEncoded(control, encoded, tempoBpm)
    : idx;
  const stepMax = tempoActive ? Math.max(0, tempoSteps.length - 1) : max;

  const changeEncoded = useCallback(
    (nextEncoded: number) => {
      if (nextEncoded === encoded) return;
      onSelect?.();
      onChange(nextEncoded);
    },
    [encoded, onChange, onSelect],
  );

  const applyStepIndex = useCallback(
    (nextIdx: number) => {
      if (tempoActive && tempoSteps.length) {
        const step = tempoSteps[nextIdx];
        if (step) changeEncoded(step.encoded);
        return;
      }
      const e = control.entries[nextIdx];
      if (e) changeEncoded(e.encoded);
    },
    [tempoActive, tempoSteps, control.entries, changeEncoded],
  );

  const wheelStateRef = useRef({
    idx,
    stepIdx,
    stepMax,
    tempoActive,
    applyStepIndex,
  });
  wheelStateRef.current = { idx, stepIdx, stepMax, tempoActive, applyStepIndex };

  const dialRef = useRef<HTMLDivElement>(null);
  const [dialDragging, setDialDragging] = useState(false);

  useEffect(() => {
    const el = dialRef.current;
    if (!el || disabled || locked) return;

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      e.stopPropagation();

      const { idx, stepIdx, stepMax, tempoActive, applyStepIndex } =
        wheelStateRef.current;
      const currentIdx = tempoActive ? stepIdx : idx;
      const next = computeDialWheelStepIndex(
        currentIdx,
        e.deltaY,
        stepMax,
        e.shiftKey,
      );
      if (next === null) return;
      applyStepIndex(next);
    };

    el.addEventListener("wheel", onWheel, { passive: false });
    return () => el.removeEventListener("wheel", onWheel);
  }, [disabled, locked]);

  const handleKnobIndex = useCallback(
    (nextIdx: number) => {
      if (tempoActive && tempoSteps.length) {
        const step = tempoSteps[nextIdx];
        if (!step) return;
        changeEncoded(step.encoded);
        return;
      }
      const e = control.entries[nextIdx];
      if (e) changeEncoded(e.encoded);
    },
    [tempoActive, tempoSteps, control.entries, changeEncoded],
  );

  const commitTypedValue = useCallback(
    (draft: string) => {
      const next = resolveTypedControlValue(control, draft, {
        tempoBpm,
        tempoActive,
      });
      if (next !== null) changeEncoded(next);
    },
    [control, tempoBpm, tempoActive, changeEncoded],
  );

  const formattedValue = tempoActive
    ? formatControlTempoValue(control, encoded, tempoBpm) ??
      formatValueLabel(entry?.label ?? String(encoded), control.parameter)
    : formatValueLabel(entry?.label ?? String(encoded), control.parameter);

  return {
    displayLabel,
    showTempo,
    tempoActive,
    tempoSteps,
    entry,
    idx,
    stepIdx,
    stepMax,
    max,
    dialRef,
    dialDragging,
    setDialDragging,
    handleKnobIndex,
    commitTypedValue,
    formattedValue,
    onToggleTempoMode: showTempo ? onToggleTempoMode : undefined,
  };
}
