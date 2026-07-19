import type { ControlDef } from "@/spec/controls";
import type { BankInfo } from "@/presets/types";
import { abSlotSelectorFromState } from "@/presets/progAbSlot";
import type { DumpSpec } from "@/spec/types";
import {
  detectDumpFamily,
  hydrateProgramFromBytes,
  hydrateSystemFromBytes,
} from "@/sysex/hydrate";
import type { ProgSerializeState } from "@/sysex/serialize";

export type MidiReceiveResult =
  | {
      family: "prog";
      state: ProgSerializeState;
      bankIdx: number;
      presetSlot: number;
    }
  | { family: "system"; state: Record<string, number> };

/** Parse an incoming SysEx dump from MIDI without touching React state. */
export function parseMidiReceive(
  data: Uint8Array,
  progSpec: DumpSpec,
  progControls: ControlDef[],
  sysControls: ControlDef[],
  banks: BankInfo[],
): MidiReceiveResult | null {
  const family = detectDumpFamily(data);
  if (!family) return null;

  if (family === "prog") {
    const state = hydrateProgramFromBytes(data, progSpec, progControls);
    const selector = abSlotSelectorFromState(banks, state);
    return {
      family: "prog",
      state,
      bankIdx: selector.bankIdx,
      presetSlot: selector.presetSlot,
    };
  }

  return {
    family: "system",
    state: hydrateSystemFromBytes(data, sysControls),
  };
}
