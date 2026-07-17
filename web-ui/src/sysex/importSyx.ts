import type { ControlDef } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import {
  detectDumpFamily,
  hydrateProgramFromBytes,
  hydrateSystemFromBytes,
} from "./hydrate";
import type { ProgSerializeState } from "./serialize";
import { parseSyxBytes } from "./syxIo";

export interface ImportSyxResult {
  family: "prog" | "system";
  progState?: ProgSerializeState;
  sysState?: Record<string, number>;
}

export function importSyxBytes(
  data: Uint8Array,
  progSpec: DumpSpec,
  progControls: ControlDef[],
  sysControls: ControlDef[],
): ImportSyxResult {
  const bytes = parseSyxBytes(data);
  const family = detectDumpFamily(bytes);
  if (!family) {
    throw new Error(
      "unrecognized SysEx dump (expected 157-byte program or 77-byte system)",
    );
  }
  if (family === "prog") {
    return {
      family,
      progState: hydrateProgramFromBytes(bytes, progSpec, progControls),
    };
  }
  return {
    family,
    sysState: hydrateSystemFromBytes(bytes, sysControls),
  };
}
