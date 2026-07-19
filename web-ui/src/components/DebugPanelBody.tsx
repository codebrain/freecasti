import { useEffect, useMemo, useState, type ReactNode } from "react";
import type { ChangeRecord } from "@/debug/change";
import type { TimingDiscrepancy } from "@/tempo/tempo";
import { DumpInspector } from "@/components/DumpInspector";
import type { MidiLogEntry } from "@/midi/midiLog";
import { detectDumpFamily } from "@/sysex/hydrate";
import type { ControlDef } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import type { ProgUiRuntime } from "@/prog/uiState";

export interface DebugPanelBodyProps {
  lastChange?: ChangeRecord | null;
  timingDiscrepancies?: TimingDiscrepancy[];
  tempoBpm?: number;
  midiLog?: readonly MidiLogEntry[];
  progSpec?: DumpSpec | null;
  sysSpec?: DumpSpec | null;
  progControls?: ControlDef[];
  sysControls?: ControlDef[];
  progUi?: ProgUiRuntime | null;
}

function DebugSection({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="space-y-2">
      <h3 className="label-caps border-b border-border/50 pb-1 text-[0.65rem] opacity-70">
        {title}
      </h3>
      {children}
    </section>
  );
}

function ChangeSummary({ change }: { change: ChangeRecord }) {
  if (change.kind === "param") {
    return (
      <div className="space-y-1 text-xs">
        <div className="text-[color:var(--color-label)]">{change.label}</div>
        <div className="font-led leading-relaxed">
          <span className="opacity-80">{change.beforeLabel}</span>
          <span className="mx-2 opacity-50">→</span>
          <span className="text-green-400">{change.afterLabel}</span>
        </div>
      </div>
    );
  }
  return <div className="text-xs opacity-80">{change.message}</div>;
}

function formatMidiLogTime(at: number): string {
  return new Date(at).toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function previousSameFamilyBytes(
  entries: readonly MidiLogEntry[],
  index: number,
): Uint8Array | null {
  const family = detectDumpFamily(entries[index]!.bytes);
  if (!family) return null;
  for (let i = index + 1; i < entries.length; i++) {
    if (detectDumpFamily(entries[i]!.bytes) === family) {
      return entries[i]!.bytes;
    }
  }
  return null;
}

function MidiLogList({
  entries,
  progSpec,
  sysSpec,
  progControls,
  sysControls,
  progUi,
}: {
  entries: readonly MidiLogEntry[];
  progSpec?: DumpSpec | null;
  sysSpec?: DumpSpec | null;
  progControls?: ControlDef[];
  sysControls?: ControlDef[];
  progUi?: ProgUiRuntime | null;
}) {
  const latestId = entries[0]?.id ?? null;
  const [expandedId, setExpandedId] = useState<string | null>(latestId);

  useEffect(() => {
    setExpandedId(latestId);
  }, [latestId]);

  if (!entries.length) {
    return <p className="text-xs opacity-50">No SysEx yet</p>;
  }

  return (
    <ul className="space-y-2 text-xs">
      {entries.map((entry, index) => {
        const expanded = entry.id === expandedId;
        return (
          <li
            key={entry.id}
            className="rounded border border-border/40 panel-recess"
          >
            <button
              type="button"
              className="flex w-full items-start gap-2 px-2 py-1.5 text-left font-led leading-relaxed hover:bg-secondary/30"
              aria-expanded={expanded}
              onClick={() =>
                setExpandedId((current) =>
                  current === entry.id ? null : entry.id,
                )
              }
            >
              <span className="mt-0.5 shrink-0 opacity-50" aria-hidden>
                {expanded ? "▾" : "▸"}
              </span>
              <span className="min-w-0 flex-1">
                <span
                  className={
                    entry.direction === "tx"
                      ? "text-green-400"
                      : entry.direction === "rx"
                        ? "text-sky-400"
                        : "text-zinc-500"
                  }
                >
                  {entry.direction === "tx"
                    ? "TX"
                    : entry.direction === "rx"
                      ? "RX"
                      : "DEBUG"}
                </span>
                <span className="opacity-50">
                  {" "}
                  · {formatMidiLogTime(entry.at)} ·{" "}
                </span>
                <span
                  className={
                    entry.direction === "rx" && entry.echoValidation === "match"
                      ? "text-green-400"
                      : entry.direction === "rx" &&
                          entry.echoValidation === "mismatch"
                        ? "text-red-400"
                        : entry.direction === "debug"
                          ? "text-zinc-500"
                          : undefined
                  }
                >
                  {entry.summary}
                </span>
              </span>
            </button>
            {expanded && (
              <div className="border-t border-border/40 px-2 pb-2">
                <DumpInspector
                  bytes={entry.bytes}
                  previousBytes={previousSameFamilyBytes(entries, index)}
                  progSpec={progSpec}
                  sysSpec={sysSpec}
                  progControls={progControls}
                  sysControls={sysControls}
                  progUi={progUi}
                />
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export function DebugPanelBody({
  lastChange,
  timingDiscrepancies = [],
  tempoBpm,
  midiLog = [],
  progSpec = null,
  sysSpec = null,
  progControls = [],
  sysControls = [],
  progUi = null,
}: DebugPanelBodyProps) {
  const inspectorProps = useMemo(
    () => ({
      progSpec,
      sysSpec,
      progControls,
      sysControls,
      progUi,
    }),
    [progControls, progSpec, progUi, sysControls, sysSpec],
  );

  return (
    <div className="space-y-5 px-4 py-4 text-sm font-led">
      {lastChange && (
        <DebugSection title="Last change">
          <ChangeSummary change={lastChange} />
        </DebugSection>
      )}

      <DebugSection title="MIDI SysEx">
        <MidiLogList entries={midiLog} {...inspectorProps} />
      </DebugSection>

      {timingDiscrepancies.length > 0 && (
        <DebugSection title="Timing">
          {tempoBpm != null && (
            <div className="text-xs opacity-60">{tempoBpm} BPM</div>
          )}
          <ul className="space-y-1.5 text-xs">
            {timingDiscrepancies.map((d) => (
              <li key={d.fieldId} className="leading-relaxed">
                <span className="text-[color:var(--color-label)]">{d.label}</span>
                {": "}
                <span className="text-[color:var(--color-foreground)]">
                  {d.division}
                </span>
                <span className="opacity-50"> → </span>
                <span>{d.actualLabel}</span>
                <span className="opacity-60">
                  {" "}
                  (Δ{d.deltaMs >= 0 ? "+" : ""}
                  {d.deltaMs.toFixed(1)} ms)
                </span>
              </li>
            ))}
          </ul>
        </DebugSection>
      )}
    </div>
  );
}
