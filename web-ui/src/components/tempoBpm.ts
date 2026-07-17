export const TEMPO_BPM_MIN = 20;
export const TEMPO_BPM_MAX = 300;

/** While editing, allow only digits (empty ok). */
export function sanitizeTempoDraft(raw: string): string {
  return raw.replace(/\D/g, "");
}

/** Commit draft to BPM; invalid/empty uses fallback. */
export function commitTempoBpmDraft(
  draft: string,
  fallback: number,
): number {
  const trimmed = draft.trim();
  if (!trimmed) {
    return clampTempoBpm(fallback);
  }
  const next = Number(trimmed);
  if (!Number.isFinite(next)) {
    return clampTempoBpm(fallback);
  }
  return clampTempoBpm(Math.round(next));
}

export function clampTempoBpm(bpm: number): number {
  return Math.max(TEMPO_BPM_MIN, Math.min(TEMPO_BPM_MAX, bpm));
}
