export const BYTE_HIGHLIGHT_CLASS =
  "rounded-sm bg-red-600/80 px-0.5 text-white";

interface HighlightedHexProps {
  data: Uint8Array;
  /** Inclusive byte indices to render (defaults to entire dump). */
  offsets?: number[];
  highlightOffsets?: Iterable<number>;
  className?: string;
}

export function HighlightedHex({
  data,
  offsets,
  highlightOffsets = [],
  className = "",
}: HighlightedHexProps) {
  const highlight = new Set(highlightOffsets);
  const indices = offsets ?? Array.from({ length: data.length }, (_, i) => i);

  return (
    <span
      className={`font-led text-xs leading-relaxed break-all ${className}`}
    >
      {indices.map((index, pos) => (
        <span key={index}>
          {pos > 0 && " "}
          <span
            className={highlight.has(index) ? BYTE_HIGHLIGHT_CLASS : undefined}
          >
            {data[index]!.toString(16).toUpperCase().padStart(2, "0")}
          </span>
        </span>
      ))}
    </span>
  );
}
