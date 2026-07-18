import { ControlTooltip } from "@/components/ControlTooltip";
import { ParamLabel } from "@/components/ParamLabel";
import { displayParameterLabel, formatValueLabel } from "@/spec/labels";
import { LockedValue } from "./LockedValue";
import type { ParamWidgetControlProps } from "./types";

export type ParamButtonControlProps = ParamWidgetControlProps;

/** Button-list control for discrete enum parameters (routing, output level, …). */
export function ParamButtonControl({
  control,
  encoded,
  onChange,
  disabled = false,
  label,
  locked = false,
  onToggleLock,
  hideLabel = false,
}: ParamButtonControlProps) {
  const displayLabel = label ?? displayParameterLabel(control.parameter, control.label);
  const entries = control.buttonEntries ?? control.entries;
  const currentEntry = entries.find((e) => e.encoded === encoded) ?? entries[0];
  const valueLabel = formatValueLabel(
    currentEntry?.label ?? String(encoded),
    control.parameter,
  );

  return (
    <div className={`w-full ${disabled ? "cursor-not-allowed" : ""}`}>
      {!hideLabel && (
        <ParamLabel
          label={displayLabel}
          description={control.description}
          locked={locked}
          onToggleLock={onToggleLock}
          disabled={disabled}
          className="mb-2"
        />
      )}
      <div className="flex w-full justify-center">
        <ControlTooltip description={control.description}>
          {locked ? (
            <LockedValue valueLabel={valueLabel} disabled={disabled} />
          ) : (
            <div
              className={`flex flex-wrap justify-center gap-2 rounded-lg ${
                disabled ? "cursor-not-allowed" : ""
              }`}
              role="radiogroup"
              aria-label={displayLabel}
            >
              {entries.map((entry) => {
                const active = entry.encoded === encoded;
                return (
                  <button
                    key={entry.encoded}
                    type="button"
                    role="radio"
                    aria-checked={active}
                    disabled={disabled}
                    className={`lux-btn rounded-lg border px-3 py-2 text-xs font-led tracking-wide ${
                      disabled
                        ? `cursor-not-allowed border-[oklch(0.22_0.01_252)] text-[color:var(--color-label)] opacity-40 ${
                            active ? "bg-[oklch(0.18_0.009_252)]" : "bg-[oklch(0.14_0.009_252)]"
                          }`
                        : active
                          ? "border-[color:var(--color-primary)]/55 bg-[linear-gradient(180deg,oklch(0.62_0.24_27/0.2)_0%,oklch(0.62_0.24_27/0.08)_100%)] text-[color:var(--color-led)] shadow-[0_0_12px_oklch(0.62_0.24_27/0.2)]"
                          : "border-[oklch(0.28_0.012_252)] bg-[oklch(0.13_0.009_252)] opacity-88 hover:border-[oklch(0.48_0.016_250/0.5)] hover:opacity-100"
                    }`}
                    onClick={() => !disabled && onChange(entry.encoded)}
                  >
                    {formatValueLabel(entry.label, control.parameter)}
                  </button>
                );
              })}
            </div>
          )}
        </ControlTooltip>
      </div>
    </div>
  );
}
