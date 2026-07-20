import type { ControlDef } from "@/spec/controls";
import type { BankInfo } from "@/presets/types";
import { abSlotSelectorFromState } from "@/presets/progAbSlot";
import type { DumpSpec } from "@/spec/types";
import {
  detectDumpFamily,
  hydrateProgramFromBytes,
  hydrateSystemFromBytes,
} from "@/sysex/hydrate";
import {
  decodeRegisterBasisBlob,
  type RegBlobLayout,
} from "@/sysex/registerBasisBlob";
import type { ProgSerializeState } from "@/sysex/serialize";

export type MidiReceiveResult =
  | {
      family: "prog";
      state: ProgSerializeState;
      bankIdx: number;
      presetSlot: number;
    }
  | { family: "system"; state: Record<string, number> };

/**
 * When the dump carries a register basis frame (offsets 24-87 nibble-packed),
 * prefer the stored register settings over the live payload bytes: the blob
 * snapshots the register as stored, while the payload tracks the edit buffer
 * (which may hold unstored edits). Returns the state unchanged for factory /
 * parameter-series dumps where the region is the space pad.
 */
export function applyRegisterBasis(
  data: Uint8Array,
  layout: RegBlobLayout,
  state: ProgSerializeState,
): ProgSerializeState {
  const basis = decodeRegisterBasisBlob(data, layout);
  if (!basis) return state;
  const encoded = { ...state.encoded };
  for (const field of layout.fields) {
    if (field.id === "name" || !field.payloadField) continue;
    if (!(field.payloadField in encoded)) continue;
    encoded[field.payloadField] = basis.values[field.id]!;
  }
  return { ...state, programName: basis.name, encoded };
}

/** Parse an incoming SysEx dump from MIDI without touching React state. */
export function parseMidiReceive(
  data: Uint8Array,
  progSpec: DumpSpec,
  progControls: ControlDef[],
  sysControls: ControlDef[],
  banks: BankInfo[],
  regBlob?: RegBlobLayout | null,
): MidiReceiveResult | null {
  const family = detectDumpFamily(data);
  if (!family) return null;

  if (family === "prog") {
    let state = hydrateProgramFromBytes(data, progSpec, progControls);
    if (regBlob) {
      state = applyRegisterBasis(data, regBlob, state);
    }
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
