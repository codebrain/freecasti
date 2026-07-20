/**
 * Decodes the front-panel menu position embedded in a program dump. The M7
 * mirrors the editor's selection on its own display: a dump can point the
 * device's menu at a parameter or leave the panel idle. Offsets and the menu
 * order come from the device runtime spec (the same file the app renders).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

interface ProgUiRaw {
  idle: Record<"92" | "98" | "99" | "146" | "147", number>;
  menu_order: string[];
}

const progUi: ProgUiRaw = JSON.parse(
  fs.readFileSync(
    path.join(here, "..", "..", "public", "m7-runtime.json"),
    "utf8",
  ),
).prog_ui;

const UI_OFFSETS = ["92", "98", "99", "146", "147"] as const;
const BROWSE_MARKER_OFFSET = 92;
const MENU_INDEX_HI_OFFSET = 98;
const MENU_INDEX_LO_OFFSET = 99;

/** Parameter the dump highlights on the device display, or null if none. */
export function progMenuHighlights(bytes: Uint8Array): string | null {
  if (bytes[BROWSE_MARKER_OFFSET] !== 2) return null;
  const index =
    ((bytes[MENU_INDEX_HI_OFFSET] ?? 0) << 4) | (bytes[MENU_INDEX_LO_OFFSET] ?? 0);
  return progUi.menu_order[index] ?? null;
}

/** True when the dump leaves the device's front panel in its idle state. */
export function progMenuIdle(bytes: Uint8Array): boolean {
  return UI_OFFSETS.every((offset) => bytes[Number(offset)] === progUi.idle[offset]);
}
