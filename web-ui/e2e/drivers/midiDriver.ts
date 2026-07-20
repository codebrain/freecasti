/**
 * Transport-agnostic stand-in for the M7 hardware on the other end of the
 * MIDI connection. The web implementation is backed by a fake Web MIDI API
 * injected into the page; a VST/Max4Live harness would implement the same
 * interface over virtual MIDI ports or the host's plumbing.
 */
export interface MidiDriver {
  /**
   * Make the MIDI transport (un)available to the editor. Takes effect the
   * next time the editor starts or restarts.
   */
  setTransportAvailable(available: boolean): Promise<void>;

  /** Enable MIDI in the editor and wire it to this fake device. */
  connect(): Promise<void>;
  disconnect(): Promise<void>;

  /** Whether the editor currently reports that no MIDI transport exists. */
  transportReportedUnavailable(): Promise<boolean>;

  /** Deliver bytes from the device to the editor. */
  receiveFromDevice(bytes: Uint8Array): Promise<void>;

  /** Everything the editor has transmitted to the device, oldest first. */
  sentMessages(): Promise<Uint8Array[]>;
  clearSentMessages(): Promise<void>;
  /** Wait until the device has received at least `count` messages. */
  waitForSentCount(count: number, timeoutMs?: number): Promise<Uint8Array[]>;

  /**
   * Whether the editor classified the most recently received message as an
   * echo of its own transmission (rather than an external change).
   */
  lastReceiveWasEcho(): Promise<boolean>;
}
