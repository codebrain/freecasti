import { SYSEX_END, SYSEX_START } from "@/sysex/frame";

export const BYTE_HIGHLIGHT_CLASS =
  "rounded-sm bg-red-600/80 px-0.5 text-white";

/** SysEx start (F0) / end (F7) framing bytes. */
export const BYTE_FRAME_CLASS = "text-red-400";

interface HighlightedHexProps {
  data: Uint8Array;
  /** Inclusive byte indices to render (defaults to entire dump). */
  offsets?: number[];
  highlightOffsets?: Iterable<number>;
  className?: string;
  /** Break the hex into lines of this many tokens. Unset renders one flow. */
  wrapEvery?: number;
}

function isSysexFrameByte(data: Uint8Array, index: number): boolean {
  const value = data[index];
  if (value === undefined) return false;
  return (
    (index === 0 && value === SYSEX_START) ||
    (index === data.length - 1 && value === SYSEX_END)
  );
}

export function HighlightedHex({
  data,
  offsets,
  highlightOffsets = [],
  className = "",
  wrapEvery,
}: HighlightedHexProps) {
  const highlight = new Set(highlightOffsets);
  const indices = offsets ?? Array.from({ length: data.length }, (_, i) => i);

  const renderByte = (index: number, showLeadingSpace: boolean) => {
    const value = data[index]!;
    const classNameForByte = highlight.has(index)
      ? BYTE_HIGHLIGHT_CLASS
      : isSysexFrameByte(data, index)
        ? BYTE_FRAME_CLASS
        : undefined;
    return (
      <span key={index}>
        {showLeadingSpace && " "}
        <span className={classNameForByte}>
          {value.toString(16).toUpperCase().padStart(2, "0")}
        </span>
      </span>
    );
  };

  const baseClass = `font-led text-xs leading-relaxed ${className}`.trim();

  if (wrapEvery && wrapEvery > 0) {
    const lines: number[][] = [];
    for (let i = 0; i < indices.length; i += wrapEvery) {
      lines.push(indices.slice(i, i + wrapEvery));
    }
    return (
      <span className={baseClass}>
        {lines.map((line, lineIndex) => (
          <span key={`line-${lineIndex}`} className="block whitespace-nowrap">
            {line.map((index, pos) => renderByte(index, pos > 0))}
          </span>
        ))}
      </span>
    );
  }

  return (
    <span className={`${baseClass} break-all`}>
      {indices.map((index, pos) => renderByte(index, pos > 0))}
    </span>
  );
}
