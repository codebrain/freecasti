export const MIDI_ERROR_DISMISS_MS = 4000;

/** MIDI errors are only surfaced while MIDI is enabled. */
export function shouldShowMidiError(
  enabled: boolean,
  lastError: string | null,
): lastError is string {
  return enabled && lastError !== null;
}
