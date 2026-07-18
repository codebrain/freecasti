import { expandPresetCatalog, isCompactPresetCatalog } from "@/presets/compact";
import type { PresetCatalog } from "@/presets/types";
import type { ProgUiRuntime } from "@/prog/uiState";
import { expandCompactSpec, isCompactSpec } from "@/spec/compact";
import type { DumpSpec } from "@/spec/types";

export interface RuntimeBundle {
  prog: DumpSpec;
  system: DumpSpec;
  presets: PresetCatalog;
  templates: {
    prog: Uint8Array;
    system: Uint8Array;
  };
  progUi: ProgUiRuntime | null;
}

export function expandSpec(raw: unknown): DumpSpec {
  if (isCompactSpec(raw)) return expandCompactSpec(raw);
  return raw as DumpSpec;
}

export function expandPresets(raw: unknown): PresetCatalog {
  if (isCompactPresetCatalog(raw)) return expandPresetCatalog(raw);
  return raw as PresetCatalog;
}

export function decodeBase64Template(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) {
    out[i] = bin.charCodeAt(i);
  }
  return out;
}

export function expandRuntimeBundle(raw: {
  prog: unknown;
  system: unknown;
  presets: unknown;
  tpl: { p: string; s: string };
  prog_ui?: unknown;
}): RuntimeBundle {
  return {
    prog: expandSpec(raw.prog),
    system: expandSpec(raw.system),
    presets: expandPresets(raw.presets),
    templates: {
      prog: decodeBase64Template(raw.tpl.p),
      system: decodeBase64Template(raw.tpl.s),
    },
    progUi: (raw.prog_ui as ProgUiRuntime | undefined) ?? null,
  };
}
