import "@/styles.css";
import "@/styles.compat.css";
import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import { DebugPanel } from "@/components/DebugPanel";
import { ControlTooltip } from "@/components/ControlTooltip";
import { AppHeaderBar, AppHeaderToolbar } from "@/components/AppHeaderToolbar";
import { HeaderBrand } from "@/components/HeaderBrand";
import {
  appSubheaderClass,
  toolbarButtonClass,
  toolbarSelectClass,
} from "@/components/toolbarButtons";
import { SendOnChangeControl } from "@/components/SendOnChangeControl";
import { HelpDialog } from "@/components/HelpDialog";
import { PresetSelector, PresetSummary } from "@/components/PresetSelector";
import { SavedPresetsPanel } from "@/components/SavedPresetsPanel";
import { ProgramPanel } from "@/components/ProgramPanel";
import { SystemPanel } from "@/components/SystemPanel";
import {
  allProgControls,
  buildParameterToFieldId,
  buildProgControlGroups,
  buildSystemControls,
} from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import {
  patchActiveSlotWithFactoryPreset,
  patchActiveSlotWithProgState,
} from "@/presets/loadPresetIntoSlot";
import {
  algorithmConstraintsFrom,
  isParameterActive,
} from "@/presets/algorithms";
import {
  groupPresetsByBank,
  resolveProgramBankIndex,
} from "@/presets/catalog";
import type { AbSide, ProgAbStore } from "@/presets/progAbSlot";
import {
  abSlotSelectorFromState,
  abCompareSlotTooltip,
  patchAbStoreActive,
  swapAbSlots,
} from "@/presets/progAbSlot";
import type { PresetCatalog } from "@/presets/types";
import { hydrateProgramFromBytes } from "@/sysex/hydrate";
import { importSyxBytes } from "@/sysex/importSyx";
import type { ProgSerializeState } from "@/sysex/serialize";
import { readSyxFromFile } from "@/sysex/syxIo";
import {
  progBytesFromSaved,
  sysBytesFromSaved,
  type SavedUserPreset,
} from "@/presets/userPresets";
import { useSysexOutput, type ActiveTab } from "@/hooks/useSysexOutput";
import { useDebugPanelResize } from "@/hooks/useDebugPanelResize";
import { useWebMidi } from "@/hooks/useWebMidi";
import {
  loadRuntime,
} from "@/loadAssets";
import type { ChangeRecord, ParamChange } from "@/debug/change";
import { useControlKeyboard } from "@/hooks/useControlKeyboard";
import { LEGAL_DISCLAIMER } from "@/content/legalDisclaimer";
import { MidiErrorToast } from "@/components/MidiErrorToast";
import { shouldShowMidiError } from "@/midi/midiErrorToast";
import type { ProgUiRuntime } from "@/prog/uiState";
import type { RegBlobLayout } from "@/sysex/registerBasisBlob";
import { displayParameterLabel } from "@/spec/labels";
import { computeTimingDiscrepancies } from "@/tempo/tempo";

import {
  commitProgIndividualFieldChange,
  applySysFieldChange,
} from "@/prog/applyFieldChange";
import { bootstrapAppState } from "@/app/bootstrap";
import { resolvePresetSlotOnBankChange } from "@/app/bankChange";
import { parseMidiReceive } from "@/app/midiReceive";
import { resolveSendOnChange } from "@/app/sendOnChange";
import {
  loadActiveTab,
  loadLockedFields,
  loadTempoModeFields,
} from "@/app/persistedState";
import {
  LS_DEBUG,
  LS_LOCKED,
  LS_PROG,
  LS_PROG_AB,
  LS_SYS,
  LS_TAB,
  LS_TEMPO_BPM,
  LS_TEMPO_MODE,
} from "@/app/storageKeys";

