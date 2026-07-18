import type { ByteBreakdownRow } from "@/debug/byteBreakdown";
import { HighlightedHex } from "@/components/HighlightedHex";

interface DumpByteTableProps {
  data: Uint8Array;
  rows: ByteBreakdownRow[];
  highlightOffsets?: Iterable<number>;
  emptyMessage?: string;
}

function formatOffsetRange(start: number, end: number): string {
  return start === end ? String(start) : `${start}–${end}`;
}

export function DumpByteTable({
  data,
  rows,
  highlightOffsets = [],
  emptyMessage = "No breakdown available",
}: DumpByteTableProps) {
  if (!rows.length) {
    return <p className="text-xs opacity-50">{emptyMessage}</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-left text-[0.65rem] leading-snug">
        <thead>
          <tr className="border-b border-border/50 text-[color:var(--color-label)]">
            <th className="py-1 pr-2 font-normal">Off</th>
            <th className="py-1 pr-2 font-normal">Bytes</th>
            <th className="py-1 pr-2 font-normal">Field</th>
            <th className="py-1 font-normal">Value</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={`${row.start}-${row.end}-${row.label}`}
              className="border-b border-border/20 align-top"
            >
              <td className="py-1 pr-2 whitespace-nowrap opacity-70">
                {formatOffsetRange(row.start, row.end)}
              </td>
              <td className="py-1 pr-2">
                <HighlightedHex
                  data={data}
                  offsets={row.offsets}
                  highlightOffsets={highlightOffsets}
                />
              </td>
              <td className="py-1 pr-2 text-[color:var(--color-label)]">
                {row.label}
              </td>
              <td className="py-1 break-words">{row.meaning}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
