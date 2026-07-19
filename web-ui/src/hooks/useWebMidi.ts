import { useCallback, useEffect, useRef, useState } from "react";

import {
  classifyRxAgainstPendingTx,
  pendingTxEchoFromBytes,
  type PendingTxEcho,
} from "@/midi/txEcho";
import { createSysexSendThrottle } from "@/midi/sysexThrottle";
import { readStoredSendOnChangeThrottleMs } from "@/midi/sendOnChangeThrottle";
import { MIDI_ERROR_DISMISS_MS } from "@/midi/midiErrorToast";
import {
  createMidiLogEntry,
  isMidiSysex,
  prependMidiLog,
  type MidiLogEntry,
} from "@/midi/midiLog";

interface WebMidiState {
  supported: boolean;
  enabled: boolean;
  setEnabled: (on: boolean) => void;
  access: MIDIAccess | null;
  outputs: MIDIOutput[];
  inputs: MIDIInput[];
  selectedOutputId: string;
  selectedInputId: string;
  setSelectedOutputId: (id: string) => void;
  setSelectedInputId: (id: string) => void;
  sendOnChange: boolean;
  setSendOnChange: (on: boolean) => void;
  sendOnChangeThrottleMs: number;
  setSendOnChangeThrottleMs: (ms: number) => void;
  lastSendAt: number | null;
  lastError: string | null;
  sendBytes: (bytes: Uint8Array) => void;
  /** Log what would be sent without transmitting (MIDI off / send-on-change off). */
  logDebugBytes: (bytes: Uint8Array) => void;
  midiLog: readonly MidiLogEntry[];
  clearMidiLog: () => void;
}

const LS_ENABLED = "m7.midi.enabled";
const LS_OUTPUT = "m7.midi.output";
const LS_INPUT = "m7.midi.input";
const LS_SEND_ON_CHANGE = "m7.midi.sendOnChange";
const LS_SEND_ON_CHANGE_THROTTLE_MS = "m7.midi.sendOnChangeThrottleMs";

