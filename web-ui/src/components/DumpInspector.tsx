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
import {
  bytesToHex,
  NAME_OFFSET,
  PROGRAM_NAME_LENGTH,
  PROG_CHECKSUM_OFFSETS,
  SYS_CHECKSUM_OFFSETS,
} from "@/sysex/frame";
import { detectDumpFamily } from "@/sysex/hydrate";
import type { ControlDef } from "@/spec/controls";
import type { DumpSpec, SpecField } from "@/spec/types";
import type { ProgUiRuntime } from "@/prog/uiState";
import type { RegBlobLayout } from "@/sysex/registerBasisBlob";
import {
  decodeRegisterBasisBlob,
  payloadValue,
} from "@/sysex/registerBasisBlob";
import { formatValueLabel } from "@/spec/labels";

export interface DumpInspectorProps {
  bytes: Uint8Array;
  /** Older message of the same family, used for changed-byte highlighting. */
  previousBytes?: Uint8Array | null;
  progSpec?: DumpSpec | null;
  sysSpec?: DumpSpec | null;
  progControls?: ControlDef[];
  sysControls?: ControlDef[];
  progUi?: ProgUiRuntime | null;
  regBlob?: RegBlobLayout | null;
}

interface RegisterBasisRow {
  id: string;
  label: string;
  stored: string;
  live: string | null;
  diverged: boolean;
}

function storedLabel(
  encoded: number,
  payloadField: SpecField | undefined,
): string {
  const entry = payloadField?.value_map?.entries.find(
    (e) => e.encoded === encoded,
  );
  if (entry) {
    return `${formatValueLabel(entry.label, payloadField?.parameter)} (${encoded})`;
  }
  return String(encoded);
}

function buildRegisterBasisRows(
  data: Uint8Array,
  regBlob: RegBlobLayout,
  spec: DumpSpec,
): RegisterBasisRow[] {
  const basis = decodeRegisterBasisBlob(data, regBlob);
  if (!basis) return [];
  const fieldsById = new Map(spec.fields.map((f) => [f.id, f]));
  const rows: RegisterBasisRow[] = [];
  for (const field of regBlob.fields) {
    if (!field.payloadField || field.id === "name") continue;
    const stored = basis.values[field.id];
    if (stored == null) continue;
    const payloadField = fieldsById.get(field.payloadField);
    const live = payloadValue(data, field);
    rows.push({
      id: field.id,
      label: field.label,
      stored: storedLabel(stored, payloadField),
      live: live == null ? null : storedLabel(live, payloadField),
      diverged: live != null && live !== stored,
    });
  }
  return rows;
}

function RegisterBasisSection({
  bytes,
  regBlob,
  spec,
}: {
  bytes: Uint8Array;
  regBlob: RegBlobLayout;
  spec: DumpSpec;
}) {
  const basis = useMemo(
    () => decodeRegisterBasisBlob(bytes, regBlob),
    [bytes, regBlob],
  );
  const rows = useMemo(
    () => buildRegisterBasisRows(bytes, regBlob, spec),
    [bytes, regBlob, spec],
  );
  if (!basis) return null;
  const divergedCount = rows.filter((row) => row.diverged).length;
  return (
    <div className="space-y-1" data-testid="register-basis-section">
      <h4 className="label-caps text-[0.65rem] opacity-70">Register basis</h4>
      <div className="text-xs">
        <span className="text-[color:var(--color-label)]">
          “{basis.name}”
        </span>
        <span className="opacity-60"> · store #{basis.storeCounter}</span>
        {divergedCount > 0 && (
          <span className="text-amber-400">
            {" "}
            · {divergedCount} unstored edit{divergedCount === 1 ? "" : "s"}
          </span>
        )}
      </div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[0.65rem] leading-snug">
          <thead>
            <tr className="border-b border-border/50 bg-white/10 text-[color:var(--color-label)]">
              <th className="py-1 pr-2 font-normal">Parameter</th>
              <th className="py-1 pr-2 font-normal">Stored</th>
              <th className="py-1 font-normal">Current</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.id}
                className="border-b border-border/20 align-top"
              >
                <td className="py-0.5 pr-2 text-[color:var(--color-label)]">
                  {row.label}
                </td>
                <td className="py-0.5 pr-2">{row.stored}</td>
                <td
                  className={
                    row.diverged ? "py-0.5 text-amber-400" : "py-0.5 opacity-70"
                  }
                >
                  {row.live == null
                    ? "—"
                    : row.diverged
                      ? `${row.live} (unstored edit)`
                      : "same"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
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
  regBlob = null,
}: DumpInspectorProps) {
  const family = detectDumpFamily(bytes);
  const dumpSpec = family === "prog" ? progSpec : family === "system" ? sysSpec : null;
  const dumpControls = useMemo(
    () =>
      family === "prog" ? progControls : family === "system" ? sysControls : [],
    [family, progControls, sysControls],
  );

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
      regBlob: family === "prog" ? regBlob : null,
    });
  }, [bytes, dumpControls, dumpSpec, family, progUi, regBlob]);

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
      {family === "prog" && regBlob && progSpec && (
        <RegisterBasisSection
          bytes={bytes}
          regBlob={regBlob}
          spec={progSpec}
        />
      )}
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
