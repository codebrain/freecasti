import { useEffect, useMemo, useState } from "react";
import {
  diffByteOffsets,
  rowTouchesChangedOffsets,
} from "@/debug/change";
import { buildByteBreakdown } from "@/debug/byteBreakdown";
import { HexDump } from "@/components/HexDump";
import { DumpByteTable } from "@/components/DumpByteTable";
import { downloadSyx, suggestSyxFilename } from "@/sysex/syxIo";
import { verifyDump } from "@/sysex/verify";
import { bytesToHex, NAME_OFFSET, PROGRAM_NAME_LENGTH } from "@/sysex/frame";
import { detectDumpFamily } from "@/sysex/hydrate";
import type { ControlDef } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import type { ProgUiRuntime } from "@/prog/uiState";

const PROG_CHECKSUM_OFFSETS = [152, 153, 154, 155] as const;
const SYS_CHECKSUM_OFFSETS = [72, 73, 74, 75] as const;

export interface DumpInspectorProps {
  bytes: Uint8Array;
  /** Older message of the same family, used for changed-byte highlighting. */
  previousBytes?: Uint8Array | null;
  progSpec?: DumpSpec | null;
  sysSpec?: DumpSpec | null;
  progControls?: ControlDef[];
  sysControls?: ControlDef[];
  progUi?: ProgUiRuntime | null;
}

function readProgramName(data: Uint8Array): string | undefined {
  if (data.length < NAME_OFFSET + PROGRAM_NAME_LENGTH) return undefined;
  const name = new TextDecoder("ascii")
    .decode(data.subarray(NAME_OFFSET, NAME_OFFSET + PROGRAM_NAME_LENGTH))
    .replace(/\s+$/, "");
  return name || undefined;
}

export function DumpInspector({
  bytes,
  previousBytes = null,
  progSpec = null,
  sysSpec = null,
  progControls = [],
  sysControls = [],
  progUi = null,
}: DumpInspectorProps) {
  const family = detectDumpFamily(bytes);
  const dumpSpec = family === "prog" ? progSpec : family === "system" ? sysSpec : null;
  const dumpControls =
    family === "prog" ? progControls : family === "system" ? sysControls : [];

  const [parseError, setParseError] = useState<string | null>(null);
  const [checksumOk, setChecksumOk] = useState<boolean | null>(null);
  const [showChangedOnly, setShowChangedOnly] = useState(true);
  const [ignoreChecksum, setIgnoreChecksum] = useState(true);

  const changedOffsets = useMemo(() => {
    if (!previousBytes) return [] as number[];
    return diffByteOffsets(previousBytes, bytes);
  }, [bytes, previousBytes]);

  const highlightOffsets = useMemo(() => {
    if (!ignoreChecksum || !family) return changedOffsets;
    const checksumOffsets: ReadonlySet<number> = new Set(
      family === "prog" ? PROG_CHECKSUM_OFFSETS : SYS_CHECKSUM_OFFSETS,
    );
    return changedOffsets.filter((offset) => !checksumOffsets.has(offset));
  }, [changedOffsets, family, ignoreChecksum]);

  const byteRows = useMemo(() => {
    if (!dumpSpec || !family) return [];
    return buildByteBreakdown(bytes, dumpSpec, family === "system" ? "system" : "prog", {
      controls: dumpControls,
      progUi: family === "prog" ? progUi : null,
    });
  }, [bytes, dumpControls, dumpSpec, family, progUi]);

  const visibleByteRows = useMemo(() => {
    if (!showChangedOnly || highlightOffsets.length === 0) return byteRows;
    return byteRows.filter((row) =>
      rowTouchesChangedOffsets(row, highlightOffsets),
    );
  }, [byteRows, highlightOffsets, showChangedOnly]);

  useEffect(() => {
    if (!family) {
      setParseError(null);
      setChecksumOk(null);
      return;
    }
    let cancelled = false;
    verifyDump(bytes, family).then((r) => {
      if (cancelled) return;
      setParseError(r.parseError);
      setChecksumOk(r.checksumOk);
    });
    return () => {
      cancelled = true;
    };
  }, [bytes, family]);

  const copyHex = async () => {
    await navigator.clipboard.writeText(bytesToHex(bytes));
  };

  const onDownloadSyx = () => {
    const label = family ?? "prog";
    downloadSyx({
      bytes,
      filename: suggestSyxFilename(
        label === "system" ? "system" : "prog",
        family === "prog" ? readProgramName(bytes) : undefined,
      ),
    });
  };

  return (
    <div className="space-y-2 pt-2">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        {checksumOk != null ? (
          <span className={checksumOk ? "text-green-400" : "text-red-400"}>
            Checksum {checksumOk ? "OK" : "FAIL"}
          </span>
        ) : (
          <span className="opacity-50">Checksum —</span>
        )}
        <span className="opacity-60">{bytes.length} B</span>
        {!family && <span className="opacity-50">· unknown SysEx</span>}
        <div className="ml-auto flex flex-wrap gap-2" data-preserve-selection="">
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
      </div>
      {parseError && (
        <div className="text-xs text-red-400">Parse: {parseError}</div>
      )}
      <div className="overflow-visible opacity-90">
        <HexDump data={bytes} highlightOffsets={highlightOffsets} />
      </div>
      {byteRows.length > 0 && (
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
            <label className="flex cursor-pointer items-center gap-2 text-xs opacity-80">
              <input
                type="checkbox"
                className="accent-[color:var(--color-label)]"
                checked={showChangedOnly}
                disabled={highlightOffsets.length === 0}
                onChange={(event) => setShowChangedOnly(event.target.checked)}
              />
              <span>Changed bytes only</span>
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
          </div>
          <DumpByteTable
            data={bytes}
            rows={visibleByteRows}
            highlightOffsets={highlightOffsets}
            emptyMessage={
              showChangedOnly
                ? "No table rows include changed bytes"
                : "No breakdown available"
            }
          />
        </div>
      )}
    </div>
  );
}
