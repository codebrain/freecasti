import { SYSEX_END, SYSEX_START } from "@/sysex/frame";

export const BYTE_HIGHLIGHT_CLASS =
  "rounded-sm bg-red-600/80 px-0.5 text-white";

/** SysEx start (F0) / end (F7) framing bytes. */
export const BYTE_FRAME_CLASS = "text-red-400";

/** Runs of this many or more ASCII spaces (0x20) collapse to `(...)`. */
export const SPACE_RUN_COLLAPSE_MIN = 3;

interface HighlightedHexProps {
  data: Uint8Array;
  /** Inclusive byte indices to render (defaults to entire dump). */
  offsets?: number[];
  highlightOffsets?: Iterable<number>;
  className?: string;
  /** Collapse long runs of 0x20 to `(...)`. Defaults to true. */
  collapseSpaceRuns?: boolean;
  /** Break the hex into lines of this many tokens. Unset renders one flow. */
  wrapEvery?: number;
}

type HexToken =
  | { kind: "byte"; index: number }
  | { kind: "space_run"; indices: number[] };

function isSysexFrameByte(data: Uint8Array, index: number): boolean {
  const value = data[index];
  if (value === undefined) return false;
  return (
    (index === 0 && value === SYSEX_START) ||
    (index === data.length - 1 && value === SYSEX_END)
  );
}

/** Collapse long runs of 0x20 so padded ASCII fields stay readable. */
export function tokenizeHexOffsets(
  data: Uint8Array,
  indices: number[],
  minSpaceRun = SPACE_RUN_COLLAPSE_MIN,
): HexToken[] {
  const tokens: HexToken[] = [];
  let i = 0;
  while (i < indices.length) {
    const index = indices[i]!;
    if (data[index] === 0x20) {
      const run: number[] = [index];
      let j = i + 1;
      while (j < indices.length && data[indices[j]!] === 0x20) {
        run.push(indices[j]!);
        j++;
      }
      if (run.length >= minSpaceRun) {
        tokens.push({ kind: "space_run", indices: run });
        i = j;
        continue;
      }
    }
    tokens.push({ kind: "byte", index });
    i++;
  }
  return tokens;
}

export function HighlightedHex({
  data,
  offsets,
  highlightOffsets = [],
  className = "",
  collapseSpaceRuns = true,
  wrapEvery,
}: HighlightedHexProps) {
  const highlight = new Set(highlightOffsets);
  const indices = offsets ?? Array.from({ length: data.length }, (_, i) => i);
  const tokens = tokenizeHexOffsets(
    data,
    indices,
    collapseSpaceRuns ? SPACE_RUN_COLLAPSE_MIN : Number.POSITIVE_INFINITY,
  );

  const renderToken = (token: HexToken, showLeadingSpace: boolean) => {
    if (token.kind === "space_run") {
      const runHighlighted = token.indices.some((index) => highlight.has(index));
      return (
        <span key={`spaces-${token.indices[0]}-${token.indices.at(-1)}`}>
          {showLeadingSpace && " "}
          <span className={runHighlighted ? BYTE_HIGHLIGHT_CLASS : "opacity-50"}>
            (...)
          </span>
        </span>
      );
    }

    const { index } = token;
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
    const lines: HexToken[][] = [];
    for (let i = 0; i < tokens.length; i += wrapEvery) {
      lines.push(tokens.slice(i, i + wrapEvery));
    }
    return (
      <span className={baseClass}>
        {lines.map((line, lineIndex) => (
          <span key={`line-${lineIndex}`} className="block whitespace-nowrap">
            {line.map((token, pos) => renderToken(token, pos > 0))}
          </span>
        ))}
      </span>
    );
  }

  return (
    <span className={`${baseClass} break-all`}>
      {tokens.map((token, pos) => renderToken(token, pos > 0))}
    </span>
  );
}
