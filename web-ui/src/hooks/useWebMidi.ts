import { useCallback, useEffect, useRef, useState } from "react";

import { createSysexSendThrottle } from "@/midi/sysexThrottle";
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
  lastSendAt: number | null;
  lastError: string | null;
  sendBytes: (bytes: Uint8Array) => void;
  midiLog: readonly MidiLogEntry[];
}

const LS_ENABLED = "m7.midi.enabled";
const LS_OUTPUT = "m7.midi.output";
const LS_INPUT = "m7.midi.input";
const LS_SEND_ON_CHANGE = "m7.midi.sendOnChange";

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
      return localStorage.getItem(LS_SEND_ON_CHANGE) === "1";
    } catch {
      return false;
    }
  });
  const [lastSendAt, setLastSendAt] = useState<number | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);
  const [midiLog, setMidiLog] = useState<MidiLogEntry[]>([]);
  const onReceiveRef = useRef(onReceive);
  onReceiveRef.current = onReceive;
  const throttleRef = useRef<ReturnType<typeof createSysexSendThrottle> | null>(null);

  const pushMidiLog = useCallback((direction: "tx" | "rx", bytes: Uint8Array) => {
    if (!isMidiSysex(bytes)) return;
    setMidiLog((prev) =>
      prependMidiLog(prev, createMidiLogEntry(direction, bytes)),
    );
  }, []);

  const sendImmediate = useCallback(
    (bytes: Uint8Array) => {
      if (!access) {
        setLastError("MIDI not connected");
        return;
      }
      const output = access.outputs.get(selectedOutputId);
      if (!output) {
        setLastError("No MIDI output selected");
        return;
      }
      try {
        output.send(bytes);
        pushMidiLog("tx", bytes);
        setLastSendAt(Date.now());
        setLastError(null);
      } catch (err) {
        setLastError(err instanceof Error ? err.message : String(err));
      }
    },
    [access, selectedOutputId, pushMidiLog],
  );

  useEffect(() => {
    throttleRef.current?.dispose();
    throttleRef.current = createSysexSendThrottle(sendImmediate);
    return () => throttleRef.current?.dispose();
  }, [sendImmediate]);

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
      throttleRef.current?.dispose();
      throttleRef.current = null;
      setMidiLog([]);
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

  const sendBytes = useCallback((bytes: Uint8Array) => {
    throttleRef.current?.enqueue(bytes);
  }, []);

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
    lastSendAt,
    lastError,
    sendBytes,
    midiLog,
  };
}
