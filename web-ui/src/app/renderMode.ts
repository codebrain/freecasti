import { useSyncExternalStore } from "react";
import type { StorageLike } from "@/presets/userPresets";
import { LS_RENDER_MODE } from "./storageKeys";

/**
 * Rendering compatibility mode.
 *
 * The UI leans heavily on `oklch()` colours and `color-mix()` (Chrome 111+).
 * Older browsers — notably the last Chrome that runs on Windows 7/8 (Chrome
 * 109) — cannot parse those, so every colour/gradient/shadow is dropped and
 * controls such as the knobs become invisible. "Simple" mode swaps in a plain
 * hex palette (via the `simple-mode` class on <html>) and lighter-weight
 * controls so the editor stays usable on those browsers.
 *
 * - `auto`   — pick Simple automatically when the browser lacks oklch support.
 * - `full`   — always use the rich UI.
 * - `simple` — always use the compatibility UI.
 */
export type RenderMode = "auto" | "full" | "simple";

const SIMPLE_MODE_CLASS = "simple-mode";

export function isRenderMode(value: unknown): value is RenderMode {
  return value === "auto" || value === "full" || value === "simple";
}

/** True when the browser can parse `oklch()` colours (Chrome/Edge 111+, etc.). */
export function detectOklchSupport(): boolean {
  try {
    return (
      typeof CSS !== "undefined" &&
      typeof CSS.supports === "function" &&
      CSS.supports("color", "oklch(0.5 0.1 250)")
    );
  } catch {
    return false;
  }
}

export function resolveSimpleMode(
  mode: RenderMode,
  oklchSupported: boolean,
): boolean {
  if (mode === "simple") return true;
  if (mode === "full") return false;
  return !oklchSupported;
}

function readStoredMode(storage: StorageLike): RenderMode {
  try {
    const raw = storage.getItem(LS_RENDER_MODE);
    return isRenderMode(raw) ? raw : "auto";
  } catch {
    return "auto";
  }
}

const oklchSupported = detectOklchSupport();
let currentMode: RenderMode =
  typeof localStorage !== "undefined" ? readStoredMode(localStorage) : "auto";

const listeners = new Set<() => void>();

function applyDocumentClass(): void {
  if (typeof document === "undefined") return;
  const simple = resolveSimpleMode(currentMode, oklchSupported);
  document.documentElement.classList.toggle(SIMPLE_MODE_CLASS, simple);
}

function emit(): void {
  for (const listener of listeners) listener();
}

/** Applies the initial `simple-mode` class. Call once before first render. */
export function initRenderMode(): void {
  applyDocumentClass();
}

export function getRenderMode(): RenderMode {
  return currentMode;
}

export function isOklchSupported(): boolean {
  return oklchSupported;
}

export function isSimpleModeActive(): boolean {
  return resolveSimpleMode(currentMode, oklchSupported);
}

export function setRenderMode(mode: RenderMode): void {
  if (mode === currentMode) return;
  currentMode = mode;
  try {
    localStorage.setItem(LS_RENDER_MODE, mode);
  } catch {
    /* ignore */
  }
  applyDocumentClass();
  emit();
}

function subscribe(listener: () => void): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

/** Reactive: the currently selected preference (auto/full/simple). */
export function useRenderModePref(): RenderMode {
  return useSyncExternalStore(subscribe, getRenderMode, getRenderMode);
}

/** Reactive: whether the compatibility UI is currently active. */
export function useSimpleMode(): boolean {
  return useSyncExternalStore(
    subscribe,
    isSimpleModeActive,
    isSimpleModeActive,
  );
}
