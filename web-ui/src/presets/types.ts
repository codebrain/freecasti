export interface PresetEntry {
  bank: string;
  preset: string;
  name_field: string;
  bank_index: number;
  program_slot: number;
  /** Parameter name → encoded integer (slim runtime catalog). */
  parameters: Record<string, number>;
}

export interface AlgorithmConstraint {
  bank_index: number;
  params: string[];
}

export type AlgorithmConstraints = Record<string, AlgorithmConstraint>;

export interface PresetCatalog {
  generated: string;
  dump_count: number;
  presets: PresetEntry[];
  algorithms?: AlgorithmConstraints;
}

export interface BankInfo {
  name: string;
  /** UI label; a "v1"/"v2" suffix is added only for algorithms with both versions. */
  displayName: string;
  bankIndex: number;
  presets: PresetEntry[];
}
