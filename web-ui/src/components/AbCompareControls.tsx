import { ControlTooltip } from "@/components/ControlTooltip";
import type { AbSide } from "@/presets/progAbSlot";

interface AbCompareControlsProps {
  active: AbSide;
  tooltips: Record<AbSide, string>;
  onSelect: (side: AbSide) => void;
  onSwap: () => void;
}

function SwapIcon() {
  return (
    <svg
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5"
      aria-hidden
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M2 5.5H12M9.5 3 12 5.5 9.5 8" />
      <path d="M14 10.5H4M6.5 8 4 10.5 6.5 13" />
    </svg>
  );
}

function sideButtonClass(selected: boolean): string {
  return `lux-btn min-w-[2.35rem] rounded-md border px-2.5 py-1 font-led text-xs tracking-[0.2em] ${
    selected
      ? "border-[color:var(--color-primary)]/55 bg-[linear-gradient(180deg,oklch(0.62_0.24_27/0.18)_0%,oklch(0.62_0.24_27/0.08)_100%)] text-[color:var(--color-led)] shadow-[0_0_14px_oklch(0.62_0.24_27/0.22)]"
      : "border-[oklch(0.28_0.012_252)] bg-[oklch(0.12_0.009_252)] opacity-82 hover:border-[oklch(0.48_0.016_250/0.5)] hover:opacity-100"
  }`;
}

export function AbCompareControls({
  active,
  tooltips,
  onSelect,
  onSwap,
}: AbCompareControlsProps) {
  return (
    <div
      className="flex shrink-0 items-center gap-1"
      role="group"
      aria-label="Compare presets A and B"
    >
      <ControlTooltip
        placement="bottom"
        description="Swap the contents of slots A and B"
      >
        <button
          type="button"
          className="lux-btn flex items-center justify-center rounded-md border border-[oklch(0.28_0.012_252)] bg-[oklch(0.12_0.009_252)] px-2 py-1.5 text-[color:var(--color-label)] opacity-82 hover:border-[oklch(0.48_0.016_250/0.5)] hover:opacity-100"
          aria-label="Swap slots A and B"
          onClick={onSwap}
        >
          <SwapIcon />
        </button>
      </ControlTooltip>
      {(["a", "b"] as const).map((side) => (
        <ControlTooltip
          key={side}
          placement="bottom"
          description={tooltips[side]}
        >
          <button
            type="button"
            className={sideButtonClass(active === side)}
            aria-pressed={active === side}
            aria-label={`Compare slot ${side.toUpperCase()}`}
            onClick={() => onSelect(side)}
          >
            {side.toUpperCase()}
          </button>
        </ControlTooltip>
      ))}
    </div>
  );
}
