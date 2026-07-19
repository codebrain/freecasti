import { describe, expect, it } from "vitest";

import { PROGRAM_MESSAGE_LENGTH, SYSEX_END, SYSEX_START } from "@/sysex/frame";

import {
  TX_ECHO_WINDOW_MS,
  classifyRxAgainstPendingTx,
  pendingTxEchoFromBytes,
} from "./txEcho";

function progDump(byteAt8 = 0x41): Uint8Array {
  const bytes = new Uint8Array(PROGRAM_MESSAGE_LENGTH);
  bytes[0] = SYSEX_START;
  bytes[6] = 0x01;
  bytes[8] = byteAt8;
  bytes[bytes.length - 1] = SYSEX_END;
  return bytes;
}

describe("txEcho", () => {
  it("tracks pending TX for program dumps", () => {
    const bytes = progDump();
    const pending = pendingTxEchoFromBytes(bytes, 1000);
    expect(pending).not.toBeNull();
    expect(pending?.family).toBe("prog");
    expect(pending?.bytes).toEqual(bytes);
  });

  it("classifies matching echo", () => {
    const bytes = progDump();
    const pending = pendingTxEchoFromBytes(bytes, 1000)!;
    const result = classifyRxAgainstPendingTx(bytes, pending, 1500);
    expect(result).toEqual({
      kind: "echo",
      validation: "match",
      diffCount: 0,
    });
  });

  it("classifies mismatching echo", () => {
    const sent = progDump(0x41);
    const echoed = progDump(0x42);
    const pending = pendingTxEchoFromBytes(sent, 1000)!;
    const result = classifyRxAgainstPendingTx(echoed, pending, 1500);
    expect(result).toEqual({
      kind: "echo",
      validation: "mismatch",
      diffCount: 1,
    });
  });

  it("treats late RX as unsolicited", () => {
    const bytes = progDump();
    const pending = pendingTxEchoFromBytes(bytes, 1000)!;
    const result = classifyRxAgainstPendingTx(
      bytes,
      pending,
      1000 + TX_ECHO_WINDOW_MS + 1,
    );
    expect(result).toEqual({ kind: "unsolicited" });
  });

  it("treats different dump family as unsolicited", () => {
    const prog = progDump();
    const sys = new Uint8Array(77);
    sys[0] = SYSEX_START;
    sys[6] = 0x02;
    sys[sys.length - 1] = SYSEX_END;
    const pending = pendingTxEchoFromBytes(prog, 1000)!;
    const result = classifyRxAgainstPendingTx(sys, pending, 1500);
    expect(result).toEqual({ kind: "unsolicited" });
  });
});
