import type { ControlDef } from "@/spec/controls";
import {
  buildParameterToFieldId,
  buildSystemControls,
  defaultEncodedState,
} from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { groupPresetsByBank } from "@/presets/catalog";
import {
  createInitialAbStore,
  type ProgAbStore,
} from "@/presets/progAbSlot";
import type { PresetCatalog } from "@/presets/types";
import type { StorageLike } from "@/presets/userPresets";
import {
  loadRestoredProgState,
  loadRestoredSysState,
  loadStoredAbStore,
} from "./persistedState";

export interface BootstrapResult {
  abStore: ProgAbStore;
  sysState: Record<string, number>;
  sysControls: ControlDef[];
}

export function bootstrapAppState(
  prog: DumpSpec,
  sys: DumpSpec,
  presets: PresetCatalog,
  storage: StorageLike = localStorage,
): BootstrapResult {
  const sysControls = buildSystemControls(sys);
  const groupedBanks = groupPresetsByBank(presets);
  const paramMap = buildParameterToFieldId(prog);

  const restoredAb = loadStoredAbStore(storage);
  const restoredProg = loadRestoredProgState(storage);
  const restoredSys = loadRestoredSysState(storage);

  const abStore =
    restoredAb ??
    createInitialAbStore(groupedBanks, presets, paramMap, restoredProg);

  const sysState = restoredSys ?? defaultEncodedState(sysControls);

  return { abStore, sysState, sysControls };
}
