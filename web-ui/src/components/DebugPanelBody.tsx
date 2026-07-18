import { useEffect, useMemo, useState, type ReactNode } from "react";
import {
  rowTouchesChangedOffsets,
  type ByteHighlight,
  type ChangeRecord,
} from "@/debug/change";
import { buildByteBreakdown } from "@/debug/byteBreakdown";
import type { TimingDiscrepancy } from "@/tempo/tempo";
import { HexDump } from "@/components/HexDump";
import { DumpByteTable } from "@/components/DumpByteTable";
import { downloadSyx, suggestSyxFilename } from "@/sysex/syxIo";
import { verifyDump } from "@/sysex/verify";
import { bytesToHex } from "@/sysex/frame";
import type { ActiveTab } from "@/hooks/useSysexOutput";
import type { MidiLogEntry } from "@/midi/midiLog";
import type { ControlDef } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import type { ProgUiRuntime } from "@/prog/uiState";

export interface DebugPanelBodyProps {
  activeTab: ActiveTab;
  progBytes: Uint8Array | null;
  sysBytes: Uint8Array | null;
  progChecksumOk: boolean;
  sysChecksumOk: boolean;
  lastChange?: ChangeRecord | null;
  byteHighlight?: ByteHighlight | null;
  programName?: string;
  timingDiscrepancies?: TimingDiscrepancy[];
  tempoBpm?: number;
  midiLog?: readonly MidiLogEntry[];
  dumpSpec?: DumpSpec | null;
  dumpControls?: ControlDef[];
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

function MidiLogList({ entries }: { entries: readonly MidiLogEntry[] }) {
  if (!entries.length) {
    return <p className="text-xs opacity-50">No SysEx yet</p>;
  }
  return (
    <ul className="space-y-1.5 text-xs">
      {entries.map((entry) => (
        <li key={entry.id} className="font-led leading-relaxed">
          <span
            className={
              entry.direction === "tx" ? "text-green-400" : "text-sky-400"
            }
          >
            {entry.direction === "tx" ? "TX" : "RX"}
          </span>
          <span className="opacity-50"> · {formatMidiLogTime(entry.at)} · </span>
          <span
            className={
              entry.direction === "rx" && entry.echoValidation === "match"
                ? "text-green-400"
                : entry.direction === "rx" && entry.echoValidation === "mismatch"
                  ? "text-red-400"
                  : undefined
            }
          >
            {entry.summary}
          </span>
        </li>
      ))}
    </ul>
  );
}

export function DebugPanelBody({
  activeTab,
  progBytes,
  sysBytes,
  progChecksumOk,
  sysChecksumOk,
  lastChange,
  byteHighlight,
  programName,
  timingDiscrepancies = [],
  tempoBpm,
  midiLog = [],
  dumpSpec,
  dumpControls = [],
  progUi = null,
}: DebugPanelBodyProps) {
  const activeBytes = activeTab === "prog" ? progBytes : sysBytes;
  const checksumOk = activeTab === "prog" ? progChecksumOk : sysChecksumOk;
  const activeLabel = activeTab === "prog" ? "Program" : "System";
  const [parseSummary, setParseSummary] = useState<string | null>(null);
  const [parseError, setParseError] = useState<string | null>(null);
  const [showChangedOnly, setShowChangedOnly] = useState(true);
  const [ignoreChecksum, setIgnoreChecksum] = useState(false);

  const activeHighlight = useMemo(() => {
    const base =
      byteHighlight?.family === activeTab ? byteHighlight.offsets : [];
    if (!ignoreChecksum) return base;
    const checksumOffsets = new Set(
      activeTab === "prog" ? [152, 153, 154, 155] : [72, 73, 74, 75],
    );
    return base.filter((offset) => !checksumOffsets.has(offset));
  }, [activeTab, byteHighlight, ignoreChecksum]);

  const byteRows = useMemo(() => {
    if (!activeBytes || !dumpSpec) return [];
    return buildByteBreakdown(activeBytes, dumpSpec, activeTab, {
      controls: dumpControls,
      progUi: activeTab === "prog" ? progUi : null,
    });
  }, [activeBytes, activeTab, dumpControls, dumpSpec, progUi]);

  const visibleByteRows = useMemo(() => {
    if (!showChangedOnly) return byteRows;
    return byteRows.filter((row) =>
      rowTouchesChangedOffsets(row, activeHighlight),
    );
  }, [activeHighlight, byteRows, showChangedOnly]);

  useEffect(() => {
    if (!activeBytes) {
      setParseSummary(null);
      setParseError(null);
      return;
    }
    let cancelled = false;
    verifyDump(activeBytes, activeTab).then((r) => {
      if (cancelled) return;
      setParseSummary(r.parseSummary);
      setParseError(r.parseError);
    });
    return () => {
      cancelled = true;
    };
  }, [activeBytes, activeTab]);

  const copyHex = async () => {
    if (!activeBytes) return;
    await navigator.clipboard.writeText(bytesToHex(activeBytes));
  };

  const onDownloadSyx = () => {
    if (!activeBytes) return;
    downloadSyx({
      bytes: activeBytes,
      filename: suggestSyxFilename(activeTab, programName),
    });
  };

  return (
    <div className="space-y-5 px-4 py-4 text-sm font-led">
      {lastChange && (
        <DebugSection title="Last change">
          <ChangeSummary change={lastChange} />
        </DebugSection>
      )}

      <DebugSection title="MIDI SysEx">
        <MidiLogList entries={midiLog} />
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

      <DebugSection title={`${activeLabel} dump`}>
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
          <span className={checksumOk ? "text-green-400" : "text-red-400"}>
            Checksum {checksumOk ? "OK" : "FAIL"}
          </span>
          <span className="opacity-60">
            {activeBytes?.length ?? 0} B
            <span className="opacity-40">
              {" "}
              · PROG {progBytes?.length ?? 0} B · SYS {sysBytes?.length ?? 0} B
            </span>
          </span>
        </div>
        {parseSummary && (
          <div className="text-xs text-[color:var(--color-label)]">{parseSummary}</div>
        )}
        {parseError && (
          <div className="text-xs text-red-400">Parse: {parseError}</div>
        )}
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded border border-border px-2 py-1 text-xs hover:bg-secondary/50"
            onClick={copyHex}
          >
            Copy hex
          </button>
          <button
            type="button"
            className="rounded border border-border px-2 py-1 text-xs hover:bg-secondary/50"
            onClick={onDownloadSyx}
          >
            Download .syx
          </button>
        </div>
        <div className="overflow-visible opacity-90">
          {activeBytes ? (
            <HexDump data={activeBytes} highlightOffsets={activeHighlight} />
          ) : (
            <span className="text-xs opacity-50">—</span>
          )}
        </div>
        {activeBytes && byteRows.length > 0 && (
          <div className="space-y-2">
            <label className="flex cursor-pointer items-center gap-2 text-xs opacity-80">
              <input
                type="checkbox"
                className="accent-[color:var(--color-label)]"
                checked={showChangedOnly}
                disabled={activeHighlight.length === 0}
                onChange={(event) => setShowChangedOnly(event.target.checked)}
              />
              <span>Changed bytes only</span>
              {activeHighlight.length > 0 ? (
                <span className="opacity-50">({activeHighlight.length} B)</span>
              ) : (
                <span className="opacity-40">(no recent change)</span>
              )}
            </label>
            <label className="flex cursor-pointer items-center gap-2 text-xs opacity-80">
              <input
                type="checkbox"
                className="accent-[color:var(--color-label)]"
                checked={ignoreChecksum}
                onChange={(event) => setIgnoreChecksum(event.target.checked)}
              />
              <span>Ignore checksum</span>
            </label>
            <DumpByteTable
              data={activeBytes}
              rows={visibleByteRows}
              highlightOffsets={activeHighlight}
              emptyMessage={
                showChangedOnly
                  ? "No table rows include changed bytes"
                  : "No breakdown available"
              }
            />
          </div>
        )}
      </DebugSection>
    </div>
  );
}