export function useWebMidi(
  onReceive?: (data: Uint8Array) => void,
): WebMidiState {
  const supported =
    typeof navigator !== "undefined" && "requestMIDIAccess" in navigator;

  const [enabled, setEnabledState] = useState(() => {
    try {
      return localStorage.getItem(LS_ENABLED) === "1";
    } catch {
      return false;
    }
  });
  const [access, setAccess] = useState<MIDIAccess | null>(null);
  const [outputs, setOutputs] = useState<MIDIOutput[]>([]);
  const [inputs, setInputs] = useState<MIDIInput[]>([]);
  const [selectedOutputId, setSelectedOutputId] = useState(() => {
    try {
      return localStorage.getItem(LS_OUTPUT) ?? "";
    } catch {
      return "";
    }
  });
  const [selectedInputId, setSelectedInputId] = useState(() => {
    try {
      return localStorage.getItem(LS_INPUT) ?? "";
    } catch {
      return "";
    }
  });
  const [sendOnChange, setSendOnChangeState] = useState(() => {
    try {
      const raw = localStorage.getItem(LS_SEND_ON_CHANGE);
      return raw === null ? true : raw === "1";
    } catch {
      return true;
    }
  });
  const [sendOnChangeThrottleMs, setSendOnChangeThrottleMsState] = useState(
    readStoredSendOnChangeThrottleMs,
  );
  const [lastSendAt, setLastSendAt] = useState<number | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);
  const [midiLog, setMidiLog] = useState<MidiLogEntry[]>([]);
  const onReceiveRef = useRef(onReceive);
  onReceiveRef.current = onReceive;
  const pendingTxEchoRef = useRef<PendingTxEcho | null>(null);
  const throttleRef = useRef<ReturnType<typeof createSysexSendThrottle> | null>(null);

  const pushMidiLog = useCallback(
    (
      direction: "tx" | "rx" | "debug",
      bytes: Uint8Array,
      options: {
        echoValidation?: "match" | "mismatch";
        echoDiffCount?: number;
      } = {},
    ) => {
      if (!isMidiSysex(bytes)) return;
      setMidiLog((prev) =>
        prependMidiLog(
          prev,
          createMidiLogEntry(direction, bytes, options),
        ),
      );
    },
    [],
  );

  const clearMidiLog = useCallback(() => {
    setMidiLog([]);
  }, []);

  /** Latest enqueue intent; throttle coalesces to one pending payload. */
  const deliverModeRef = useRef<"tx" | "debug">("tx");

  const sendImmediate = useCallback(
    (bytes: Uint8Array) => {
      const mode = deliverModeRef.current;
      if (mode === "debug") {
        pushMidiLog("debug", bytes);
        return;
      }
      if (!access) {
        pushMidiLog("debug", bytes);
        setLastError("MIDI not connected");
        return;
      }
      const output = access.outputs.get(selectedOutputId);
      if (!output) {
        pushMidiLog("debug", bytes);
        setLastError("No MIDI output selected");
        return;
      }
      try {
        output.send(bytes);
        pendingTxEchoRef.current = pendingTxEchoFromBytes(bytes);
        pushMidiLog("tx", bytes);
        setLastSendAt(Date.now());
        setLastError(null);
      } catch (err) {
        pushMidiLog("debug", bytes);
        setLastError(err instanceof Error ? err.message : String(err));
      }
    },
    [access, selectedOutputId, pushMidiLog],
  );

  useEffect(() => {
    throttleRef.current?.dispose();
    throttleRef.current = createSysexSendThrottle(
      sendImmediate,
      sendOnChangeThrottleMs,
    );
    return () => throttleRef.current?.dispose();
  }, [sendImmediate, sendOnChangeThrottleMs]);

  const refreshPorts = useCallback((midi: MIDIAccess) => {
    setOutputs(Array.from(midi.outputs.values()));
    setInputs(Array.from(midi.inputs.values()));
  }, []);

  const setEnabled = useCallback((on: boolean) => {
    setEnabledState(on);
    try {
      localStorage.setItem(LS_ENABLED, on ? "1" : "0");
    } catch {
      /* ignore */
    }
    if (!on) {
      pendingTxEchoRef.current = null;
      setAccess(null);
      setOutputs([]);
      setInputs([]);
      setLastError(null);
    }
  }, []);

  useEffect(() => {
    if (!lastError) return;
    const id = window.setTimeout(() => setLastError(null), MIDI_ERROR_DISMISS_MS);
    return () => window.clearTimeout(id);
  }, [lastError]);

  useEffect(() => {
    if (!enabled || !supported) return;
    let cancelled = false;
    navigator
      .requestMIDIAccess({ sysex: true })
      .then((midi) => {
        if (cancelled) return;
        setAccess(midi);
        refreshPorts(midi);
        midi.onstatechange = () => refreshPorts(midi);
      })
      .catch((err) => {
        setLastError(err instanceof Error ? err.message : String(err));
      });
    return () => {
      cancelled = true;
    };
  }, [enabled, supported, refreshPorts]);

  useEffect(() => {
    if (!access || !selectedInputId) return;
    const input = access.inputs.get(selectedInputId);
    if (!input) return;

    const handler = (ev: MIDIMessageEvent) => {
      if (!ev.data) return;
      const data = new Uint8Array(ev.data);
      const classification = classifyRxAgainstPendingTx(
        data,
        pendingTxEchoRef.current,
      );
      if (classification.kind === "echo") {
        pendingTxEchoRef.current = null;
        pushMidiLog("rx", data, {
          echoValidation: classification.validation,
          echoDiffCount: classification.diffCount,
        });
        return;
      }
      pushMidiLog("rx", data);
      onReceiveRef.current?.(data);
    };
    input.onmidimessage = handler;
    return () => {
      input.onmidimessage = null;
    };
  }, [access, selectedInputId, pushMidiLog]);

  const setSelectedOutputIdPersist = useCallback((id: string) => {
    setSelectedOutputId(id);
    try {
      localStorage.setItem(LS_OUTPUT, id);
    } catch {
      /* ignore */
    }
  }, []);

  const setSelectedInputIdPersist = useCallback((id: string) => {
    setSelectedInputId(id);
    try {
      localStorage.setItem(LS_INPUT, id);
    } catch {
      /* ignore */
    }
  }, []);

  const setSendOnChange = useCallback((on: boolean) => {
    setSendOnChangeState(on);
    try {
      localStorage.setItem(LS_SEND_ON_CHANGE, on ? "1" : "0");
    } catch {
      /* ignore */
    }
  }, []);

  const setSendOnChangeThrottleMs = useCallback((ms: number) => {
    setSendOnChangeThrottleMsState(ms);
    try {
      localStorage.setItem(LS_SEND_ON_CHANGE_THROTTLE_MS, String(ms));
    } catch {
      /* ignore */
    }
  }, []);

  const enqueueDeliver = useCallback(
    (bytes: Uint8Array, mode: "tx" | "debug") => {
      deliverModeRef.current = mode;
      if (throttleRef.current) {
        throttleRef.current.enqueue(bytes);
        return;
      }
      sendImmediate(bytes);
    },
    [sendImmediate],
  );

  const sendBytes = useCallback(
    (bytes: Uint8Array) => {
      enqueueDeliver(bytes, "tx");
    },
    [enqueueDeliver],
  );

  const logDebugBytes = useCallback(
    (bytes: Uint8Array) => {
      enqueueDeliver(bytes, "debug");
    },
    [enqueueDeliver],
  );

  return {
    supported,
    enabled,
    setEnabled,
    access,
    outputs,
    inputs,
    selectedOutputId,
    selectedInputId,
    setSelectedOutputId: setSelectedOutputIdPersist,
    setSelectedInputId: setSelectedInputIdPersist,
    sendOnChange,
    setSendOnChange,
    sendOnChangeThrottleMs,
    setSendOnChangeThrottleMs,
    lastSendAt,
    lastError,
    sendBytes,
    logDebugBytes,
    midiLog,
    clearMidiLog,
  };
}
