import { PROG_PARAM_ORDER } from "@/spec/param-order";
import { DEFAULT_ALGORITHM_CONSTRAINTS } from "./algorithms";
import type { AlgorithmConstraints, PresetCatalog, PresetEntry } from "./types";

/** On-wire preset catalog (minimal columns). */
export interface CompactPresetCatalog {
  banks: string[];
  params: string[];
  presets: CompactPresetRow[];
  algorithms?: AlgorithmConstraints;
}

/** [bank_index, program_slot, name, ...encoded params in `params` order] */
export type CompactPresetRow = [number, number, string, ...number[]];

export function isCompactPresetCatalog(data: unknown): data is CompactPresetCatalog {
  return (
    typeof data === "object" &&
    data !== null &&
    Array.isArray((data as CompactPresetCatalog).banks) &&
    Array.isArray((data as CompactPresetCatalog).presets)
  );
}

export function expandPresetCatalog(raw: CompactPresetCatalog): PresetCatalog {
  const params = raw.params.length ? raw.params : [...PROG_PARAM_ORDER];
  const presets: PresetEntry[] = raw.presets.map((row) => {
    const [bankIndex, programSlot, name, ...encValues] = row;
    const parameters: Record<string, number> = {};
    params.forEach((param, i) => {
      parameters[param] = encValues[i];
    });
    return {
      bank: raw.banks[bankIndex] ?? `bank ${bankIndex}`,
      preset: name,
      name_field: name,
      bank_index: bankIndex,
      program_slot: programSlot,
      parameters,
    };
  });
  return {
    generated: "",
    dump_count: presets.length,
    presets,
    algorithms: raw.algorithms ?? DEFAULT_ALGORITHM_CONSTRAINTS,
  };
}
