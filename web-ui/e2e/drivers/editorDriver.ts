/**
 * Target-agnostic driver for an "M7 editor" — the abstract application the
 * feature files describe. The web UI implements this over Playwright; a future
 * VST plugin or Max4Live patch harness can implement the same interface over
 * its own automation transport and reuse the features and step definitions
 * unchanged.
 *
 * All values are the human-readable forms shown to the user ("20 ms",
 * "-12 dB", "Mono L", "1/4"), never encoded device bytes or DOM details.
 */

export type EditorView = "program" | "system";
export type CompareSlot = "A" | "B";

export interface EditorDriver {
  /** Start the editor with a clean slate (no persisted state). */
  start(): Promise<void>;
  /** End the session and start a new one, keeping persisted state. */
  restart(): Promise<void>;

  activeView(): Promise<EditorView>;
  openView(view: EditorView): Promise<void>;

  /** Name of the currently loaded program. */
  programName(): Promise<string>;
  /** Load a factory program by bank display name and program name. */
  selectFactoryProgram(bank: string, program: string): Promise<void>;

  /** Set a parameter by typing/choosing a human-readable value. */
  setParameter(name: string, value: string): Promise<void>;
  /** The human-readable value currently shown for a parameter. */
  parameterValue(name: string): Promise<string>;
  /**
   * Every value the editor offers for a parameter, in low-to-high order,
   * exactly as displayed. Steps that display identically are collapsed.
   */
  parameterValues(name: string): Promise<string[]>;
  /** Whether the user can currently change the parameter. */
  parameterEditable(name: string): Promise<boolean>;
  lockParameter(name: string): Promise<void>;
  unlockParameter(name: string): Promise<void>;
  /** Give a parameter's control the editor's selection focus. */
  selectParameter(name: string): Promise<void>;
  /** Clear the current control selection. */
  deselectParameter(): Promise<void>;

  activeCompareSlot(): Promise<CompareSlot>;
  selectCompareSlot(slot: CompareSlot): Promise<void>;
  swapCompareSlots(): Promise<void>;

  saveUserPreset(name: string): Promise<void>;
  loadUserPreset(name: string): Promise<void>;
  deleteUserPreset(name: string): Promise<void>;
  savedPresetNames(): Promise<string[]>;

  /** Export the current program as a SysEx dump file. */
  exportProgramFile(): Promise<Uint8Array>;
  /** Export the current system settings as a SysEx dump file. */
  exportSystemFile(): Promise<Uint8Array>;
  /** Import a SysEx dump file (program or system). */
  importFile(bytes: Uint8Array, filename?: string): Promise<void>;

  setTempoBpm(bpm: number | string): Promise<void>;
  tempoBpm(): Promise<number>;
  setTempoMode(parameter: string, on: boolean): Promise<void>;
  /**
   * Signed millisecond error (actual − ideal) the editor surfaces for a
   * tempo-mode parameter whose note division cannot be hit exactly by a
   * device time step, or null when the division snaps perfectly.
   */
  timingErrorMs(parameter: string): Promise<number | null>;

  /** Transmit the active view's dump to the connected device now. */
  sendToDevice(): Promise<void>;
  setSendOnChange(on: boolean): Promise<void>;
  setSendOnChangeThrottleMs(ms: number): Promise<void>;
}
