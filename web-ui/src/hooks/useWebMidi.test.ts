/**
 * @vitest-environment happy-dom
 */
import { act, createElement, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { MIDI_ERROR_DISMISS_MS } from "@/midi/midiErrorToast";
import { useWebMidi } from "./useWebMidi";

function renderUseWebMidi() {
  let midi: ReturnType<typeof useWebMidi> | null = null;
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  function Probe() {
    const state = useWebMidi();
    useEffect(() => {
      midi = state;
    });
    return null;
  }

  act(() => {
    root.render(createElement(Probe));
  });

  return {
    get current() {
      if (!midi) throw new Error("useWebMidi not ready");
      return midi;
    },
    cleanup() {
      act(() => {
        root.unmount();
      });
      container.remove();
    },
  };
}

describe("useWebMidi lastError", () => {
  let probe: ReturnType<typeof renderUseWebMidi>;

  beforeEach(() => {
    vi.useFakeTimers();
    probe = renderUseWebMidi();
  });

  afterEach(() => {
    probe.cleanup();
    vi.useRealTimers();
  });

  it("clears lastError when MIDI is turned off", () => {
    act(() => {
      probe.current.setEnabled(true);
      probe.current.sendBytes(new Uint8Array([0xf0, 0xf7]));
    });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(probe.current.lastError).toBe("MIDI not connected");

    act(() => {
      probe.current.setEnabled(false);
    });

    expect(probe.current.lastError).toBeNull();
  });

  it("auto-dismisses lastError after a timeout", () => {
    act(() => {
      probe.current.setEnabled(true);
      probe.current.sendBytes(new Uint8Array([0xf0, 0xf7]));
    });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(probe.current.lastError).toBe("MIDI not connected");

    act(() => {
      vi.advanceTimersByTime(MIDI_ERROR_DISMISS_MS);
    });

    expect(probe.current.lastError).toBeNull();
  });

  it("logs DEBUG when a send cannot reach MIDI", () => {
    act(() => {
      probe.current.setEnabled(true);
      probe.current.sendBytes(new Uint8Array([0xf0, 0xf7]));
    });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(probe.current.midiLog).toHaveLength(1);
    expect(probe.current.midiLog[0]?.direction).toBe("debug");
  });

  it("logDebugBytes records DEBUG without an error", () => {
    act(() => {
      probe.current.logDebugBytes(new Uint8Array([0xf0, 0xf7]));
    });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(probe.current.lastError).toBeNull();
    expect(probe.current.midiLog[0]?.direction).toBe("debug");
  });
});
