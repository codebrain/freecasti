/** Shared rack-style toolbar button chrome (header + MIDI bar). */

const TOOLBAR_BTN_BASE =
  "lux-btn inline-flex items-center justify-center min-h-[2.125rem] px-3.5 py-1.5 font-led text-[0.65rem] tracking-[0.22em] uppercase outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-primary)]/40 focus-visible:ring-offset-1 focus-visible:ring-offset-[oklch(0.08_0.006_252)]";

const TOOLBAR_BTN_ACTIVE =
  "border border-[color:var(--color-primary)]/60 bg-[linear-gradient(180deg,oklch(0.62_0.24_27/0.22)_0%,oklch(0.62_0.24_27/0.1)_100%)] text-[color:var(--color-led)] shadow-[0_0_16px_oklch(0.62_0.24_27/0.28),inset_0_1px_0_oklch(0.78_0.08_27/0.18)]";

const TOOLBAR_BTN_IDLE =
  "border border-[oklch(0.28_0.012_252)] bg-[linear-gradient(180deg,oklch(0.16_0.01_252)_0%,oklch(0.12_0.009_252)_100%)] text-[color:var(--color-label)] opacity-92 hover:border-[oklch(0.48_0.016_250/0.55)] hover:bg-[linear-gradient(180deg,oklch(0.19_0.01_252)_0%,oklch(0.14_0.009_252)_100%)] hover:opacity-100 hover:shadow-[0_4px_14px_oklch(0_0_0/0.28)]";

export function toolbarButtonClass(active = false, disabled = false): string {
  if (disabled) {
    return `${TOOLBAR_BTN_BASE} cursor-not-allowed border-[oklch(0.2_0.01_252)] bg-[oklch(0.1_0.008_252)] text-[color:var(--color-label)] opacity-35`;
  }
  return `${TOOLBAR_BTN_BASE} ${active ? TOOLBAR_BTN_ACTIVE : TOOLBAR_BTN_IDLE}`;
}

/** Recessed track for a two-option segmented control (Program / System). */
export const toolbarSegmentTrackClass =
  "inline-flex rounded-lg border border-[oklch(0.26_0.012_252)] bg-[oklch(0.08_0.007_255)] p-0.5 shadow-[inset_0_3px_8px_oklch(0_0_0/0.65),0_1px_0_oklch(0.38_0.014_250/0.1)]";

export function toolbarSegmentButtonClass(
  selected: boolean,
  edge: "start" | "end",
): string {
  const radius =
    edge === "start"
      ? "rounded-l-[0.35rem] rounded-r-none"
      : "rounded-r-[0.35rem] rounded-l-none";
  if (selected) {
    return `${TOOLBAR_BTN_BASE} ${radius} min-w-[5.5rem] border border-[color:var(--color-primary)]/55 bg-[linear-gradient(180deg,oklch(0.64_0.245_27/0.24)_0%,oklch(0.62_0.24_27/0.12)_100%)] text-[color:var(--color-led)] shadow-[0_0_14px_oklch(0.62_0.24_27/0.32),inset_0_1px_0_oklch(0.78_0.08_27/0.16)]`;
  }
  return `${TOOLBAR_BTN_BASE} ${radius} min-w-[5.5rem] border border-transparent bg-transparent text-[color:var(--color-label)] opacity-72 hover:bg-[oklch(0.14_0.009_252/0.85)] hover:opacity-100`;
}

/** Shell around inline BPM in the header. */
export const toolbarBpmShellClass =
  "inline-flex items-center gap-2 rounded-lg border border-[oklch(0.28_0.012_252)] bg-[linear-gradient(180deg,oklch(0.14_0.009_252)_0%,oklch(0.1_0.008_252)_100%)] px-3 py-1.5 shadow-[inset_0_3px_7px_oklch(0_0_0/0.55),0_1px_0_oklch(0.38_0.014_250/0.08)]";

export const appHeaderClass =
  "relative flex flex-wrap items-center justify-between gap-4 border-b border-[oklch(0.3_0.012_252/0.75)] bg-[linear-gradient(180deg,oklch(0.15_0.01_250)_0%,oklch(0.1_0.008_255)_100%)] px-5 py-4 shadow-[inset_0_1px_0_oklch(0.72_0.02_250/0.1)]";

export const appSubheaderClass =
  "relative flex min-h-[2.875rem] flex-wrap items-center justify-between gap-2.5 border-b border-[oklch(0.24_0.01_252/0.8)] bg-[linear-gradient(180deg,oklch(0.13_0.009_252)_0%,oklch(0.11_0.009_255)_100%)] px-5 py-2.5 shadow-[inset_0_1px_0_oklch(0.38_0.014_250/0.06)]";

export const toolbarSelectClass =
  "lux-btn max-w-[11rem] rounded-lg border border-[oklch(0.28_0.012_252)] bg-[linear-gradient(180deg,oklch(0.14_0.009_252)_0%,oklch(0.1_0.008_252)_100%)] px-2.5 py-1.5 text-xs font-led tracking-wide text-[color:var(--color-label)] shadow-[inset_0_2px_5px_oklch(0_0_0/0.42)] hover:border-[oklch(0.48_0.016_250/0.55)] focus:border-[color:var(--color-primary)]/50 focus:outline-none focus:ring-1 focus:ring-[color:var(--color-primary)]/30";
