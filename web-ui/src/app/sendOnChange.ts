import type { ProgSerializeState } from "@/sysex/serialize";

/**
 * Pure decision logic for the "send on change" effect.
 *
 * When state changes originate from a MIDI receive (RX) from the device, we must
 * update the controls but never transmit anything back — no TX send and no debug
 * "would-send" echo. The RX-updated state is adopted as the new baseline so that
 * a subsequent *user* edit still diffs correctly and transmits.
 *
 * Kept side-effect free so it can be unit tested; the caller performs the actual
 * `sendBytes` / `logDebugBytes` and ref updates.
 */
export interface SendOnChangeInput {
  /** True when the pending state change came from an RX dump. */
  suppressed: boolean;
  prevProg: ProgSerializeState | null;
  progState: ProgSerializeState | null;
  prevSys: Record<string, number> | null;
  sysState: Record<string, number> | null;
  /** midi.enabled && midi.sendOnChange. */
  transmit: boolean;
  progBytes: Uint8Array | null;
  sysBytes: Uint8Array | null;
}

export interface SendOnChangeResult {
  /** Payloads to transmit to the device. */
  send: Uint8Array[];
  /** Payloads to record in the debug log only (never transmitted). */
  logDebug: Uint8Array[];
  nextPrevProg: ProgSerializeState | null;
  nextPrevSys: Record<string, number> | null;
  /** True when an RX (suppressed) update was consumed and the flag should clear. */
  suppressionConsumed: boolean;
}

export function resolveSendOnChange(input: SendOnChangeInput): SendOnChangeResult {
  const {
    suppressed,
    prevProg,
    progState,
    prevSys,
    sysState,
    transmit,
    progBytes,
    sysBytes,
  } = input;

  // Not ready yet: leave the baseline untouched and do nothing.
  if (!progState || !sysState) {
    return {
      send: [],
      logDebug: [],
      nextPrevProg: prevProg,
      nextPrevSys: prevSys,
      suppressionConsumed: false,
    };
  }

  // RX-originated update: adopt as the new baseline and never echo it back.
  if (suppressed) {
    return {
      send: [],
      logDebug: [],
      nextPrevProg: progState,
      nextPrevSys: sysState,
      suppressionConsumed: true,
    };
  }

  const progChanged = prevProg !== null && progState !== prevProg;
  const sysChanged = prevSys !== null && sysState !== prevSys;

  const send: Uint8Array[] = [];
  const logDebug: Uint8Array[] = [];

  if (progChanged && progBytes) {
    (transmit ? send : logDebug).push(progBytes);
  }
  if (sysChanged && sysBytes) {
    (transmit ? send : logDebug).push(sysBytes);
  }

  return {
    send,
    logDebug,
    nextPrevProg: progState,
    nextPrevSys: sysState,
    suppressionConsumed: false,
  };
}
