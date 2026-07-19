import { HighlightedHex } from "@/components/HighlightedHex";

interface HexDumpProps {
  data: Uint8Array;
  highlightOffsets?: Iterable<number>;
  className?: string;
}

export function HexDump({
  data,
  highlightOffsets = [],
  className = "",
}: HexDumpProps) {
  return (
    <HighlightedHex
      data={data}
      highlightOffsets={highlightOffsets}
      className={`overflow-visible opacity-90 ${className}`}
    />
  );
}
