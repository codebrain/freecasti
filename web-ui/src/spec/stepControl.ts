import type { ControlDef } from "./controls";

/** Step a control value by discrete entry index (+1 / −1). */
export function stepControlEncoded(
  control: ControlDef,
  encoded: number,
  delta: number,
): number | null {
  const entries =
    control.widget === "buttons"
      ? (control.buttonEntries ?? control.entries)
      : control.entries;
  const idx = entries.findIndex((e) => e.encoded === encoded);
  const baseIdx = idx >= 0 ? idx : control.entryIndex(encoded);
  const nextIdx = baseIdx + delta;
  if (nextIdx < 0 || nextIdx >= entries.length) return null;
  return entries[nextIdx]?.encoded ?? null;
}

export function arrowKeyDelta(key: string): number | null {
  if (key === "ArrowUp" || key === "ArrowRight") return 1;
  if (key === "ArrowDown" || key === "ArrowLeft") return -1;
  return null;
}

export function isTypingTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  return target.isContentEditable;
}
