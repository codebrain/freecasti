/** UI overrides for parameter names (spec names unchanged on wire). */
const PARAMETER_DISPLAY_LABELS: Record<string, string> = {
  "early to reverb mix": "Early/Late",
  modulation: "MOD",
  "audio routing": "Routing",
  "audio format": "Format",
  "display level": "Display",
  "midi channel": "Channel",
  "midi bank": "MIDI Bank",
  "wet gain": "Wet Gain",
  "dry gain": "Dry Gain",
  "output level": "Output Level",
};

/** RT multiply knobs store unitless factors in the spec (e.g. `0.5`, `1.0`). */
export const MULTIPLY_PARAMETERS = new Set([
  "lf rt multiply",
  "hf rt multiply",
]);

export function isMultiplyParameter(parameter: string | undefined): boolean {
  return parameter !== undefined && MULTIPLY_PARAMETERS.has(parameter);
}

const EARLY_LATE_MIX_PARAMETER = "early to reverb mix";
const EARLY_LATE_SIDE_MAX = 20;

/** `A/B` mix labels (each side 0–20) → `early% / late%` (sums to 100%). */
export function formatEarlyLateMixLabel(label: string): string | null {
  const match = label.trim().match(/^(\d+)\/(\d+)$/);
  if (!match) return null;
  const early = Number(match[1]);
  const late = Number(match[2]);
  if (!Number.isFinite(early) || !Number.isFinite(late)) return null;
  if (early > EARLY_LATE_SIDE_MAX || late > EARLY_LATE_SIDE_MAX) return null;
  const total = early + late;
  if (total <= 0) return "0% / 0%";
  const earlyPct = Math.round((early / total) * 100);
  const latePct = Math.round((late / total) * 100);
  return `${earlyPct}% / ${latePct}%`;
}

/** Convert spec labels like `0.5 s` to `500 ms` for display. */
function formatSubSecondTimeLabel(label: string): string | null {
  const secMatch = label.match(/^([\d.]+)\s*s$/i);
  if (!secMatch) return null;
  const seconds = Number(secMatch[1]);
  if (!Number.isFinite(seconds) || seconds >= 1) return null;
  return `${Math.round(seconds * 1000)} ms`;
}

/** Reverb time table stores bare seconds (e.g. `2.2`); show ms/s like other times. */
function formatBareReverbSecondsLabel(
  label: string,
  parameter?: string,
): string | null {
  if (parameter !== "reverb time") return null;
  const trimmed = label.trim();
  if (!/^[\d.]+$/.test(trimmed)) return null;
  const seconds = Number(trimmed);
  if (!Number.isFinite(seconds)) return null;
  if (seconds < 1) return `${Math.round(seconds * 1000)} ms`;
  return `${trimmed} s`;
}

export function displayParameterLabel(
  parameter: string | undefined,
  fallback: string,
): string {
  if (parameter && parameter in PARAMETER_DISPLAY_LABELS) {
    return PARAMETER_DISPLAY_LABELS[parameter];
  }
  return fallback.replace(/roll-off/gi, "rolloff");
}

/** Title-case enum labels from the spec (e.g. `off` → `Off`, `mono l` → `Mono L`). */
export function formatValueLabel(
  label: string,
  parameter?: string,
): string {
  if (!label) return label;
  // Numeric / unit values (times, dB, Hz, etc.)
  if (/^-?\d/.test(label)) {
    if (parameter === EARLY_LATE_MIX_PARAMETER) {
      const mix = formatEarlyLateMixLabel(label);
      if (mix) return mix;
    }
    const timeLabel = formatSubSecondTimeLabel(label);
    if (timeLabel) return timeLabel;
    const reverbTime = formatBareReverbSecondsLabel(label, parameter);
    if (reverbTime) return reverbTime;
    if (isMultiplyParameter(parameter) && !/\bx$/i.test(label.trim())) {
      return `${label}x`;
    }
    return label;
  }
  // Already mixed-case names (banks, NonLin, Edit (receive), …)
  if (/[A-Z]/.test(label.slice(1))) return label;
  return label.replace(/\b[a-z]/g, (ch) => ch.toUpperCase());
}
