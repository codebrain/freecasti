import { useEffect, useState } from "react";
import { ControlTooltip } from "@/components/ControlTooltip";
import {
  toolbarButtonClass,
  toolbarBpmShellClass,
} from "@/components/toolbarButtons";
import {
  clampSendOnChangeThrottleMs,
  commitSendOnChangeThrottleDraft,
  sanitizeSendOnChangeThrottleDraft,
  SEND_ON_CHANGE_THROTTLE_MS_MAX,
  SEND_ON_CHANGE_THROTTLE_MS_MIN,
} from "@/midi/sendOnChangeThrottle";

export interface SendOnChangeControlProps {
  active: boolean;
  disabled?: boolean;
  throttleMs: number;
  onToggle: () => void;
  onThrottleMsChange: (ms: number) => void;
}

export function SendOnChangeControl({
  active,
  disabled = false,
  throttleMs,
  onToggle,
  onThrottleMsChange,
}: SendOnChangeControlProps) {
  const [focused, setFocused] = useState(false);
  const [draft, setDraft] = useState(String(throttleMs));

  useEffect(() => {
    if (!focused) {
      setDraft(String(throttleMs));
    }
  }, [throttleMs, focused]);

  const commit = () => {
    const next = commitSendOnChangeThrottleDraft(draft, throttleMs);
    setDraft(String(next));
    if (next !== throttleMs) {
      onThrottleMsChange(next);
    }
  };

  const tooltip = `Automatically send SysEx when you edit — throttled to at most once every ${throttleMs} ms. Device echoes are validated against the last TX and shown in the debug panel.`;

  return (
    <ControlTooltip description={tooltip}>
      <div
        className={`${toolbarBpmShellClass} gap-1.5 py-1 pr-2 pl-1.5 ${
          disabled ? "opacity-35" : ""
        }`}
      >
        <button
          type="button"
          className={`${toolbarButtonClass(active, disabled)} min-h-[1.75rem] px-2.5 py-1`}
          disabled={disabled}
          onClick={onToggle}
          aria-pressed={active}
        >
          On change
        </button>
        <label className="flex items-center gap-1 text-xs">
          <input
            type="text"
            inputMode="numeric"
            autoComplete="off"
            autoCorrect="off"
            spellCheck={false}
            name="m7-send-on-change-throttle-ms"
            aria-label="Send on change throttle milliseconds"
            disabled={disabled}
            value={focused ? draft : String(throttleMs)}
            onFocus={(e) => {
              setDraft(String(throttleMs));
              setFocused(true);
              e.currentTarget.select();
            }}
            onChange={(e) => {
              setDraft(sanitizeSendOnChangeThrottleDraft(e.target.value));
            }}
            onBlur={() => {
              setFocused(false);
              commit();
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                (e.currentTarget as HTMLInputElement).blur();
              } else if (e.key === "ArrowUp") {
                e.preventDefault();
                const base = commitSendOnChangeThrottleDraft(draft, throttleMs);
                const next = clampSendOnChangeThrottleMs(base + 50);
                setDraft(String(next));
                onThrottleMsChange(next);
              } else if (e.key === "ArrowDown") {
                e.preventDefault();
                const base = commitSendOnChangeThrottleDraft(draft, throttleMs);
                const next = clampSendOnChangeThrottleMs(base - 50);
                setDraft(String(next));
                onThrottleMsChange(next);
              }
            }}
            onClick={(e) => e.stopPropagation()}
            className="w-[3rem] rounded border border-[oklch(0.22_0.01_252)] bg-[oklch(0.08_0.007_252)] px-1 py-0.5 text-center font-led text-xs tabular-nums shadow-[inset_0_1px_3px_oklch(0_0_0/0.4)] focus:border-[color:var(--color-primary)]/45 focus:bg-[oklch(0.1_0.008_252)] focus:outline-none focus:ring-1 focus:ring-[color:var(--color-primary)]/25 disabled:cursor-not-allowed"
            title={`${SEND_ON_CHANGE_THROTTLE_MS_MIN}–${SEND_ON_CHANGE_THROTTLE_MS_MAX} ms`}
          />
          <span className="label-caps text-[0.6rem] opacity-70">ms</span>
        </label>
      </div>
    </ControlTooltip>
  );
}
