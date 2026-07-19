export const SEND_ON_CHANGE_THROTTLE_MS_MIN = 0;
export const SEND_ON_CHANGE_THROTTLE_MS_MAX = 10_000;
export const SEND_ON_CHANGE_THROTTLE_MS_DEFAULT = 15;

export function sanitizeSendOnChangeThrottleDraft(raw: string): string {
  return raw.replace(/\D/g, "");
}

export function clampSendOnChangeThrottleMs(ms: number): number {
  return Math.max(
    SEND_ON_CHANGE_THROTTLE_MS_MIN,
    Math.min(SEND_ON_CHANGE_THROTTLE_MS_MAX, ms),
  );
}

export function commitSendOnChangeThrottleDraft(
  draft: string,
  fallback: number,
): number {
  const trimmed = draft.trim();
  if (!trimmed) {
    return clampSendOnChangeThrottleMs(fallback);
  }
  const next = Number(trimmed);
  if (!Number.isFinite(next)) {
    return clampSendOnChangeThrottleMs(fallback);
  }
  return clampSendOnChangeThrottleMs(Math.round(next));
}

export function readStoredSendOnChangeThrottleMs(): number {
  try {
    const raw = localStorage.getItem("m7.midi.sendOnChangeThrottleMs");
    if (raw == null) return SEND_ON_CHANGE_THROTTLE_MS_DEFAULT;
    const next = Number(raw);
    if (!Number.isFinite(next)) return SEND_ON_CHANGE_THROTTLE_MS_DEFAULT;
    return clampSendOnChangeThrottleMs(Math.round(next));
  } catch {
    return SEND_ON_CHANGE_THROTTLE_MS_DEFAULT;
  }
}
