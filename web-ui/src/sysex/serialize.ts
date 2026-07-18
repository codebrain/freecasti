import type { SpecField } from "@/spec/types";
import type { ProgUiRuntime } from "@/prog/uiState";
import { applyProgUiBytes, resolveProgUi } from "@/prog/uiState";
import { encodeAtOffsets } from "./encodings";
import {
  NAME_LENGTH,
  NAME_OFFSET,
  PROGRAM_MESSAGE_LENGTH,
  SYSTEM_MESSAGE_LENGTH,
  writeProgramDumpChecksum,
  writeSystemDumpChecksum,
} from "./frame";

import type { ProgUiState } from "@/prog/uiState";

export interface ProgSerializeState {
  programName: string;
  encoded: Record<string, number>;
  ui?: ProgUiState;
}

export type SysSerializeState = Record<string, number>;

function patchField(
  buf: Uint8Array,
  field: SpecField,
  encoded: number,
): void {
  const encoding = field.encoding;
  if (!encoding || encoding === "ascii_space_padded") return;
  const wire = encodeAtOffsets(encoded, encoding, field.offsets.length);
  for (let i = 0; i < wire.length; i++) {
    buf[field.start + i] = wire[i];
  }
}

function patchProgramName(buf: Uint8Array, name: string): void {
  const ascii = new TextEncoder().encode(name);
  const slice = ascii.subarray(0, NAME_LENGTH);
  buf.fill(0x20, NAME_OFFSET, NAME_OFFSET + NAME_LENGTH);
  buf.set(slice, NAME_OFFSET);
  for (let i = slice.length; i < NAME_LENGTH; i++) {
    buf[NAME_OFFSET + i] = 0x20;
  }
}

export function buildProgramDump(
  state: ProgSerializeState,
  fields: SpecField[],
  template: Uint8Array,
  progUi?: ProgUiRuntime | null,
): Uint8Array {
  if (template.length !== PROGRAM_MESSAGE_LENGTH) {
    throw new Error(`program template length ${template.length} != ${PROGRAM_MESSAGE_LENGTH}`);
  }
  const buf = new Uint8Array(template);
  patchProgramName(buf, state.programName);

  for (const field of fields) {
    if (field.kind === "checksum" || field.kind === "frame") continue;
    if (field.id === "program_name") continue;
    const val = state.encoded[field.id];
    if (val === undefined) continue;
    patchField(buf, field, val);
  }

  const bank = state.encoded.bank_index;
  if (bank !== undefined) {
    const mirrorField = fields.find((f) => f.id === "bank_index_mirror");
    if (mirrorField) {
      patchField(buf, mirrorField, bank & 0x0f);
    }
  }

  if (progUi) {
    applyProgUiBytes(buf, resolveProgUi(state), progUi);
  }

  writeProgramDumpChecksum(buf);
  return buf;
}

export function buildSystemDump(
  state: SysSerializeState,
  fields: SpecField[],
  template: Uint8Array,
): Uint8Array {
  if (template.length !== SYSTEM_MESSAGE_LENGTH) {
    throw new Error(`system template length ${template.length} != ${SYSTEM_MESSAGE_LENGTH}`);
  }
  const buf = new Uint8Array(template);

  for (const field of fields) {
    if (field.kind === "checksum" || field.kind === "frame") continue;
    const val = state[field.id];
    if (val === undefined) continue;
    patchField(buf, field, val);
  }

  writeSystemDumpChecksum(buf);
  return buf;
}
