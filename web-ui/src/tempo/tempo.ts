import type { ControlDef } from "@/spec/controls";

/** Program parameters with musically meaningful time values. */
export const TEMPO_PARAMETERS = new Set([
  "reverb time",
  "predelay",
  "delay time",
]);

export function isTempoParameter(parameter: string | undefined): boolean {
  return parameter !== undefined && TEMPO_PARAMETERS.has(parameter);
}

export interface TempoDivision {
  name: string;
  ms: number;
}

export interface TimingDiscrepancy {
  fieldId: string;
  label: string;
  division: string;
  idealMs: number;
  actualMs: number;
  actualLabel: string;
  deltaMs: number;
}

/** Parse `500 ms`, `100 mSec`, `2.2 s`, or bare seconds for reverb time. */
export function parseTimeMs(label: string, parameter?: string): number | null {
  const trimmed = label.trim();
  const msMatch = trimmed.match(/^([\d.]+)\s*m\s*s(?:ec)?$/i);
  if (msMatch) return Number(msMatch[1]);
  const sMatch = trimmed.match(/^([\d.]+)\s*s$/i);
  if (sMatch) return Number(sMatch[1]) * 1000;
  if (parameter === "reverb time" && /^[\d.]+$/.test(trimmed)) {
    const seconds = Number(trimmed);
    if (Number.isFinite(seconds)) return seconds * 1000;
  }
  return null;
}

export function maxMsForParameter(parameter: string): number {
  if (parameter === "reverb time") return 30_000;
  return 1_000;
}

/** Min/max time supported by a control's value table. */
export function controlTimeRangeMs(
  control: ControlDef,
): { minMs: number; maxMs: number } | null {
  let minMs = Infinity;
  let maxMs = -Infinity;
  for (const entry of control.entries) {
    const ms = parseTimeMs(entry.label, control.parameter);
    if (ms === null) continue;
    minMs = Math.min(minMs, ms);
    maxMs = Math.max(maxMs, ms);
  }
  if (!Number.isFinite(minMs)) return null;
  return { minMs, maxMs };
}

export interface TempoStep {
  division: TempoDivision;
  encoded: number;
}

/**
 * Tempo divisions that map to distinct device values within this control's
 * time range — defines the knob scale in tempo mode.
 */
export function tempoStepsForControl(
  control: ControlDef,
  bpm: number,
): TempoStep[] {
  if (bpm <= 0 || !isTempoParameter(control.parameter)) return [];
  const range = controlTimeRangeMs(control);
  if (!range) return [];

  const divisions = tempoDivisions(bpm, range.maxMs).filter(
    (d) => d.ms >= range.minMs - 0.5 && d.ms <= range.maxMs + 0.5,
  );

  const seen = new Set<number>();
  const steps: TempoStep[] = [];
  for (const division of divisions) {
    const encoded = encodedForDivisionMs(control, division.ms);
    if (encoded === null || seen.has(encoded)) continue;
    seen.add(encoded);
    steps.push({ division, encoded });
  }
  return steps;
}

function straightMs(quarterMs: number, denom: number, mult = 1): number {
  return (quarterMs * 4 * mult) / denom;
}

function tripletMs(quarterMs: number, denom: number, mult = 1): number {
  return (straightMs(quarterMs, denom, mult) * 2) / 3;
}

function dottedMs(quarterMs: number, denom: number, mult = 1): number {
  return straightMs(quarterMs, denom, mult) * 1.5;
}

type DivisionModifier = "straight" | "triplet" | "dotted";

interface DivisionSpec {
  denom: number;
  mult?: number;
  modifier: DivisionModifier;
}

/**
 * Tempo-sync grid for predelay / delay / reverb time.
 *
 * Assumes 4/4 and a quarter-note pulse. Straight notes use denominators down to
 * 1/32; triplets and dots apply only at musically common subdivisions (no whole-
 * note triplet or dotted whole). Bar multiples are straight only.
 */
