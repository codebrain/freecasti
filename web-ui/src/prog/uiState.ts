import { encodeAtOffsets } from "@/sysex/encodings";
import type { ProgSerializeState } from "@/sysex/serialize";

export type ProgUiMode = "idle" | "browse" | "edit";

export interface ProgUiState {
  mode: ProgUiMode;
  /** Catalog ``folder_hint`` when ``mode`` is ``browse`` or ``edit``. */
  parameter?: string;
}

export interface ProgUiByteMap {
  "92": number;
  "98": number;
  "99": number;
  "146": number;
  "147": number;
}

export interface ProgUiParameterEntry {
  index: number;
  browse?: ProgUiByteMap;
  edit?: { "92": number; "146": number; "147": number };
}

export interface ProgUiRuntime {
  idle: ProgUiByteMap;
  menu_order: string[];
  by_parameter: Record<string, ProgUiParameterEntry>;
}

export const UI_OFFSETS = ["92", "98", "99", "146", "147"] as const;

/**
 * Offset 92 panel-mode value while the front-panel favorites screen is
 * displayed (see sysex/prog/favorites/). Not a parameter menu state.
 */
export const FAVORITES_SCREEN_FLAG = 8;

function writeUiMap(buf: Uint8Array, map: ProgUiByteMap): void {
  for (const key of UI_OFFSETS) {
    buf[Number(key)] = map[key];
  }
}

export function defaultProgUiState(): ProgUiState {
  return { mode: "idle" };
}

export function withProgUiIdle(state: ProgSerializeState): ProgSerializeState {
  return { ...state, ui: defaultProgUiState() };
}

export function resolveProgUi(state: ProgSerializeState): ProgUiState {
  return state.ui ?? defaultProgUiState();
}

export function applyProgUiBytes(
  buf: Uint8Array,
  ui: ProgUiState,
  progUi: ProgUiRuntime,
): void {
  if (ui.mode === "idle" || !ui.parameter) {
    writeUiMap(buf, progUi.idle);
    return;
  }

  const row = progUi.by_parameter[ui.parameter];
  if (!row) {
    writeUiMap(buf, progUi.idle);
    return;
  }

  if (ui.mode === "browse" && row.browse) {
    writeUiMap(buf, row.browse);
    return;
  }

  const edit = row.edit;
  const browse = row.browse;
  const idle = progUi.idle;

  buf[92] = browse?.["92"] ?? 2;
  const wire = encodeAtOffsets(row.index, "nibble_hilo", 2);
  buf[98] = wire[0]!;
  buf[99] = wire[1]!;
  buf[146] = edit?.["146"] ?? browse?.["146"] ?? idle["146"];
  buf[147] = edit?.["147"] ?? browse?.["147"] ?? idle["147"];
}

export function decodeProgUiFromBytes(
  data: Uint8Array,
  progUi: ProgUiRuntime,
): ProgUiState {
  if (data[92] === FAVORITES_SCREEN_FLAG) {
    // Favorites screen: no parameter menu open.
    return { mode: "idle" };
  }
  const idle = progUi.idle;
  if (
    data[92] === idle["92"] &&
    data[98] === idle["98"] &&
    data[99] === idle["99"] &&
    data[146] === idle["146"] &&
    data[147] === idle["147"]
  ) {
    return { mode: "idle" };
  }

  const menuIndex = (data[98]! << 4) | data[99]!;
  const parameter = progUi.menu_order[menuIndex];
  if (!parameter) {
    return { mode: "idle" };
  }

  if (data[92] === 2) {
    const row = progUi.by_parameter[parameter];
    const edit = row?.edit;
    if (
      edit &&
      data[146] === edit["146"] &&
      data[147] === edit["147"]
    ) {
      return { mode: "edit", parameter };
    }
    return { mode: "browse", parameter };
  }

  return { mode: "edit", parameter };
}
