import { detectDumpFamily } from "@/sysex/hydrate";
import { NAME_LENGTH, NAME_OFFSET, SYSEX_END, SYSEX_START } from "@/sysex/frame";

export type MidiLogDirection = "tx" | "rx";

export type MidiEchoValidation = "match" | "mismatch";

export interface MidiLogEntry {
  id: string;
  at: number;
  direction: MidiLogDirection;
  bytes: Uint8Array;
  summary: string;
  /** Set when an RX message is the device echo of a recent TX. */
  echoValidation?: MidiEchoValidation;
  echoDiffCount?: number;
}

export const MIDI_LOG_MAX = 10;

export function isMidiSysex(data: Uint8Array): boolean {
  return data.length >= 2 && data[0] === SYSEX_START && data[data.length - 1] === SYSEX_END;
}

function readProgramName(data: Uint8Array): string | null {
  if (data.length < NAME_OFFSET + NAME_LENGTH) return null;
  const name = new TextDecoder("ascii")
    .decode(data.subarray(NAME_OFFSET, NAME_OFFSET + NAME_LENGTH))
    .replace(/\s+$/, "");
  return name || null;
}

export function summarizeMidiSysex(
  bytes: Uint8Array,
  options: {
    echoValidation?: MidiEchoValidation;
    echoDiffCount?: number;
  } = {},
): string {
  const family = detectDumpFamily(bytes);
  let base: string;
  if (family === "prog") {
    const name = readProgramName(bytes);
    base = name
      ? `program ${bytes.length} B · ${name}`
      : `program ${bytes.length} B`;
  } else if (family === "system") {
    base = `system ${bytes.length} B`;
  } else {
    base = `sysex ${bytes.length} B`;
  }

  if (options.echoValidation === "match") {
    return `${base} · echo match`;
  }
  if (options.echoValidation === "mismatch") {
    const n = options.echoDiffCount ?? 0;
    return `${base} · echo mismatch (${n} B)`;
  }
  return base;
}

export function prependMidiLog(
  prev: readonly MidiLogEntry[],
  entry: MidiLogEntry,
  max = MIDI_LOG_MAX,
): MidiLogEntry[] {
  return [entry, ...prev].slice(0, max);
}

export interface MidiLogEntryOptions {
  at?: number;
  echoValidation?: MidiEchoValidation;
  echoDiffCount?: number;
}

export function createMidiLogEntry(
  direction: MidiLogDirection,
  bytes: Uint8Array,
  options: MidiLogEntryOptions = {},
): MidiLogEntry {
  const at = options.at ?? Date.now();
  return {
    id: `${at}-${direction}-${Math.random().toString(36).slice(2, 9)}`,
    at,
    direction,
    bytes: new Uint8Array(bytes),
    summary: summarizeMidiSysex(bytes, {
      echoValidation: options.echoValidation,
      echoDiffCount: options.echoDiffCount,
    }),
    echoValidation: options.echoValidation,
    echoDiffCount: options.echoDiffCount,
  };
}