export const MUSICAL_DIVISION_SPECS: readonly DivisionSpec[] = [
  { denom: 32, modifier: "straight" },
  { denom: 16, modifier: "triplet" },
  { denom: 16, modifier: "straight" },
  { denom: 16, modifier: "dotted" },
  { denom: 8, modifier: "triplet" },
  { denom: 8, modifier: "straight" },
  { denom: 8, modifier: "dotted" },
  { denom: 4, modifier: "triplet" },
  { denom: 4, modifier: "straight" },
  { denom: 4, modifier: "dotted" },
  { denom: 2, modifier: "triplet" },
  { denom: 2, modifier: "straight" },
  { denom: 2, modifier: "dotted" },
  { denom: 1, modifier: "straight" },
  { denom: 1, mult: 2, modifier: "straight" },
  { denom: 1, mult: 4, modifier: "straight" },
  { denom: 1, mult: 8, modifier: "straight" },
  { denom: 1, mult: 16, modifier: "straight" },
  { denom: 1, mult: 32, modifier: "straight" },
];

function divisionMs(
  quarterMs: number,
  denom: number,
  modifier: DivisionModifier,
  mult = 1,
): number {
  switch (modifier) {
    case "straight":
      return straightMs(quarterMs, denom, mult);
    case "triplet":
      return tripletMs(quarterMs, denom, mult);
    case "dotted":
      return dottedMs(quarterMs, denom, mult);
  }
}

function divisionName(
  denom: number,
  mult: number,
  modifier: DivisionModifier = "straight",
): string {
  const suffix = modifier === "triplet" ? "T" : modifier === "dotted" ? "D" : "";
  return `${mult}/${denom}${suffix}`;
}

/** Display whole bars as `1`, `2`, … and whole note as `1`. */
export function formatDivisionLabel(name: string): string {
  const barMatch = normalizeDivisionName(name).match(/^(\d+)\/1$/);
  if (barMatch) return barMatch[1];
  return name;
}

/** Accept `1`, `2`, … as bar counts and `1` as alias for whole note `1/1`. */
export function normalizeDivisionName(name: string): string {
  const trimmed = name.trim();
  if (/^\d+$/.test(trimmed)) return `${trimmed}/1`;
  return trimmed;
}

/** Build snap/display candidates up to `maxMs` (default 30 s). */
export function tempoDivisions(
  bpm: number,
  maxMs = 30_000,
): TempoDivision[] {
  if (bpm <= 0) return [];
  const quarterMs = 60_000 / bpm;

  const out: TempoDivision[] = [];
  for (const spec of MUSICAL_DIVISION_SPECS) {
    const mult = spec.mult ?? 1;
    const ms = divisionMs(quarterMs, spec.denom, spec.modifier, mult);
    if (ms <= 0 || ms > maxMs + 0.5) continue;
    out.push({
      name: divisionName(spec.denom, mult, spec.modifier),
      ms,
    });
  }

  return out.sort((a, b) => a.ms - b.ms);
}

export function nearestTempoDivision(
  ms: number,
  bpm: number,
  maxMs = 30_000,
): TempoDivision | null {
  const divisions = tempoDivisions(bpm, maxMs);
  if (!divisions.length) return null;
  let best = divisions[0];
  let bestDist = Math.abs(ms - best.ms);
  for (const div of divisions) {
    const dist = Math.abs(ms - div.ms);
    if (dist < bestDist) {
      best = div;
      bestDist = dist;
    }
  }
  return best;
}

export function entryTimeMs(control: ControlDef, encoded: number): number | null {
  const entry = control.entries.find((e) => e.encoded === encoded);
  if (!entry) return null;
  return parseTimeMs(entry.label, control.parameter);
}

export function encodedForDivisionMs(
  control: ControlDef,
  targetMs: number,
): number | null {
  let bestEncoded: number | null = null;
  let bestDist = Infinity;
  for (const entry of control.entries) {
    const ms = parseTimeMs(entry.label, control.parameter);
    if (ms === null) continue;
    const dist = Math.abs(ms - targetMs);
    if (dist < bestDist) {
      bestDist = dist;
      bestEncoded = entry.encoded;
    }
  }
  return bestEncoded;
}