export function App() {
  const [loadError, setLoadError] = useState<string | null>(null);
  const [progSpec, setProgSpec] = useState<DumpSpec | null>(null);
  const [sysSpec, setSysSpec] = useState<DumpSpec | null>(null);
  const [catalog, setCatalog] = useState<PresetCatalog | null>(null);
  const [progTemplate, setProgTemplate] = useState<Uint8Array | null>(null);
  const [sysTemplate, setSysTemplate] = useState<Uint8Array | null>(null);
  const [progUi, setProgUi] = useState<ProgUiRuntime | null>(null);
  const [regBlob, setRegBlob] = useState<RegBlobLayout | null>(null);
  const [activeTab, setActiveTab] = useState<ActiveTab>(loadActiveTab);
  const [debugOpen, setDebugOpen] = useState(() => {
    try {
      return localStorage.getItem(LS_DEBUG) === "1";
    } catch {
      return false;
    }
  });
  const {
    width: debugPanelWidth,
    isResizing: debugPanelResizing,
    onResizePointerDown: onDebugPanelResizePointerDown,
  } = useDebugPanelResize();
  const [helpOpen, setHelpOpen] = useState(false);
  const [abStore, setAbStore] = useState<ProgAbStore | null>(null);
  const [sysState, setSysState] = useState<Record<string, number> | null>(null);
  const [lastChange, setLastChange] = useState<ChangeRecord | null>(null);
  const [selectedFieldId, setSelectedFieldId] = useState<string | null>(null);
  const [lockedFieldIds, setLockedFieldIds] = useState<Set<string>>(loadLockedFields);
  const [tempoBpm, setTempoBpm] = useState(() => {
    try {
      const raw = localStorage.getItem(LS_TEMPO_BPM);
      const n = raw ? Number(raw) : 120;
      return Number.isFinite(n) ? Math.max(20, Math.min(300, n)) : 120;
    } catch {
      return 120;
    }
  });
  const [tempoModeFields, setTempoModeFields] = useState<Set<string>>(loadTempoModeFields);
  const importRef = useRef<HTMLInputElement>(null);
  const suppressSendOnChangeRef = useRef(false);
  const prevProgStateForSendRef = useRef<ProgSerializeState | null>(null);
  const prevSysStateForSendRef = useRef<Record<string, number> | null>(null);

  const progGroups = useMemo(
    () => (progSpec ? buildProgControlGroups(progSpec) : []),
    [progSpec],
  );
  const sysControls = useMemo(
    () => (sysSpec ? buildSystemControls(sysSpec) : []),
    [sysSpec],
  );
  const progControls = useMemo(
    () => (progSpec ? allProgControls(progSpec) : []),
    [progSpec],
  );
  const paramToField = useMemo(
    () => (progSpec ? buildParameterToFieldId(progSpec) : new Map()),
    [progSpec],
  );
  const banks = useMemo(
    () => (catalog ? groupPresetsByBank(catalog) : []),
    [catalog],
  );

  const activeAb = abStore?.active ?? "a";
  const activeSlot = abStore?.[activeAb];
  const progState = activeSlot?.state ?? null;
  const bankIdx = activeSlot?.bankIdx ?? 0;

  const abTooltips = useMemo(
    () =>
      abStore
        ? {
            a: abCompareSlotTooltip({
              side: "a",
              active: abStore.active,
              programName: abStore.a.state.programName,
              bankName: banks[abStore.a.bankIdx]?.displayName,
            }),
            b: abCompareSlotTooltip({
              side: "b",
              active: abStore.active,
              programName: abStore.b.state.programName,
              bankName: banks[abStore.b.bankIdx]?.displayName,
            }),
          }
        : { a: "Compare slot A", b: "Compare slot B" },
    [abStore, banks],
  );

  const setActiveProgState = useCallback(
    (next: ProgSerializeState | ((prev: ProgSerializeState) => ProgSerializeState)) => {
      setAbStore((store) => {
        if (!store) return store;
        const slot = store[store.active];
        const nextState = typeof next === "function" ? next(slot.state) : next;
        return patchAbStoreActive(store, { state: nextState });
      });
    },
    [],
  );

  const algorithmConstraints = useMemo(
    () => algorithmConstraintsFrom(catalog),
    [catalog],
  );
  const activeProgramBankIndex = useMemo(
    () =>
      resolveProgramBankIndex(banks, bankIdx, progState?.encoded),
    [banks, bankIdx, progState?.encoded],
  );

  const isProgParamActive = useCallback(
    (parameter: string | undefined) =>
      isParameterActive(activeProgramBankIndex, parameter, algorithmConstraints),
    [activeProgramBankIndex, algorithmConstraints],
  );

  const progControlByField = useMemo(() => {
    const map = new Map<string, ControlDef>();
    if (!progSpec) return map;
    for (const control of allProgControls(progSpec)) {
      map.set(control.fieldId, control);
    }
    return map;
  }, [progSpec]);

  const sysControlByField = useMemo(
    () => new Map(sysControls.map((control) => [control.fieldId, control])),
    [sysControls],
  );

  const toggleFieldLock = useCallback((fieldId: string) => {
    setLockedFieldIds((prev) => {
      const next = new Set(prev);
      if (next.has(fieldId)) next.delete(fieldId);
      else next.add(fieldId);
      try {
        localStorage.setItem(LS_LOCKED, JSON.stringify([...next]));
      } catch {
        /* ignore */
      }
      return next;
    });
  }, []);

  const sysex = useSysexOutput(
    progState,
    sysState,
    activeTab,
    progSpec,
    sysSpec,
    progTemplate,
    sysTemplate,
    progUi,
  );

  const recordAction = useCallback(
    (family: ActiveTab, message: string) => {
      setLastChange({ kind: "action", family, message });
    },
    [],
  );

  const recordParamChange = useCallback(
    (family: ActiveTab, change: ParamChange) => {
      setLastChange({ kind: "param", family, ...change });
    },
    [],
  );

  const onSelectAb = useCallback(
    (side: AbSide) => {
      setSelectedFieldId(null);
      setActiveProgState((prev) => {
        if (prev.ui?.mode !== "browse") return prev;
        return { ...prev, ui: { mode: "idle" } };
      });
      if (abStore && abStore.active !== side) {
        recordAction("prog", `switch to slot ${side.toUpperCase()}`);
      }
      setAbStore((store) =>
        store && store.active !== side ? { ...store, active: side } : store,
      );
    },
    [abStore, recordAction, setActiveProgState],
  );

  const onSwapAb = useCallback(() => {
    setSelectedFieldId(null);
    setAbStore((store) => (store ? swapAbSlots(store) : store));
    recordAction("prog", "swap slots A/B");
  }, [recordAction]);

  const onClearSelection = useCallback(() => {
    setSelectedFieldId(null);
    setActiveProgState((prev) => {
      if (prev.ui?.mode !== "browse") return prev;
      setLastChange({ kind: "action", family: "prog", message: "deselect" });
      return { ...prev, ui: { mode: "idle" } };
    });
  }, [setActiveProgState]);

  const onSelectProgField = useCallback(
    (fieldId: string) => {
      setSelectedFieldId(fieldId);
      const control = progControlByField.get(fieldId);
      if (!control?.parameter || !isProgParamActive(control.parameter)) return;
      recordAction(
        "prog",
        `select ${displayParameterLabel(control.parameter, control.label)}`,
      );
      setActiveProgState((prev) => ({
        ...prev,
        ui: { mode: "browse", parameter: control.parameter! },
      }));
    },
    [progControlByField, isProgParamActive, setActiveProgState, recordAction],
  );

  const onProgStep = useCallback(
    (fieldId: string, encoded: number) => {
      const control = progControlByField.get(fieldId);
      let change: ParamChange | null = null;
      setActiveProgState((prev) => {
        const result = commitProgIndividualFieldChange(
          prev,
          fieldId,
          encoded,
          control,
          {
            isParameterActive: isProgParamActive,
            tempoModeFields,
            tempoBpm,
          },
        );
        if (result.kind !== "change") return prev;
        change = result.change;
        return result.state;
      });
      if (change) recordParamChange("prog", change);
    },
    [
      progControlByField,
      isProgParamActive,
      recordParamChange,
      tempoModeFields,
      tempoBpm,
      setActiveProgState,
    ],
  );

  const onSysStep = useCallback(
    (fieldId: string, encoded: number) => {
      if (!sysState) return;
      const result = applySysFieldChange(
        sysState,
        fieldId,
        encoded,
        sysControlByField.get(fieldId),
      );
      if (result.kind !== "change") return;
      recordParamChange("system", result.change);
      setSysState(result.state);
    },
    [sysState, sysControlByField, recordParamChange],
  );

  useControlKeyboard({
    selectedFieldId,
    activeTab,
    progEncoded: progState?.encoded ?? null,
    progUiState: progState?.ui ?? null,
    sysEncoded: sysState,
    progControls: progControlByField,
    sysControls: sysControlByField,
    isProgParamActive,
    onProgStep,
    onSysStep,
    onClearSelection,
    tempoModeFields,
    tempoBpm,
  });

  const timingDiscrepancies = useMemo(() => {
    if (!progState || !progSpec || tempoBpm <= 0) return [];
    return computeTimingDiscrepancies(
      allProgControls(progSpec),
      progState.encoded,
      tempoBpm,
      tempoModeFields,
    );
  }, [progState, progSpec, tempoBpm, tempoModeFields]);

  const onTempoBpmChange = useCallback((bpm: number) => {
    setTempoBpm(bpm);
    try {
      localStorage.setItem(LS_TEMPO_BPM, String(bpm));
    } catch {
      /* ignore */
    }
  }, []);

  const toggleTempoMode = useCallback(
    (fieldId: string) => {
      const control = progControlByField.get(fieldId);
      const enabling = !tempoModeFields.has(fieldId);
      setTempoModeFields((prev) => {
        const next = new Set(prev);
        if (enabling) next.add(fieldId);
        else next.delete(fieldId);
        try {
          localStorage.setItem(LS_TEMPO_MODE, JSON.stringify([...next]));
        } catch {
          /* ignore */
        }
        return next;
      });
      if (enabling && control && tempoBpm > 0) {
        let change: ParamChange | null = null;
        setActiveProgState((prev) => {
          const current = prev.encoded[fieldId];
          if (current === undefined) return prev;
          const nextTempoFields = new Set(tempoModeFields);
          nextTempoFields.add(fieldId);
          const result = commitProgIndividualFieldChange(
            prev,
            fieldId,
            current,
            control,
            {
              isParameterActive: isProgParamActive,
              tempoModeFields: nextTempoFields,
              tempoBpm,
            },
          );
          if (result.kind !== "change") return prev;
          change = result.change;
          return result.state;
        });
        if (change) recordParamChange("prog", change);
      }
    },
    [
      progControlByField,
      tempoBpm,
      tempoModeFields,
      isProgParamActive,
      recordParamChange,
      setActiveProgState,
    ],
  );

  useEffect(() => {
    setSelectedFieldId(null);
    setActiveProgState((prev) => {
      if (prev.ui?.mode !== "browse") return prev;
      setLastChange({ kind: "action", family: "prog", message: "deselect" });
      return { ...prev, ui: { mode: "idle" } };
    });
  }, [activeTab, setActiveProgState]);

  useEffect(() => {
    if (!selectedFieldId || activeTab !== "prog") return;
    const control = progControlByField.get(selectedFieldId);
    if (control && !isProgParamActive(control.parameter)) {
      setSelectedFieldId(null);
      setActiveProgState((prev) => {
        if (prev.ui?.mode !== "browse") return prev;
        setLastChange({ kind: "action", family: "prog", message: "deselect" });
        return { ...prev, ui: { mode: "idle" } };
      });
    }
  }, [
    selectedFieldId,
    activeTab,
    isProgParamActive,
    progControlByField,
    setActiveProgState,
  ]);

  const handleMidiReceive = useCallback(
    (data: Uint8Array) => {
      if (!progSpec || !sysSpec) return;
      const parsed = parseMidiReceive(
        data,
        progSpec,
        allProgControls(progSpec),
        sysControls,
        banks,
      );
      if (!parsed) return;
      // Mark the resulting state change as RX-originated so the send-on-change
      // effect adopts it as a baseline instead of echoing it back to the device.
      suppressSendOnChangeRef.current = true;
      if (parsed.family === "prog") {
        recordAction("prog", "MIDI receive (program)");
        setAbStore((store) => {
          if (!store) return store;
          return patchAbStoreActive(store, {
            state: parsed.state,
            bankIdx: parsed.bankIdx,
            presetSlot: parsed.presetSlot,
          });
        });
        setSelectedFieldId(null);
        setActiveTab("prog");
      } else {
        recordAction("system", "MIDI receive (system)");
        setSysState(parsed.state);
        setSelectedFieldId(null);
        setActiveTab("system");
      }
    },
    [progSpec, sysSpec, sysControls, banks, recordAction],
  );

  const midi = useWebMidi(handleMidiReceive);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const {
          prog,
          system: sys,
          presets,
          templates,
          progUi: ui,
          regBlob: blobLayout,
        } = await loadRuntime();
        if (cancelled) return;

        setProgSpec(prog);
        setSysSpec(sys);
        setCatalog(presets);
        setProgTemplate(templates.prog);
        setSysTemplate(templates.system);
        setProgUi(ui);
        setRegBlob(blobLayout);

        const { abStore: restoredAb, sysState: restoredSys } = bootstrapAppState(
          prog,
          sys,
          presets,
        );

        setAbStore(restoredAb);
        setSysState(restoredSys);
      } catch (err) {
        if (!cancelled) {
          setLoadError(
            err instanceof Error ? err.message : String(err),
          );
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (abStore) {
      try {
        localStorage.setItem(LS_PROG_AB, JSON.stringify(abStore));
        localStorage.setItem(
          LS_PROG,
          JSON.stringify(abStore[abStore.active].state),
        );
      } catch {
        /* ignore */
      }
    }
  }, [abStore]);

  useEffect(() => {
    if (sysState) {
      try {
        localStorage.setItem(LS_SYS, JSON.stringify(sysState));
      } catch {
        /* ignore */
      }
    }
  }, [sysState]);

  useEffect(() => {
    try {
      localStorage.setItem(LS_TAB, activeTab);
    } catch {
      /* ignore */
    }
  }, [activeTab]);

  useEffect(() => {
    try {
      localStorage.setItem(LS_DEBUG, debugOpen ? "1" : "0");
    } catch {
      /* ignore */
    }
  }, [debugOpen]);

  const {
    enabled: midiEnabled,
    sendOnChange: midiSendOnChange,
    sendBytes: midiSendBytes,
    logDebugBytes: midiLogDebugBytes,
  } = midi;
  useEffect(() => {
    const result = resolveSendOnChange({
      suppressed: suppressSendOnChangeRef.current,
      prevProg: prevProgStateForSendRef.current,
      progState,
      prevSys: prevSysStateForSendRef.current,
      sysState,
      transmit: midiEnabled && midiSendOnChange,
      progBytes: sysex.progBytes,
      sysBytes: sysex.sysBytes,
    });

    prevProgStateForSendRef.current = result.nextPrevProg;
    prevSysStateForSendRef.current = result.nextPrevSys;
    if (result.suppressionConsumed) {
      suppressSendOnChangeRef.current = false;
    }

    for (const bytes of result.send) midiSendBytes(bytes);
    for (const bytes of result.logDebug) midiLogDebugBytes(bytes);
  }, [
    midiEnabled,
    midiSendOnChange,
    midiSendBytes,
    midiLogDebugBytes,
    progState,
    sysState,
    sysex.progBytes,
    sysex.sysBytes,
  ]);

  const applyBankPreset = useCallback(
    (bIdx: number, slot: number) => {
      if (!catalog) return;
      const bank = banks[bIdx];
      const entry = bank?.presets.find((p) => p.program_slot === slot);
      if (!entry) return;
      recordAction("prog", `preset ${entry.bank} / ${entry.preset}`);
      setAbStore((store) => {
        if (!store) return store;
        return patchActiveSlotWithFactoryPreset(
          store,
          entry,
          paramToField,
          lockedFieldIds,
          bIdx,
          slot,
        );
      });
    },
    [catalog, banks, paramToField, recordAction, lockedFieldIds],
  );

  const onBankChange = useCallback(
    (bIdx: number) => {
      setSelectedFieldId(null);
      const bank = banks[bIdx];
      const slot = resolvePresetSlotOnBankChange(
        bank,
        abStore?.[abStore.active]?.presetSlot ?? 0,
      );
      if (slot === null) return;
      applyBankPreset(bIdx, slot);
    },
    [banks, abStore, applyBankPreset],
  );

  const onPresetChange = (slot: number) => {
    setSelectedFieldId(null);
    applyBankPreset(bankIdx, slot);
  };

  const onImportSyx = async (file: Blob) => {
    if (!progSpec || !sysSpec) return;
    try {
      const data = await readSyxFromFile(file);
      const result = importSyxBytes(
        data,
        progSpec,
        allProgControls(progSpec),
        sysControls,
      );
      const label = file instanceof File ? file.name : "import";
      if (result.family === "prog" && result.progState) {
        recordAction("prog", `import ${label}`);
        setProgTemplate(new Uint8Array(data));
        setAbStore((store) => {
          if (!store) return store;
          return patchActiveSlotWithProgState(
            store,
            result.progState!,
            lockedFieldIds,
            abSlotSelectorFromState(banks, result.progState!),
          );
        });
        setActiveTab("prog");
      } else if (result.sysState) {
        recordAction("system", `import ${label}`);
        setSysTemplate(new Uint8Array(data));
        setSysState(result.sysState);
        setActiveTab("system");
      }
    } catch (err) {
      setLastChange({
        kind: "action",
        family: activeTab,
        message: err instanceof Error ? err.message : String(err),
      });
    }
  };

  const onLoadUserPreset = useCallback(
    (preset: SavedUserPreset) => {
      if (!progSpec) return;
      const progBytes = progBytesFromSaved(preset);
      recordAction("prog", `saved preset ${preset.name}`);
      const hydrated = hydrateProgramFromBytes(
        progBytes,
        progSpec,
        allProgControls(progSpec),
      );
      setProgTemplate(new Uint8Array(progBytes));
      setAbStore((store) => {
        if (!store) return store;
        return patchActiveSlotWithProgState(
          store,
          hydrated,
          lockedFieldIds,
          abSlotSelectorFromState(banks, hydrated),
        );
      });
      const sysB = sysBytesFromSaved(preset);
      if (sysB) {
        setSysTemplate(new Uint8Array(sysB));
        setSysState(hydrateSystemFromBytes(sysB, sysControls));
      } else if (preset.sys?.state) {
        setSysState(preset.sys.state);
      }
    },
    [progSpec, sysControls, banks, recordAction, lockedFieldIds],
  );

  if (loadError) {
    return (
      <div className="min-h-screen flex items-center justify-center p-8">
        <div className="panel-raised max-w-lg p-6 text-center space-y-3">
          <HeaderBrand centered logoClassName="h-12 w-auto" />
          <p className="text-red-400 text-sm">{loadError}</p>
          <p className="text-sm opacity-80">
            Run <code className="font-led">python run.py</code> from the repo root
            to sync <code className="font-led">web-ui/public/</code>, then reload.
          </p>
        </div>
      </div>
    );
  }

  if (!abStore || !sysState || !progSpec) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div
          className="h-8 w-8 rounded-full border-2 border-[color:var(--color-led-dim)] border-t-[color:var(--color-led)] animate-spin"
          role="status"
          aria-label="Loading"
        />
      </div>
    );
  }

  return (
    <div
      className={`min-h-screen px-4 py-8 md:px-6 md:py-12 ${
        debugOpen && !debugPanelResizing ? "transition-[padding] duration-300" : ""
      } ${debugOpen ? "debug-panel-open" : ""}`}
      style={
        debugOpen
          ? ({ "--debug-panel-width": `${debugPanelWidth}px` } as CSSProperties)
          : undefined
      }
    >
      <main className="mx-auto max-w-[1240px] rack-chassis">
        <h1 className="sr-only">Freecasti — Bricasti M7 reverb editor</h1>
        <AppHeaderBar>
          <HeaderBrand />
          <AppHeaderToolbar
            activeTab={activeTab}
            onTabChange={setActiveTab}
            tempoBpm={tempoBpm}
            onTempoBpmChange={onTempoBpmChange}
            onHelpOpen={() => setHelpOpen(true)}
            debugOpen={debugOpen}
            onDebugToggle={() => setDebugOpen((o) => !o)}
          />
        </AppHeaderBar>

        <div className={appSubheaderClass}>
          <div className="flex min-w-0 flex-1 flex-wrap items-center gap-3">
            {!midi.supported ? (
              <span className="text-xs opacity-50">Web MIDI not supported in this browser</span>
            ) : (
              <div
                className={`flex flex-wrap items-center gap-3 ${
                  midi.enabled ? "" : "invisible pointer-events-none"
                }`}
                aria-hidden={!midi.enabled}
              >
                <ControlTooltip description="MIDI output port for sending SysEx to the device.">
                  <select
                    className={toolbarSelectClass}
                    value={midi.selectedOutputId}
                    onChange={(e) => midi.setSelectedOutputId(e.target.value)}
                    disabled={!midi.enabled}
                  >
                    <option value="">Output…</option>
                    {midi.outputs.map((o) => (
                      <option key={o.id} value={o.id}>
                        {o.name}
                      </option>
                    ))}
                  </select>
                </ControlTooltip>
                <ControlTooltip description="MIDI input port for receiving program and system dumps from the device.">
                  <select
                    className={toolbarSelectClass}
                    value={midi.selectedInputId}
                    onChange={(e) => midi.setSelectedInputId(e.target.value)}
                    disabled={!midi.enabled}
                  >
                    <option value="">Input…</option>
                    {midi.inputs.map((i) => (
                      <option key={i.id} value={i.id}>
                        {i.name}
                      </option>
                    ))}
                  </select>
                </ControlTooltip>
                <ControlTooltip
                  description={`Send the current ${activeTab === "prog" ? "program" : "system"} dump to the Bricasti now`}
                >
                  <button
                    type="button"
                    className={toolbarButtonClass(false, !midi.enabled)}
                    disabled={!midi.enabled}
                    onClick={() =>
                      sysex.activeBytes && midi.sendBytes(sysex.activeBytes)
                    }
                  >
                    Send
                  </button>
                </ControlTooltip>
                <SendOnChangeControl
                  active={midi.sendOnChange}
                  disabled={!midi.enabled}
                  throttleMs={midi.sendOnChangeThrottleMs}
                  onToggle={() => midi.setSendOnChange(!midi.sendOnChange)}
                  onThrottleMsChange={midi.setSendOnChangeThrottleMs}
                />
              </div>
            )}
          </div>
          <ControlTooltip
            description={
              midi.supported
                ? "Enable Web MIDI to send and receive SysEx with the Bricasti M7."
                : "Web MIDI is not available in this browser."
            }
          >
            <button
              type="button"
              disabled={!midi.supported}
              className={`shrink-0 ${toolbarButtonClass(midi.enabled, !midi.supported)}`}
              onClick={() => midi.setEnabled(!midi.enabled)}
              aria-pressed={midi.enabled}
            >
              MIDI {midi.enabled ? "On" : "Off"}
            </button>
          </ControlTooltip>
        </div>

        <input
          ref={importRef}
          type="file"
          accept=".syx,.SYX"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) void onImportSyx(f);
            e.target.value = "";
          }}
        />

        {shouldShowMidiError(midi.enabled, midi.lastError) && (
          <MidiErrorToast message={midi.lastError} />
        )}

        <section
          id="editor-panel"
          role="tabpanel"
          aria-labelledby={
            activeTab === "prog" ? "header-tab-prog" : "header-tab-system"
          }
          className="panel-recess rack-editor-well px-6 md:px-10 py-10 md:py-12 space-y-8"
        >
          {activeTab === "prog" ? (
            <>
              <div className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)] xl:items-stretch">
                <PresetSelector
                  banks={banks}
                  bankIndex={bankIdx}
                  loadedBankIndex={progState.encoded.bank_index ?? 0}
                  loadedProgramSlot={progState.encoded.program_slot ?? 0}
                  onBankChange={onBankChange}
                  onPresetChange={onPresetChange}
                />
                <div className="flex h-full min-h-0 flex-col gap-4">
                  <PresetSummary
                    programName={progState.programName}
                    bankName={banks[bankIdx]?.displayName}
                    activeAb={activeAb}
                    abTooltips={abTooltips}
                    onSelectAb={onSelectAb}
                    onSwapAb={onSwapAb}
                  />
                  <ProgramPanel
                    groups={progGroups}
                    state={progState}
                    variant="core-only"
                    isParameterActive={isProgParamActive}
                    selectedFieldId={selectedFieldId}
                    onSelectField={onSelectProgField}
                    lockedFieldIds={lockedFieldIds}
                    onToggleFieldLock={toggleFieldLock}
                    tempoBpm={tempoBpm}
                    tempoModeFields={tempoModeFields}
                    onToggleTempoMode={toggleTempoMode}
                    onChange={(next, change) => {
                      recordParamChange("prog", change);
                      setActiveProgState(next);
                    }}
                  />
                </div>
              </div>
              <ProgramPanel
                groups={progGroups}
                state={progState}
                variant="rest-only"
                isParameterActive={isProgParamActive}
                selectedFieldId={selectedFieldId}
                onSelectField={onSelectProgField}
                lockedFieldIds={lockedFieldIds}
                onToggleFieldLock={toggleFieldLock}
                tempoBpm={tempoBpm}
                tempoModeFields={tempoModeFields}
                onToggleTempoMode={toggleTempoMode}
                onChange={(next, change) => {
                  recordParamChange("prog", change);
                  setActiveProgState(next);
                }}
                sidePanel={
                  <SavedPresetsPanel
                    progState={progState}
                    progBytes={sysex.progBytes}
                    sysState={sysState}
                    sysBytes={sysex.sysBytes}
                    onLoad={onLoadUserPreset}
                    onImportClick={() => importRef.current?.click()}
                  />
                }
              />
            </>
          ) : (
            <SystemPanel
              controls={sysControls}
              state={sysState}
              selectedFieldId={selectedFieldId}
              onSelectField={setSelectedFieldId}
              onChange={(next, change) => {
                recordParamChange("system", change);
                setSysState(next);
              }}
            />
          )}
        </section>

        <footer className="mt-8 px-6 pb-6 text-center text-[0.65rem] leading-relaxed text-[color:var(--color-label)] opacity-60">
          {LEGAL_DISCLAIMER}
        </footer>
      </main>

      <HelpDialog open={helpOpen} onClose={() => setHelpOpen(false)} />

      <DebugPanel
        open={debugOpen}
        onToggle={() => setDebugOpen((o) => !o)}
        width={debugPanelWidth}
        onResizePointerDown={onDebugPanelResizePointerDown}
        lastChange={lastChange}
        timingDiscrepancies={timingDiscrepancies}
        tempoBpm={tempoBpm}
        midiLog={midi.midiLog}
        onClearLog={midi.clearMidiLog}
        progSpec={progSpec}
        sysSpec={sysSpec}
        progControls={progControls}
        sysControls={sysControls}
        progUi={progUi}
        regBlob={regBlob}
      />
    </div>
  );
}
