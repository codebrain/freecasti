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
  const highlight = new Set(highlightOffsets);

  return (
    <div
      className={`font-led text-xs leading-relaxed break-all overflow-visible ${className}`}
    >
      {Array.from(data, (byte, index) => (
        <span key={index}>
          {index > 0 && " "}
          <span
            className={
              highlight.has(index)
                ? "rounded-sm bg-red-600/80 px-0.5 text-white"
                : undefined
            }
          >
            {byte.toString(16).toUpperCase().padStart(2, "0")}
          </span>
        </span>
      ))}
    </div>
  );
}
