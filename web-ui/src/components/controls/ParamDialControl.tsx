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
    max,
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
    tempoBpm,
    tempoMode,
    onToggleTempoMode,
    disabled,
    locked,
  });

  return (
    <div ref={dialRef} className={`flex flex-col items-center gap-2 ${disabled ? "cursor-not-allowed" : ""}`}>
      <ParamLabel
        label={displayLabel}
        locked={locked}
        onToggleLock={onToggleLock}
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
          step={1}
          size={size}
          featured={featured}
          disabled={disabled}
          locked={locked}
          selected={selected}
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
