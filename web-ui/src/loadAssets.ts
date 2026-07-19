import type { RuntimeBundle } from "@/runtime/expandRuntime";
import { expandRuntimeBundle } from "@/runtime/expandRuntime";

export type { RuntimeBundle } from "@/runtime/expandRuntime";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`fetch ${path}: ${res.status}`);
  return res.json() as Promise<T>;
}

let runtimePromise: Promise<RuntimeBundle> | null = null;

/** Load compact prog/system specs, preset catalog, and SysEx skeleton templates. */
export async function loadRuntime(): Promise<RuntimeBundle> {
  if (!runtimePromise) {
    runtimePromise = fetchJson<{
      prog: unknown;
      system: unknown;
      presets: unknown;
      tpl: { p: string; s: string };
    }>(`${import.meta.env.BASE_URL}m7-runtime.json`).then(expandRuntimeBundle);
  }
  return runtimePromise;
}
