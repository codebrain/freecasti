import { describe, expect, it } from "vitest";
import type { ProgSerializeState } from "@/sysex/serialize";
import { resolveSendOnChange, type SendOnChangeInput } from "./sendOnChange";

const progA = { tag: "progA" } as unknown as ProgSerializeState;
const progB = { tag: "progB" } as unknown as ProgSerializeState;
const sysA: Record<string, number> = { a: 1 };
const sysB: Record<string, number> = { a: 2 };

const PROG_BYTES = new Uint8Array([0xf0, 0x01, 0xf7]);
const SYS_BYTES = new Uint8Array([0xf0, 0x02, 0xf7]);

function baseInput(over: Partial<SendOnChangeInput> = {}): SendOnChangeInput {
  return {
    suppressed: false,
    prevProg: progA,
    progState: progA,
    prevSys: sysA,
    sysState: sysA,
    transmit: true,
    progBytes: PROG_BYTES,
    sysBytes: SYS_BYTES,
    ...over,
  };
}

describe("resolveSendOnChange", () => {
  it("does nothing when nothing changed", () => {
    const result = resolveSendOnChange(baseInput());
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([]);
    expect(result.suppressionConsumed).toBe(false);
    expect(result.nextPrevProg).toBe(progA);
    expect(result.nextPrevSys).toBe(sysA);
  });

  it("transmits a changed program dump when transmit is enabled", () => {
    const result = resolveSendOnChange(
      baseInput({ progState: progB, transmit: true }),
    );
    expect(result.send).toEqual([PROG_BYTES]);
    expect(result.logDebug).toEqual([]);
    expect(result.nextPrevProg).toBe(progB);
  });

  it("transmits a changed system dump when transmit is enabled", () => {
    const result = resolveSendOnChange(
      baseInput({ sysState: sysB, transmit: true }),
    );
    expect(result.send).toEqual([SYS_BYTES]);
    expect(result.logDebug).toEqual([]);
    expect(result.nextPrevSys).toBe(sysB);
  });

  it("logs debug only (no transmit) when transmit is disabled", () => {
    const result = resolveSendOnChange(
      baseInput({ progState: progB, sysState: sysB, transmit: false }),
    );
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([PROG_BYTES, SYS_BYTES]);
  });

  it("only sends the family that changed", () => {
    const result = resolveSendOnChange(baseInput({ progState: progB }));
    expect(result.send).toEqual([PROG_BYTES]);
  });

  it("never transmits or echoes an RX (suppressed) update, even with transmit enabled", () => {
    const result = resolveSendOnChange(
      baseInput({
        suppressed: true,
        progState: progB,
        sysState: sysB,
        transmit: true,
      }),
    );
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([]);
  });

  it("adopts the RX update as the new baseline and consumes suppression", () => {
    const result = resolveSendOnChange(
      baseInput({ suppressed: true, progState: progB, sysState: sysB }),
    );
    expect(result.suppressionConsumed).toBe(true);
    expect(result.nextPrevProg).toBe(progB);
    expect(result.nextPrevSys).toBe(sysB);
  });

  it("does not echo an RX update to the debug log even when transmit is disabled", () => {
    const result = resolveSendOnChange(
      baseInput({
        suppressed: true,
        progState: progB,
        sysState: sysB,
        transmit: false,
      }),
    );
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([]);
  });

  it("transmits a subsequent user edit after an RX baseline was adopted", () => {
    // Simulate the RX step first.
    const rx = resolveSendOnChange(
      baseInput({ suppressed: true, progState: progB, sysState: sysB }),
    );
    // Then a user edit changes prog again; baseline is the RX state.
    const progC = { tag: "progC" } as unknown as ProgSerializeState;
    const user = resolveSendOnChange(
      baseInput({
        suppressed: false,
        prevProg: rx.nextPrevProg,
        progState: progC,
        prevSys: rx.nextPrevSys,
        sysState: sysB,
        transmit: true,
      }),
    );
    expect(user.send).toEqual([PROG_BYTES]);
    expect(user.nextPrevProg).toBe(progC);
  });

  it("does nothing and preserves the baseline when state is not ready", () => {
    const result = resolveSendOnChange(
      baseInput({ suppressed: true, progState: null, sysState: null }),
    );
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([]);
    expect(result.suppressionConsumed).toBe(false);
    expect(result.nextPrevProg).toBe(progA);
    expect(result.nextPrevSys).toBe(sysA);
  });

  it("establishes a baseline without sending when prev is null (first load)", () => {
    const result = resolveSendOnChange(
      baseInput({ prevProg: null, prevSys: null, progState: progB, sysState: sysB }),
    );
    expect(result.send).toEqual([]);
    expect(result.logDebug).toEqual([]);
    expect(result.nextPrevProg).toBe(progB);
    expect(result.nextPrevSys).toBe(sysB);
  });
});
