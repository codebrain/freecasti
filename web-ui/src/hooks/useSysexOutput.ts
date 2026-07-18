import { useMemo } from "react";
import type { DumpSpec } from "@/spec/types";
import type { ProgSerializeState } from "@/sysex/serialize";
import type { ProgUiRuntime } from "@/prog/uiState";
import { computeSysexOutput } from "@/sysex/computeSysexOutput";

export type ActiveTab = "prog" | "system";

export type { SysexOutput } from "@/sysex/computeSysexOutput";

export function useSysexOutput(
  progState: ProgSerializeState | null,
  sysState: Record<string, number> | null,
  activeTab: ActiveTab,
  progSpec: DumpSpec | null,
  sysSpec: DumpSpec | null,
  progTemplate: Uint8Array | null,
  sysTemplate: Uint8Array | null,
  progUi?: ProgUiRuntime | null,
) {
  return useMemo(
    () =>
      computeSysexOutput(
        progState,
        sysState,
        activeTab,
        progSpec,
        sysSpec,
        progTemplate,
        sysTemplate,
        progUi,
      ),
    [
      progState,
      sysState,
      activeTab,
      progSpec,
      sysSpec,
      progTemplate,
      sysTemplate,
      progUi,
    ],
  );
}
