import { ControlTooltip } from "@/components/ControlTooltip";
import { Knob } from "@/components/Knob";
import { ParamLabel } from "@/components/ParamLabel";
import type { ParamWidgetControlProps } from "./types";
import { useParamDial } from "./useParamDial";

export type ParamDialControlProps = ParamWidgetControlProps;

/** Rotary dial for a spec-backed parameter (predelay, wet gain, reverb time, …). */
export function ParamDialControl({
  control,
  encoded,
  onChange,
  defaultEncoded,
  size = 58,
  label,
  featured = false,
  disabled = false,
  selected = false,
  onSelect,
  locked = false,
  onToggleLock,
  tempoBpm = 120,
  tempoMode = false,
  onToggleTempoMode,
}: ParamDialControlProps) {
  const {
    displayLabel,
    tempoActive,
    idx,
    stepIdx,
    stepMax,
    defaultStepIdx,
    max,
    valueMarkers,
    dialRef,
    dialDragging,
    setDialDragging,
    handleKnobIndex,
    commitTypedValue,
    formattedValue,
    onToggleTempoMode: showTempoToggle,
  } = useParamDial({
    control,
    encoded,
    onChange,
    onSelect,
    label,
    defaultEncoded,
    tempoBpm,
    tempoMode,
    onToggleTempoMode,
    disabled,
    locked,
  });

  return (
    <div
      ref={dialRef}
      data-testid="param-control"
      data-param={control.parameter ?? control.fieldId}
      className={`flex flex-col items-center gap-0.5 ${disabled ? "cursor-not-allowed" : ""}`}
    >
      <ParamLabel
        label={displayLabel}
        description={control.description}
        tooltipSuppressed={dialDragging}
        tempoMode={tempoActive}
        onToggleTempoMode={showTempoToggle}
        disabled={disabled}
        className={featured ? "knob-hero-label label-caps" : ""}
      />
      <ControlTooltip description={control.description} suppressed={dialDragging}>
          <Knob
            value={tempoActive ? stepIdx : idx}
            min={0}
            max={Math.max(0, tempoActive ? stepMax : max)}
            defaultValue={defaultStepIdx}
            step={1}
            size={size}
            featured={featured}
            disabled={disabled}
            locked={locked}
            onToggleLock={onToggleLock}
            selected={selected}
            valueMarkers={valueMarkers}
            onDraggingChange={setDialDragging}
            displayValue={formattedValue}
            onValueCommit={commitTypedValue}
            valueAriaLabel={displayLabel}
            onChange={handleKnobIndex}
          />
        </ControlTooltip>
    </div>
  );
}
