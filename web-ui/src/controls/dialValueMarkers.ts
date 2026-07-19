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

/** Relative difference between adjacent step deltas that counts as a change. */
const DELTA_REL_TOLERANCE = 0.05;

/** Safety cap so labels stay readable around a dial. */
const DEFAULT_MAX_MARKERS = 8;

function deltaChanges(a: number, b: number): boolean {
  return (
    Math.abs(b - a) >
    Math.max(Math.abs(a), Math.abs(b)) * DELTA_REL_TOLERANCE + 1e-9
  );
}

/**
 * Indices where a new step size begins (e.g. reverb time switching from
 * 0.05 s to 0.1 s steps). The returned index is the shared junction entry.
 */
export function incrementBreakpoints(values: number[]): number[] {
  const out: number[] = [];
  for (let i = 1; i < values.length - 1; i++) {
    const prev = values[i]! - values[i - 1]!;
    const next = values[i + 1]! - values[i]!;
    if (deltaChanges(prev, next)) out.push(i);
  }
  return out;
}

/** True when consecutive numeric steps do not share a near-constant gap. */
export function hasUnevenNumericGaps(values: number[]): boolean {
  if (values.length < 3) return false;
  return incrementBreakpoints(values).length > 0;
}

/** Drop a redundant “.0” on whole numbers for compact dial ring text. */
function compactMarkerNumber(s: string): string {
  const n = Number(s);
  if (!Number.isFinite(n)) return s;
  if (Math.abs(n - Math.round(n)) < 1e-9) return String(Math.round(n));
  return s;
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
  if (/^-?[\d.]+$/.test(trimmed)) return compactMarkerNumber(trimmed);

  const formatted = formatValueLabel(label, parameter);
  const withUnit = formatted.match(/^(-?[\d.]+)\s*(.*)$/i);
  if (!withUnit) return formatted;
  const num = compactMarkerNumber(withUnit[1]!);
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

/**
 * Marker entry indices for a dial with uniform increments:
 * extremes plus the perfect middle when one exists (odd entry count),
 * otherwise 4 labels spaced equally around the arc.
 */
function uniformMarkerIndices(count: number): number[] {
  const last = count - 1;
  if (last < 1) return [];
  if (count % 2 === 1) return [0, last / 2, last];
  const indices = [0, Math.round(last / 3), Math.round((2 * last) / 3), last];
  return [...new Set(indices)];
}

interface MarkerEntry {
  index: number;
  value: number | null;
  label: string;
}

function markerEntries(control: ControlDef, labels: string[]): MarkerEntry[] {
  return labels.map((raw, index) => {
    const value = parseEntryNumeric(raw, control.parameter);
    return {
      index,
      value: value !== null && Number.isFinite(value) ? value : null,
      label: formatDialMarkerLabel(raw, control.parameter),
    };
  });
}

/**
 * Contiguous numeric run in the middle of the table, skipping non-numeric
 * endpoints like `off`, `Small`, or `Full`. Null when the numeric values are
 * not one contiguous run.
 */
function numericCore(
  entries: MarkerEntry[],
): { start: number; values: number[] } | null {
  let start = 0;
  while (start < entries.length && entries[start]!.value === null) start++;
  let end = entries.length - 1;
  while (end >= 0 && entries[end]!.value === null) end--;
  if (start > end) return null;
  const values: number[] = [];
  for (let i = start; i <= end; i++) {
    const v = entries[i]!.value;
    if (v === null) return null;
    values.push(v);
  }
  return { start, values };
}

/**
 * Min / mid / max markers from a plain ordered label list (e.g. tempo
 * divisions), or 4 equally spaced labels when there is no perfect middle.
 */
export function dialUniformMarkers(
  labels: string[],
): Pick<DialValueMarker, "pct" | "label">[] {
  if (labels.length < 2) return [];
  const last = labels.length - 1;
  return uniformMarkerIndices(labels.length).map((i) => ({
    pct: i / last,
    label: labels[i]!,
  }));
}

/**
 * Labeled dial markers:
 * - extremes are always labeled;
 * - uniform-increment dials get the perfect middle when one exists,
 *   otherwise 4 equally spaced labels;
 * - changing-increment dials get a label at each step-size breakpoint.
 */
export function dialValueMarkersForControl(
  control: ControlDef,
  options?: {
    labels?: string[];
    maxMarkers?: number;
  },
): DialValueMarker[] {
  const labels = options?.labels ?? control.entries.map((e) => e.label);
  if (labels.length < 2) return [];

  const maxMarkers = Math.max(2, options?.maxMarkers ?? DEFAULT_MAX_MARKERS);
  const entries = markerEntries(control, labels);
  const last = entries.length - 1;
  const core = numericCore(entries);
  const breakpoints =
    core && core.values.length >= 3 ? incrementBreakpoints(core.values) : [];

  let indices: number[];
  if (breakpoints.length > 0) {
    const interior = breakpoints
      .map((i) => i + core!.start)
      .filter((i) => i !== 0 && i !== last);
    indices = [0, ...interior, last];
  } else {
    indices = uniformMarkerIndices(entries.length);
  }

  if (indices.length > maxMarkers) {
    const interior = indices.slice(1, -1);
    const keep = maxMarkers - 2;
    const sampled = new Set<number>();
    for (let k = 0; k < keep; k++) {
      const t = keep === 1 ? 0.5 : k / (keep - 1);
      sampled.add(interior[Math.round(t * (interior.length - 1))]!);
    }
    indices = [0, ...sampled, last];
  }

  return indices.map((index) => ({
    index,
    pct: index / last,
    label: entries[index]!.label,
  }));
}
