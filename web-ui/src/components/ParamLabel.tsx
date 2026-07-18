import { ControlTooltip } from "@/components/ControlTooltip";
import { PadlockIcon } from "@/components/PadlockIcon";

interface ParamLabelProps {
  label: string;
  /** Parameter description shown when hovering the title. */
  description?: string;
  /** Hide description tooltip while true (e.g. dial drag). */
  tooltipSuppressed?: boolean;
  locked?: boolean;
  onToggleLock?: () => void;
  tempoMode?: boolean;
  onToggleTempoMode?: () => void;
  disabled?: boolean;
  className?: string;
}

function lockTooltip(locked: boolean, label: string): string {
  return locked
    ? `Unlock ${label} — allow preset changes to this parameter`
    : `Lock ${label} — keep this value when loading a preset`;
}

function tempoTooltip(tempoMode: boolean, label: string): string {
  return tempoMode
    ? `Tempo mode off — edit ${label} as device time`
    : `Tempo mode — edit ${label} as note divisions (1, 1/4, 1/8T, 1/8D…)`;
}

function MetronomeIcon({ active }: { active: boolean }) {
  return (
    <svg viewBox="0 0 16 16" className="h-3 w-3" aria-hidden fill="currentColor">
      <path d="M8 1.5 2 14h12L8 1.5z" fill="none" stroke="currentColor" strokeWidth="1.2" />
      <path d="M8 5v4.5" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <circle cx="8" cy="10.5" r="1.1" fill="currentColor" />
      {active && (
        <path
          d="M11 3.5 13 2"
          stroke="currentColor"
          strokeWidth="1.2"
          strokeLinecap="round"
        />
      )}
    </svg>
  );
}

export function ParamLabel({
  label,
  description,
  tooltipSuppressed = false,
  locked = false,
  onToggleLock,
  tempoMode = false,
  onToggleTempoMode,
  disabled = false,
  className = "",
}: ParamLabelProps) {
  const showIcons = onToggleTempoMode || onToggleLock;
  const isHero = className.includes("knob-hero-label");
  const typographyClass = isHero ? "knob-hero-label label-caps" : "label-caps";
  const disabledClass = disabled ? "param-label-inactive" : "";
  const iconClass = (active: boolean) =>
    `inline-flex rounded p-0.5 transition-colors ${
      disabled
        ? "cursor-not-allowed text-[color:var(--color-label)]"
        : "cursor-pointer"
    } ${
      disabled
        ? ""
        : active
          ? "text-[color:var(--color-led)] shadow-[0_0_8px_oklch(0.62_0.24_27/0.45)]"
          : "text-[color:var(--color-label)] opacity-50 hover:opacity-100"
    }`;

  return (
    <div
      className={`flex flex-col items-center gap-1 ${typographyClass} ${disabledClass} ${
        disabled ? "cursor-not-allowed" : ""
      }`.trim()}
    >
      <ControlTooltip description={description} suppressed={tooltipSuppressed}>
        <span>{label}</span>
      </ControlTooltip>
      {showIcons && (
        <div className="flex items-center justify-center gap-1.5">
          {onToggleTempoMode && (
            <ControlTooltip
              description={
                disabled
                  ? `${label} is not available for this program type`
                  : tempoTooltip(tempoMode, label)
              }
            >
              <button
                type="button"
                disabled={disabled}
                onClick={(e) => {
                  e.stopPropagation();
                  if (!disabled) onToggleTempoMode();
                }}
                className={iconClass(tempoMode)}
                aria-label={tempoMode ? `Tempo mode off for ${label}` : `Tempo mode for ${label}`}
                aria-pressed={tempoMode}
              >
                <MetronomeIcon active={tempoMode && !disabled} />
              </button>
            </ControlTooltip>
          )}
          {onToggleLock && (
            <ControlTooltip
              description={
                disabled
                  ? `${label} is not available for this program type`
                  : lockTooltip(locked, label)
              }
            >
              <button
                type="button"
                disabled={disabled}
                onClick={(e) => {
                  e.stopPropagation();
                  if (!disabled) onToggleLock();
                }}
                className={iconClass(locked)}
                aria-label={locked ? `Unlock ${label}` : `Lock ${label}`}
                aria-pressed={locked}
              >
                <PadlockIcon locked={locked && !disabled} />
              </button>
            </ControlTooltip>
          )}
        </div>
      )}
    </div>
  );
}
