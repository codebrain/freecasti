import type { DumpSpec } from "@/spec/types";
import { buildProgramDump, buildSystemDump } from "@/sysex/serialize";
import type { ProgSerializeState } from "@/sysex/serialize";
import {
  verifyProgramDumpChecksum,
  verifySystemDumpChecksum,
} from "@/sysex/frame";
import type { ActiveTab } from "@/hooks/useSysexOutput";

export interface SysexOutput {
  progBytes: Uint8Array | null;
  sysBytes: Uint8Array | null;
  activeBytes: Uint8Array | null;
  progChecksumOk: boolean;
  sysChecksumOk: boolean;
  activeChecksumOk: boolean;
}

export function computeSysexOutput(
  progState: ProgSerializeState | null,
  sysState: Record<string, number> | null,
  activeTab: ActiveTab,
  progSpec: DumpSpec | null,
  sysSpec: DumpSpec | null,
  progTemplate: Uint8Array | null,
  sysTemplate: Uint8Array | null,
): SysexOutput {
  const progBytes =
    progState && progSpec && progTemplate
      ? buildProgramDump(progState, progSpec.fields, progTemplate)
      : null;
  const sysBytes =
    sysState && sysSpec && sysTemplate
      ? buildSystemDump(sysState, sysSpec.fields, sysTemplate)
      : null;

  const activeBytes = activeTab === "prog" ? progBytes : sysBytes;
  const progChecksumOk = progBytes ? verifyProgramDumpChecksum(progBytes) : false;
  const sysChecksumOk = sysBytes ? verifySystemDumpChecksum(sysBytes) : false;

  return {
    progBytes,
    sysBytes,
    activeBytes,
    progChecksumOk,
    sysChecksumOk,
    activeChecksumOk: activeTab === "prog" ? progChecksumOk : sysChecksumOk,
  };
}
