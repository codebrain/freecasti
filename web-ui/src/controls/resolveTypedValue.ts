import type { ControlDef } from "@/spec/controls";
import { formatEarlyLateMixLabel, formatValueLabel, isMultiplyParameter } from "@/spec/labels";
import {
  encodedForDivisionMs,
  formatDivisionLabel,
  isTempoParameter,
  normalizeDivisionName,
  parseTimeMs,
  tempoStepsForControl,
} from "@/tempo/tempo";

function normalizeText(text: string): string {
  return text.trim().toLowerCase().replace(/\s+/g, " ");
}

const DB_PARAMETERS = new Set([
  "wet gain",
  "dry gain",
  "delay level",
  "vlf cut",
  "output level",
]);

const MS_PARAMETERS = new Set(["predelay", "delay time"]);

const HZ_PARAMETERS = new Set([
  "rolloff",
  "early rolloff",
  "hf rt crossover",
  "lf rt crossover",
]);

/**
 * Map a unitless numeric entry into the same comparison space as table labels.
 * Positive dB magnitudes are treated as attenuation (e.g. `45` → −45 dB).
 */
export function normalizeBareNumeric(value: number, parameter?: string): number {
  if (parameter === "reverb time") {
    // Bare values ≥ 30 are milliseconds; smaller values are seconds.
    return value >= 30 ? value : value * 1000;
  }
  if (parameter && MS_PARAMETERS.has(parameter)) {
    return value;
  }
  if (parameter && HZ_PARAMETERS.has(parameter)) {
    return value;
  }
  if (parameter && DB_PARAMETERS.has(parameter) && value > 0) {
    return -value;
  }
  return value;
}

/** Parse a user-typed value into a number comparable to table labels. */
export function parseNumericFromUserInput(
  text: string,
  parameter?: string,
): number | null {
  const trimmed = text.trim().toLowerCase();
  if (!trimmed) return null;

  const dbMatch = trimmed.match(/^(-?[\d.]+)\s*db$/i);
  if (dbMatch) return Number(dbMatch[1]);

  const hzMatch = trimmed.match(/^(-?[\d.]+)\s*hz$/i);
  if (hzMatch) return Number(hzMatch[1]);

  const xMatch = trimmed.match(/^(-?[\d.]+)\s*x$/i);
  if (xMatch) return Number(xMatch[1]);

  if (/\d\s*m\s*s(?:ec)?$/i.test(trimmed) || /\d\s*s$/i.test(trimmed)) {
    const ms = parseTimeMs(trimmed, parameter);
    if (ms !== null) return ms;
  }

  if (/^-?[\d.]+$/.test(trimmed)) {
    const n = Number(trimmed);
    if (!Number.isFinite(n)) return null;
    return normalizeBareNumeric(n, parameter);
  }

  return null;
}

/** Parse a spec table label into a number for nearest-neighbor matching. */
export function parseEntryNumeric(
  label: string,
  parameter?: string,
): number | null {
  const ms = parseTimeMs(label, parameter);
  if (ms !== null) return ms;

  const trimmed = label.trim().toLowerCase();
  const dbMatch = trimmed.match(/^(-?[\d.]+)\s*db$/);
  if (dbMatch) return Number(dbMatch[1]);

  const hzMatch = trimmed.match(/^(-?[\d.]+)\s*hz$/);
  if (hzMatch) return Number(hzMatch[1]);

  if (isMultiplyParameter(parameter) && /^[\d.]+$/.test(trimmed)) {
    return Number(trimmed);
  }

  if (/^-?[\d.]+$/.test(trimmed)) return Number(trimmed);

  return null;
}

function entriesFor(control: ControlDef) {
  return control.buttonEntries ?? control.entries;
}

function matchLabelEntry(
  entries: ControlDef["entries"],
  text: string,
  parameter?: string,
): number | null {
  const inputNorm = normalizeText(text);
  for (const entry of entries) {
    if (normalizeText(entry.label) === inputNorm) return entry.encoded;
    if (normalizeText(formatValueLabel(entry.label, parameter)) === inputNorm) {
      return entry.encoded;
    }
  }
  return null;
}

/**
 * Resolve typed text to an encoded table value.
 * Returns null when the input is empty or cannot be matched safely.
 */
export function resolveTypedControlValue(
  control: ControlDef,
  draft: string,
  options?: {
    tempoBpm?: number;
    tempoActive?: boolean;
  },
): number | null {
  const text = draft.trim();
  if (!text) return null;

  const entries = entriesFor(control);
  const parameter = control.parameter;

  const labelMatch = matchLabelEntry(entries, text, parameter);
  if (labelMatch !== null) return labelMatch;

  if (parameter === "early to reverb mix") {
    const inputNorm = normalizeText(text);
    for (const entry of entries) {
      const display = formatEarlyLateMixLabel(entry.label);
      if (display && normalizeText(display) === inputNorm) return entry.encoded;
    }
    const slash = text.match(/^(\d+)\s*\/\s*(\d+)$/);
    if (slash) {
      const target = `${slash[1]}/${slash[2]}`;
      const mix = entries.find((e) => e.label === target);
      if (mix) return mix.encoded;
    }
  }

  if (
    options?.tempoActive &&
    options.tempoBpm &&
    options.tempoBpm > 0 &&
    isTempoParameter(parameter)
  ) {
    const normalized = normalizeDivisionName(text);
    const steps = tempoStepsForControl(control, options.tempoBpm);
    for (const step of steps) {
      const names = [
        step.division.name,
        normalizeDivisionName(step.division.name),
        formatDivisionLabel(step.division.name),
      ];
      if (names.some((name) => normalizeText(name) === normalizeText(normalized))) {
        return step.encoded;
      }
    }

    const msFromBare =
      parseTimeMs(text, parameter) ?? parseNumericFromUserInput(text, parameter);
    if (msFromBare !== null) {
      const enc = encodedForDivisionMs(control, msFromBare);
      if (enc !== null) return enc;
    }
  }

  const inputNum = parseNumericFromUserInput(text, parameter);
  if (inputNum === null) return null;

  let bestEncoded: number | null = null;
  let bestDist = Infinity;
  for (const entry of entries) {
    const entryNum = parseEntryNumeric(entry.label, parameter);
    if (entryNum === null) continue;
    const dist = Math.abs(entryNum - inputNum);
    if (dist < bestDist) {
      bestDist = dist;
      bestEncoded = entry.encoded;
    }
  }

  return bestEncoded;
}
