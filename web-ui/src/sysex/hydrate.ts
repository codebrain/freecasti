import type { ControlDef } from "@/spec/controls";
import type { DumpSpec, SpecField } from "@/spec/types";
import { decodeAtOffsets } from "./encodings";
import {
  DATA_OFFSET,
  NAME_LENGTH,
  NAME_OFFSET,
  PROGRAM_MESSAGE_LENGTH,
  SYSTEM_MESSAGE_LENGTH,
} from "./frame";
import { withProgUiIdle } from "@/prog/uiState";

function readProgramName(data: Uint8Array): string {
  const slice = data.subarray(NAME_OFFSET, NAME_OFFSET + NAME_LENGTH);
  return new TextDecoder("ascii").decode(slice).replace(/\s+$/, "");
}

function hydrateEncoded(
  data: Uint8Array,
  controls: ControlDef[],
): Record<string, number> {
  const encoded: Record<string, number> = {};
  for (const c of controls) {
    encoded[c.fieldId] = decodeAtOffsets(data, c.offsets, c.encoding);
  }
  return encoded;
}

export function hydrateProgramFromBytes(
  data: Uint8Array,
  spec: DumpSpec,
  controls: ControlDef[],
): ProgSerializeState {
  if (data.length !== PROGRAM_MESSAGE_LENGTH) {
    throw new Error(`expected ${PROGRAM_MESSAGE_LENGTH}-byte program dump`);
  }
  const encoded = hydrateEncoded(data, controls);

  for (const field of spec.fields) {
    if (field.id === "bank_index" || field.id === "program_slot") {
      if (field.encoding) {
        encoded[field.id] = decodeAtOffsets(data, field.offsets, field.encoding);
      }
    }
  }

  return withProgUiIdle({
    programName: readProgramName(data),
    encoded,
  });
}

export function hydrateSystemFromBytes(
  data: Uint8Array,
  controls: ControlDef[],
): Record<string, number> {
  if (data.length !== SYSTEM_MESSAGE_LENGTH) {
    throw new Error(`expected ${SYSTEM_MESSAGE_LENGTH}-byte system dump`);
  }
  return hydrateEncoded(data, controls);
}

export function detectDumpFamily(data: Uint8Array): "prog" | "system" | null {
  if (data.length === PROGRAM_MESSAGE_LENGTH && data[6] === 0x01) return "prog";
  if (data.length === SYSTEM_MESSAGE_LENGTH && data[6] === 0x02) return "system";
  return null;
}

import { readSyxFromFile } from "./syxIo";

export async function loadSyxFile(file: Blob): Promise<Uint8Array> {
  return readSyxFromFile(file);
}
