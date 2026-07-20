import { PadlockIcon } from "@/components/PadlockIcon";

interface LockedValueProps {
  valueLabel: string;
  disabled?: boolean;
  iconSize?: number;
  className?: string;
}

/** Padlock + read-only value when a control is preset-locked. */
export function LockedValue({
  valueLabel,
  disabled = false,
  iconSize = 32,
  className = "",
}: LockedValueProps) {
  const valueClass = `text-sm tabular-nums ${disabled ? "control-value-inactive" : "led-text"}`;
  return (
    <div
      className={`flex flex-col items-center justify-center gap-2 rounded-lg py-3 ${
        disabled ? "cursor-not-allowed" : ""
      } ${className}`.trim()}
    >
      <PadlockIcon
        locked
        className={
          disabled
            ? "text-[color:var(--color-label)]"
            : "text-[color:var(--color-led)] shadow-[0_0_12px_oklch(0.62_0.24_27/0.45)]"
        }
        style={{ width: iconSize, height: iconSize }}
      />
      <span data-testid="param-value" className={valueClass}>
        {valueLabel}
      </span>
    </div>
  );
}
