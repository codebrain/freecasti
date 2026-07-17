import { detectDumpFamily } from "@/sysex/hydrate";
import { NAME_LENGTH, NAME_OFFSET, SYSEX_END, SYSEX_START } from "@/sysex/frame";

export type MidiLogDirection = "tx" | "rx";

export interface MidiLogEntry {
  id: string;
  at: number;
  direction: MidiLogDirection;
  bytes: Uint8Array;
  summary: string;
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

export function summarizeMidiSysex(bytes: Uint8Array): string {
  const family = detectDumpFamily(bytes);
  if (family === "prog") {
    const name = readProgramName(bytes);
    return name
      ? `program ${bytes.length} B · ${name}`
      : `program ${bytes.length} B`;
  }
  if (family === "system") {
    return `system ${bytes.length} B`;
  }
  return `sysex ${bytes.length} B`;
}

export function prependMidiLog(
  prev: readonly MidiLogEntry[],
  entry: MidiLogEntry,
  max = MIDI_LOG_MAX,
): MidiLogEntry[] {
  return [entry, ...prev].slice(0, max);
}

export function createMidiLogEntry(
  direction: MidiLogDirection,
  bytes: Uint8Array,
  at = Date.now(),
): MidiLogEntry {
  return {
    id: `${at}-${direction}-${Math.random().toString(36).slice(2, 9)}`,
    at,
    direction,
    bytes: new Uint8Array(bytes),
    summary: summarizeMidiSysex(bytes),
  };
}
