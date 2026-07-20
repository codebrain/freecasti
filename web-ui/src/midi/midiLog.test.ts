import { describe, expect, it } from "vitest";

import {
  createMidiLogEntry,
  isMidiSysex,
  prependMidiLog,
  summarizeMidiSysex,
} from "./midiLog";
import { PROGRAM_MESSAGE_LENGTH, SYSEX_END, SYSEX_START } from "@/sysex/frame";

describe("midiLog", () => {
  it("detects SysEx framing", () => {
    expect(isMidiSysex(new Uint8Array([SYSEX_START, 1, SYSEX_END]))).toBe(true);
    expect(isMidiSysex(new Uint8Array([0x90, 60, 100]))).toBe(false);
  });

  it("summarizes program and system dumps", () => {
    const prog = new Uint8Array(PROGRAM_MESSAGE_LENGTH);
    prog[0] = SYSEX_START;
    prog[6] = 0x01;
    prog[prog.length - 1] = SYSEX_END;
    prog[8] = 0x41; // 'A'
    expect(summarizeMidiSysex(prog)).toContain("program 157 B");

    const sys = new Uint8Array(77);
    sys[0] = SYSEX_START;
    sys[6] = 0x02;
    sys[sys.length - 1] = SYSEX_END;
    expect(summarizeMidiSysex(sys)).toBe("system 77 B");
  });

  it("keeps only the most recent entries", () => {
    const mk = (n: number) =>
      createMidiLogEntry("tx", new Uint8Array([SYSEX_START, n, SYSEX_END]));
    let log = prependMidiLog([], mk(1));
    log = prependMidiLog(log, mk(2));
    log = prependMidiLog(log, mk(3), 2);
    expect(log).toHaveLength(2);
    expect(log[0].bytes[1]).toBe(3);
    expect(log[1].bytes[1]).toBe(2);
  });

  it("defaults to a 10-message history", () => {
    const mk = (n: number) =>
      createMidiLogEntry("tx", new Uint8Array([SYSEX_START, n, SYSEX_END]));
    let log: ReturnType<typeof createMidiLogEntry>[] = [];
    for (let n = 0; n < 15; n++) {
      log = prependMidiLog(log, mk(n));
    }
    expect(log).toHaveLength(10);
    expect(log[0].bytes[1]).toBe(14);
    expect(log[9].bytes[1]).toBe(5);
  });
});
