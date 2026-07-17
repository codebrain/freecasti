import { useEffect, useState, type ReactNode } from "react";
import type { ChangeRecord, ByteHighlight } from "@/debug/change";
import type { TimingDiscrepancy } from "@/tempo/tempo";
import { HexDump } from "@/components/HexDump";
import { downloadSyx, suggestSyxFilename } from "@/sysex/syxIo";
import { verifyDump } from "@/sysex/verify";
import { bytesToHex } from "@/sysex/frame";
import type { ActiveTab } from "@/hooks/useSysexOutput";
import type { MidiLogEntry } from "@/midi/midiLog";

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
          <span>{entry.summary}</span>
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
}: DebugPanelBodyProps) {
  const activeBytes = activeTab === "prog" ? progBytes : sysBytes;
  const checksumOk = activeTab === "prog" ? progChecksumOk : sysChecksumOk;
  const activeLabel = activeTab === "prog" ? "Program" : "System";
  const [parseSummary, setParseSummary] = useState<string | null>(null);
  const [parseError, setParseError] = useState<string | null>(null);

  const activeHighlight =
    byteHighlight?.family === activeTab ? byteHighlight.offsets : [];

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
      </DebugSection>
    </div>
  );
}