export function tempoStepIndexForEncoded(
  control: ControlDef,
  encoded: number,
  bpm: number,
): number {
  const steps = tempoStepsForControl(control, bpm);
  if (!steps.length) return 0;

  const direct = steps.findIndex((s) => s.encoded === encoded);
  if (direct >= 0) return direct;

  const ms = entryTimeMs(control, encoded);
  if (ms === null) return 0;

  let best = 0;
  let bestDist = Infinity;
  for (let i = 0; i < steps.length; i++) {
    const dist = Math.abs(ms - steps[i].division.ms);
    if (dist < bestDist) {
      bestDist = dist;
      best = i;
    }
  }
  return best;
}

/** @deprecated Use tempoStepIndexForEncoded */
export function divisionIndexForEncoded(
  control: ControlDef,
  encoded: number,
  bpm: number,
): number {
  return tempoStepIndexForEncoded(control, encoded, bpm);
}

export function snapControlToTempo(
  control: ControlDef,
  encoded: number,
  bpm: number,
): number {
  if (bpm <= 0 || !isTempoParameter(control.parameter)) return encoded;

  const currentMs = entryTimeMs(control, encoded);
  if (currentMs === null) return encoded;

  const range = controlTimeRangeMs(control);
  const maxMs = range?.maxMs ?? maxMsForParameter(control.parameter ?? "");
  const target = nearestTempoDivision(currentMs, bpm, maxMs);
  if (!target) return encoded;

  const snapped = encodedForDivisionMs(control, target.ms);
  return snapped ?? encoded;
}

export function formatControlTempoValue(
  control: ControlDef,
  encoded: number,
  bpm: number,
): string | null {
  if (bpm <= 0 || !isTempoParameter(control.parameter)) return null;
  const ms = entryTimeMs(control, encoded);
  if (ms === null) return null;
  const range = controlTimeRangeMs(control);
  const maxMs = range?.maxMs ?? maxMsForParameter(control.parameter ?? "");
  const div = nearestTempoDivision(ms, bpm, maxMs);
  return div ? formatDivisionLabel(div.name) : null;
}

/** Step by adjacent tempo divisions when tempo mode is active. */
export function stepControlTempoEncoded(
  control: ControlDef,
  encoded: number,
  delta: number,
  bpm: number,
): number | null {
  if (bpm <= 0 || !isTempoParameter(control.parameter)) return null;

  const steps = tempoStepsForControl(control, bpm);
  if (!steps.length) return null;

  const idx = tempoStepIndexForEncoded(control, encoded, bpm);
  const nextIdx = idx + delta;
  if (nextIdx < 0 || nextIdx >= steps.length) return null;

  const snapped = steps[nextIdx].encoded;
  return snapped === encoded ? null : snapped;
}

export function computeTimingDiscrepancies(
  controls: Iterable<ControlDef>,
  encoded: Record<string, number>,
  bpm: number,
  tempoModeFields: ReadonlySet<string>,
): TimingDiscrepancy[] {
  if (bpm <= 0) return [];
  const out: TimingDiscrepancy[] = [];

  for (const control of controls) {
    if (!tempoModeFields.has(control.fieldId)) continue;
    if (!isTempoParameter(control.parameter)) continue;

    const enc = encoded[control.fieldId];
    if (enc === undefined) continue;

    const actualMs = entryTimeMs(control, enc);
    if (actualMs === null) continue;

    const range = controlTimeRangeMs(control);
    const maxMs = range?.maxMs ?? maxMsForParameter(control.parameter ?? "");
    const div = nearestTempoDivision(actualMs, bpm, maxMs);
    if (!div) continue;

    const deltaMs = actualMs - div.ms;
    if (Math.abs(deltaMs) < 0.05) continue;

    const entry = control.entries.find((e) => e.encoded === enc);
    out.push({
      fieldId: control.fieldId,
      label: control.label,
      division: formatDivisionLabel(div.name),
      idealMs: div.ms,
      actualMs,
      actualLabel: entry?.label ?? String(enc),
      deltaMs,
    });
  }

  return out;
}
