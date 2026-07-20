/**
 * Init scripts injected into the page before the app loads. Playwright
 * serializes these functions, so they must be fully self-contained.
 */

export const FAKE_OUTPUT_ID = "fake-m7-out";
export const FAKE_INPUT_ID = "fake-m7-in";

/** Replace Web MIDI with an in-page fake exposing `window.__fakeMidi`. */
export function installFakeWebMidi(): void {
  const sent: number[][] = [];
  const output = {
    id: "fake-m7-out",
    name: "Fake M7 Out",
    send(bytes: Iterable<number>) {
      sent.push(Array.from(bytes));
    },
  };
  const input: {
    id: string;
    name: string;
    onmidimessage: ((ev: { data: Uint8Array }) => void) | null;
  } = {
    id: "fake-m7-in",
    name: "Fake M7 In",
    onmidimessage: null,
  };
  const access = {
    outputs: new Map([[output.id, output]]),
    inputs: new Map([[input.id, input]]),
    onstatechange: null as (() => void) | null,
  };
  Object.defineProperty(navigator, "requestMIDIAccess", {
    configurable: true,
    value: () => Promise.resolve(access),
  });
  Object.defineProperty(window, "__fakeMidi", {
    configurable: true,
    value: {
      sent,
      receive(bytes: number[]) {
        input.onmidimessage?.({ data: new Uint8Array(bytes) });
      },
      clear() {
        sent.length = 0;
      },
    },
  });
}

/** Strip Web MIDI support so the editor sees an unsupported environment. */
export function removeWebMidiSupport(): void {
  const nav = navigator as unknown as Record<string, unknown>;
  const proto = Navigator.prototype as unknown as Record<string, unknown>;
  try {
    delete proto.requestMIDIAccess;
  } catch {
    /* ignore */
  }
  try {
    delete nav.requestMIDIAccess;
  } catch {
    /* ignore */
  }
  try {
    delete (window as unknown as Record<string, unknown>).__fakeMidi;
  } catch {
    /* ignore */
  }
}
