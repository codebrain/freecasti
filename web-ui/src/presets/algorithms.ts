import type { AlgorithmConstraints, PresetCatalog } from "./types";

/** Fallback when loading an older presets.json without `algorithms`. */
export const DEFAULT_ALGORITHM_CONSTRAINTS: AlgorithmConstraints = {
  nonlin: {
    bank_index: 10,
    params: [
      "size",
      "predelay",
      "rolloff",
      "early select",
      "early to reverb mix",
      "early rolloff",
    ],
  },
};

export function algorithmConstraintsFrom(
  catalog: Pick<PresetCatalog, "algorithms"> | null | undefined,
): AlgorithmConstraints {
  const fromCatalog = catalog?.algorithms?.nonlin;
  if (!fromCatalog?.params?.length) {
    return DEFAULT_ALGORITHM_CONSTRAINTS;
  }
  return {
    nonlin: {
      bank_index:
        typeof fromCatalog.bank_index === "number"
          ? fromCatalog.bank_index
          : DEFAULT_ALGORITHM_CONSTRAINTS.nonlin.bank_index,
      params: fromCatalog.params,
    },
  };
}

export function nonlinActiveParams(
  constraints: AlgorithmConstraints = DEFAULT_ALGORITHM_CONSTRAINTS,
): ReadonlySet<string> {
  return new Set(constraints.nonlin?.params ?? DEFAULT_ALGORITHM_CONSTRAINTS.nonlin.params);
}

export function isNonLinBank(
  bankIndex: number,
  constraints: AlgorithmConstraints = DEFAULT_ALGORITHM_CONSTRAINTS,
): boolean {
  const nonlinIndex =
    constraints.nonlin?.bank_index ?? DEFAULT_ALGORITHM_CONSTRAINTS.nonlin.bank_index;
  return bankIndex === nonlinIndex;
}

export function isParameterActive(
  bankIndex: number,
  parameter: string | undefined,
  constraints: AlgorithmConstraints = DEFAULT_ALGORITHM_CONSTRAINTS,
): boolean {
  if (!parameter) return true;
  if (!isNonLinBank(bankIndex)) return true;
  return nonlinActiveParams(constraints).has(parameter);
}
