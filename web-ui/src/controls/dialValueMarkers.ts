import type { ControlDef } from "@/spec/controls";
import { formatValueLabel } from "@/spec/labels";
import { parseEntryNumeric } from "@/controls/resolveTypedValue";

export interface DialValueMarker {
  /** 0–1 position along the dial arc (matches index-based knob scale). */
  pct: number;
  /** Short label drawn beside the dial. */
  label: string;
  /** Entry index this marker snaps to. */
  index: number;
}

/** Relative spread of consecutive step deltas that counts as uneven. */
const UNEVEN_CV_THRESHOLD = 0.12;

/** Soft cap so labels stay readable around a dial. */
const DEFAULT_MAX_MARKERS = 7;

function consecutiveDeltas(values: number[]): number[] {
  const deltas: number[] = [];
  for (let i = 1; i < values.length; i++) {
    deltas.push(Math.abs(values[i]! - values[i - 1]!));
  }
  return deltas;
}

/** True when consecutive numeric steps do not share a near-constant gap. */
export function hasUnevenNumericGaps(values: number[]): boolean {
  if (values.length < 4) return false;
  const deltas = consecutiveDeltas(values).filter((d) => d > 0);
  if (deltas.length < 3) return false;
  const mean = deltas.reduce((a, b) => a + b, 0) / deltas.length;
  if (!(mean > 0)) return false;
  const variance =
    deltas.reduce((a, d) => a + (d - mean) ** 2, 0) / deltas.length;
  return Math.sqrt(variance) / mean > UNEVEN_CV_THRESHOLD;
}

/**
 * Unitless ring text from a table label (e.g. `500 ms` → `500`, `2.2 s` → `2.2`).
 * Large Hz values compact to `k` (e.g. `4800 Hz` → `4.8k`).
 */
export function formatDialMarkerLabel(
  label: string,
  parameter?: string,
): string {
  const trimmed = label.trim();
  // Prefer the raw table number when it is already unitless (reverb time, multiply).
  if (/^-?[\d.]+$/.test(trimmed)) return trimmed;

  const formatted = formatValueLabel(label, parameter);
  const withUnit = formatted.match(/^(-?[\d.]+)\s*(.*)$/i);
  if (!withUnit) return formatted;
  const num = withUnit[1]!;
  const unit = (withUnit[2] ?? "").trim().toLowerCase();
  if (!unit || unit === "x") return num;
  if (unit === "hz") {
    const n = Number(num);
    if (n >= 1000) return `${Number((n / 1000).toFixed(1))}k`;
    return num;
  }
  // ms, s, dB, etc. — number only
  return num;
}

interface MarkerEntry {
  index: number;
  value: number | null;
  label: string;
}

function markerEntries(
  control: ControlDef,
  labels: string[],
): MarkerEntry[] {
  return labels.map((raw, index) => {
    const value = parseEntryNumeric(raw, control.parameter);
    return {
      index,
      value: value !== null && Number.isFinite(value) ? value : null,
      label: formatDialMarkerLabel(raw, control.parameter),
    };
  });
}

/** True when `value` is a “round” landmark on a typical audio dial. */
function isLandmarkValue(value: number): boolean {
  const abs = Math.abs(value);
  if (abs === 0) return true;
  // Powers of 10 and simple multiples (1, 2, 5 × 10^n).
  const exp = Math.floor(Math.log10(abs));
  const scale = 10 ** exp;
  const norm = abs / scale;
  for (const target of [1, 2, 2.5, 5, 10]) {
    if (Math.abs(norm - target) < 1e-6) return true;
  }
  // Half-units for small scales (0.5, 1.5, …) when magnitude < 10.
  if (abs < 10 && Math.abs(abs * 2 - Math.round(abs * 2)) < 1e-6) return true;
  return false;
}

function minIndexDistance(index: number, chosen: MarkerEntry[]): number {
  if (chosen.length === 0) return Infinity;
  return Math.min(...chosen.map((c) => Math.abs(c.index - index)));
}

function toMarkers(
  chosen: MarkerEntry[],
  labelCount: number,
): DialValueMarker[] {
  const denom = Math.max(1, labelCount - 1);
  return chosen.map((e) => ({
    index: e.index,
    pct: e.index / denom,
    label: e.label,
  }));
}

/**
 * Min/max ring markers from an ordered label list (e.g. tempo divisions).
 */
export function dialExtremeMarkers(
  labels: string[],
): Pick<DialValueMarker, "pct" | "label">[] {
  if (labels.length < 2) return [];
  return [
    { pct: 0, label: labels[0]! },
    { pct: 1, label: labels[labels.length - 1]! },
  ];
}

/**
 * Labeled dial markers. Every multi-step dial gets min/max extremes; uneven
 * numeric tables also get intermediate landmarks.
 */
export function dialValueMarkersForControl(
  control: ControlDef,
  options?: {
    labels?: string[];
    maxMarkers?: number;
  },
): DialValueMarker[] {
  const labels =
    options?.labels ?? control.entries.map((e) => e.label);
  if (labels.length < 2) return [];

  const maxMarkers = options?.maxMarkers ?? DEFAULT_MAX_MARKERS;
  const entries = markerEntries(control, labels);
  const first = entries[0]!;
  const last = entries[entries.length - 1]!;

  const numericValues = entries
    .map((e) => e.value)
    .filter((v): v is number => v !== null);
  const uneven =
    numericValues.length >= 4 &&
    numericValues.length === entries.length &&
    hasUnevenNumericGaps(numericValues);

  if (!uneven) {
    // Even / short / non-numeric: extremes only.
    return toMarkers([first, last], labels.length);
  }

  const chosen: MarkerEntry[] = [first];
  const landmarks = entries.filter(
    (e) =>
      e.index !== first.index &&
      e.index !== last.index &&
      e.value !== null &&
      isLandmarkValue(e.value),
  );

  // Prefer landmarks that stay readable around the arc. Use a looser
  // separation for landmarks than for filler ticks so round values (1, 10, …)
  // win over nearby non-landmarks.
  const landmarkSep = Math.max(
    1,
    Math.floor((labels.length - 1) / (maxMarkers * 2)),
  );
  const fillSep = Math.max(
    1,
    Math.floor((labels.length - 1) / (maxMarkers + 1)),
  );
  for (const candidate of landmarks) {
    if (chosen.length >= maxMarkers - 1) break;
    if (minIndexDistance(candidate.index, chosen) < landmarkSep) continue;
    if (Math.abs(candidate.index - last.index) < landmarkSep) continue;
    chosen.push(candidate);
  }

  // Fill remaining slots with index-even samples snapped to nearest entry.
  while (chosen.length < maxMarkers - 1) {
    let best: MarkerEntry | null = null;
    let bestScore = -1;
    for (const candidate of entries) {
      if (candidate.index === last.index) continue;
      if (chosen.some((c) => c.index === candidate.index)) continue;
      const dist = minIndexDistance(candidate.index, [...chosen, last]);
      if (dist <= bestScore) continue;
      bestScore = dist;
      best = candidate;
    }
    if (!best || bestScore < fillSep * 0.5) break;
    chosen.push(best);
  }

  chosen.push(last);
  chosen.sort((a, b) => a.index - b.index);
  return toMarkers(chosen, labels.length);
}
