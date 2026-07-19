import type { ProgAbStore } from "@/presets/progAbSlot";
import { parseStoredAbStore } from "@/presets/progAbSlot";
import type { StorageLike } from "@/presets/userPresets";
import type { ActiveTab } from "@/hooks/useSysexOutput";
import type { ProgSerializeState } from "@/sysex/serialize";
import {
  LS_LOCKED,
  LS_PROG,
  LS_PROG_AB,
  LS_SYS,
  LS_TAB,
  LS_TEMPO_MODE,
} from "./storageKeys";

function parseStringSet(raw: string | null): Set<string> {
  if (!raw) return new Set();
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return new Set();
    return new Set(parsed.filter((id): id is string => typeof id === "string"));
  } catch {
    return new Set();
  }
}

export function loadTempoModeFields(storage: StorageLike = localStorage): Set<string> {
  return parseStringSet(storage.getItem(LS_TEMPO_MODE));
}

export function loadLockedFields(storage: StorageLike = localStorage): Set<string> {
  return parseStringSet(storage.getItem(LS_LOCKED));
}

export function loadStoredAbStore(storage: StorageLike = localStorage): ProgAbStore | null {
  try {
    const raw = storage.getItem(LS_PROG_AB);
    if (!raw) return null;
    return parseStoredAbStore(JSON.parse(raw));
  } catch {
    return null;
  }
}

export function loadActiveTab(storage: StorageLike = localStorage): ActiveTab {
  try {
    const tab = storage.getItem(LS_TAB);
    return tab === "system" ? "system" : "prog";
  } catch {
    return "prog";
  }
}

export function loadRestoredProgState(
  storage: StorageLike = localStorage,
): ProgSerializeState | null {
  try {
    const raw = storage.getItem(LS_PROG);
    if (!raw) return null;
    return JSON.parse(raw) as ProgSerializeState;
  } catch {
    return null;
  }
}

export function loadRestoredSysState(
  storage: StorageLike = localStorage,
): Record<string, number> | null {
  try {
    const raw = storage.getItem(LS_SYS);
    if (!raw) return null;
    return JSON.parse(raw) as Record<string, number>;
  } catch {
    return null;
  }
}
