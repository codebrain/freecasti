import type { ProgSerializeState } from "@/sysex/serialize";
import { base64ToBytes, bytesToBase64 } from "@/sysex/syxIo";

export const LS_USER_PRESETS = "m7.userPresets";

export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export interface SavedUserPreset {
  id: string;
  name: string;
  savedAt: string;
  prog: {
    state: ProgSerializeState;
    syxBase64: string;
  };
  sys?: {
    state: Record<string, number>;
    syxBase64: string;
  };
}

function readAll(storage: StorageLike): SavedUserPreset[] {
  try {
    const raw = storage.getItem(LS_USER_PRESETS);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as SavedUserPreset[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeAll(storage: StorageLike, presets: SavedUserPreset[]): void {
  storage.setItem(LS_USER_PRESETS, JSON.stringify(presets));
}

export function listUserPresets(storage: StorageLike): SavedUserPreset[] {
  return readAll(storage).sort((a, b) => b.savedAt.localeCompare(a.savedAt));
}

export function getUserPreset(
  storage: StorageLike,
  id: string,
): SavedUserPreset | undefined {
  return readAll(storage).find((p) => p.id === id);
}

export function saveUserPreset(
  storage: StorageLike,
  name: string,
  progState: ProgSerializeState,
  progBytes: Uint8Array,
  sysState?: Record<string, number>,
  sysBytes?: Uint8Array,
): SavedUserPreset {
  const trimmed = name.trim();
  if (!trimmed) {
    throw new Error("preset name is required");
  }

  const entry: SavedUserPreset = {
    id: crypto.randomUUID(),
    name: trimmed,
    savedAt: new Date().toISOString(),
    prog: {
      state: progState,
      syxBase64: bytesToBase64(progBytes),
    },
  };

  if (sysState && sysBytes) {
    entry.sys = {
      state: sysState,
      syxBase64: bytesToBase64(sysBytes),
    };
  }

  const presets = readAll(storage);
  presets.push(entry);
  writeAll(storage, presets);
  return entry;
}

export function updateUserPreset(
  storage: StorageLike,
  id: string,
  patch: Partial<Pick<SavedUserPreset, "name">>,
): SavedUserPreset {
  const presets = readAll(storage);
  const idx = presets.findIndex((p) => p.id === id);
  if (idx < 0) throw new Error(`preset not found: ${id}`);
  if (patch.name !== undefined) {
    const trimmed = patch.name.trim();
    if (!trimmed) throw new Error("preset name is required");
    presets[idx] = { ...presets[idx], name: trimmed };
  }
  writeAll(storage, presets);
  return presets[idx];
}

export function deleteUserPreset(storage: StorageLike, id: string): void {
  const presets = readAll(storage).filter((p) => p.id !== id);
  writeAll(storage, presets);
}

export function progBytesFromSaved(preset: SavedUserPreset): Uint8Array {
  return base64ToBytes(preset.prog.syxBase64);
}

export function sysBytesFromSaved(preset: SavedUserPreset): Uint8Array | null {
  return preset.sys ? base64ToBytes(preset.sys.syxBase64) : null;
}
