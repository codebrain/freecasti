/** Compute the next dial step index from a wheel event. */
export function computeDialWheelStepIndex(
  currentIdx: number,
  deltaY: number,
  stepMax: number,
  shiftKey: boolean,
): number | null {
  const dir = deltaY < 0 ? 1 : -1;
  const mag = shiftKey ? 1 : Math.max(1, stepMax / 100);
  let next = currentIdx + dir * mag;
  next = Math.round(next);
  next = Math.max(0, Math.min(stepMax, next));
  if (next === currentIdx) return null;
  return next;
}
