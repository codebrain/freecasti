export const SYSEX_SEND_MIN_INTERVAL_MS = 500;

export interface SysexSendThrottle {
  enqueue: (bytes: Uint8Array) => void;
  dispose: () => void;
}

/** Coalesce rapid SysEx updates; flush at most once per `minIntervalMs`. */
export function createSysexSendThrottle(
  sendImmediate: (bytes: Uint8Array) => void,
  minIntervalMs = SYSEX_SEND_MIN_INTERVAL_MS,
  now: () => number = Date.now,
): SysexSendThrottle {
  let pending: Uint8Array | null = null;
  let timer: ReturnType<typeof setTimeout> | null = null;
  let lastSendAt = 0;

  const flush = () => {
    timer = null;
    if (!pending) return;
    const bytes = pending;
    pending = null;
    sendImmediate(bytes);
    lastSendAt = now();
    if (pending) schedule();
  };

  const schedule = () => {
    if (timer) return;
    const delay =
      lastSendAt > 0
        ? Math.max(0, minIntervalMs - (now() - lastSendAt))
        : minIntervalMs;
    timer = setTimeout(flush, delay);
  };

  const enqueue = (bytes: Uint8Array) => {
    pending = new Uint8Array(bytes);
    schedule();
  };

  const dispose = () => {
    if (timer) clearTimeout(timer);
    timer = null;
    pending = null;
  };

  return { enqueue, dispose };
}
