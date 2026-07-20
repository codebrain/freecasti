import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { expandPresetCatalog, type CompactPresetRow } from "@/presets/compact";
import { groupPresetsByBank } from "@/presets/catalog";
import { buildParameterToFieldId } from "@/spec/controls";
import { PROG_PARAM_ORDER } from "@/spec/param-order";
import type { DumpSpec } from "@/spec/types";

export const repoRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

export interface FullPresetDump {
  presets: Array<{
    bank: string;
    preset: string;
    name_field: string;
    bank_index: number;
    program_slot: number;
    parameters: Record<string, { encoded: number }>;
  }>;
}

export function compactFromFull(presetsFull: FullPresetDump) {
  const byIndex: Record<number, string> = {};
  for (const entry of presetsFull.presets) {
    byIndex[entry.bank_index] = entry.bank;
  }
  const banks = Object.keys(byIndex)
    .map(Number)
    .sort((a, b) => a - b)
    .map((i) => byIndex[i]);
  const presets = presetsFull.presets.map(
    (entry): CompactPresetRow => [
      entry.bank_index,
      entry.program_slot,
      entry.name_field,
      ...PROG_PARAM_ORDER.map((name) => entry.parameters[name].encoded),
    ],
  );
  return expandPresetCatalog({
    banks,
    params: [...PROG_PARAM_ORDER],
    presets,
  });
}

export function loadProgSpec(): DumpSpec {
  return JSON.parse(
    fs.readFileSync(
      path.join(repoRoot, "specification/prog/m7_program_dump.spec.json"),
      "utf8",
    ),
  );
}

export function loadPresetCatalogFixture() {
  const presetsFull: FullPresetDump = JSON.parse(
    fs.readFileSync(
      path.join(repoRoot, "specification/prog/presets/presets.json"),
      "utf8",
    ),
  );
  const spec = loadProgSpec();
  const catalog = compactFromFull(presetsFull);
  return {
    presetsFull,
    spec,
    catalog,
    banks: groupPresetsByBank(catalog),
    paramMap: buildParameterToFieldId(spec),
  };
}
