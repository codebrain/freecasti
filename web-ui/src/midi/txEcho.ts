import { detectDumpFamily } from "@/sysex/hydrate";
import { sysexByteDiffCount, sysexBytesEqual } from "@/midi/sysexCompare";

export type DumpFamily = "prog" | "system";

export interface PendingTxEcho {
  bytes: Uint8Array;
  sentAt: number;
  family: DumpFamily;
}

export const TX_ECHO_WINDOW_MS = 3000;

export type TxEchoClassification =
  | { kind: "echo"; validation: "match" | "mismatch"; diffCount: number }
  | { kind: "unsolicited" };

export function pendingTxEchoFromBytes(
  bytes: Uint8Array,
  sentAt = Date.now(),
): PendingTxEcho | null {
  const family = detectDumpFamily(bytes);
  if (family !== "prog" && family !== "system") return null;
  return { bytes: new Uint8Array(bytes), sentAt, family };
}

export function classifyRxAgainstPendingTx(
  rx: Uint8Array,
  pending: PendingTxEcho | null,
  now = Date.now(),
): TxEchoClassification {
  if (!pending) return { kind: "unsolicited" };
  if (now - pending.sentAt > TX_ECHO_WINDOW_MS) return { kind: "unsolicited" };

  const rxFamily = detectDumpFamily(rx);
  if (rxFamily !== pending.family) return { kind: "unsolicited" };

  if (sysexBytesEqual(rx, pending.bytes)) {
    return { kind: "echo", validation: "match", diffCount: 0 };
  }

  return {
    kind: "echo",
    validation: "mismatch",
    diffCount: sysexByteDiffCount(rx, pending.bytes),
  };
}
