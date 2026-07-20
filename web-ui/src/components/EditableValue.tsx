import { useEffect, useRef, useState } from "react";

interface EditableValueProps {
  displayValue: string;
  disabled?: boolean;
  /** Grey inactive readout; defaults to `disabled`. Set false when locked but still active. */
  dimmed?: boolean;
  featured?: boolean;
  size?: number;
  ariaLabel?: string;
  className?: string;
  onCommit: (draft: string) => void;
}

/** Click-to-type value readout; reverts when commit does not change state. */
export function EditableValue({
  displayValue,
  disabled = false,
  dimmed,
  featured = false,
  size = 68,
  ariaLabel,
  className = "",
  onCommit,
}: EditableValueProps) {
  const [focused, setFocused] = useState(false);
  const [draft, setDraft] = useState(displayValue);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!focused) {
      setDraft(displayValue);
    }
  }, [displayValue, focused]);

  useEffect(() => {
    if (!focused) return;
    const el = inputRef.current;
    if (!el) return;
    el.focus();
    el.select();
  }, [focused]);

  const typography = featured
    ? "text-2xl font-medium tracking-wide"
    : size >= 100
      ? "text-lg"
      : "text-sm";

  const inactive = dimmed ?? disabled;

  const commit = () => {
    onCommit(draft);
    setFocused(false);
  };

  if (disabled && inactive) {
    return (
      <div
        data-testid="param-value"
        className={`tabular-nums min-h-[1.25rem] rounded-md border border-transparent px-1 control-value-inactive ${typography} ${className}`.trim()}
      >
        {displayValue}
      </div>
    );
  }

  if (disabled) {
    return (
      <div
        data-testid="param-value"
        className={`tabular-nums min-h-[1.25rem] rounded-md border border-transparent px-1 led-text ${typography} ${className}`.trim()}
      >
        {displayValue}
      </div>
    );
  }

  if (!focused) {
    return (
      <button
        type="button"
        data-testid="param-value"
        className={`tabular-nums min-h-[1.25rem] led-text cursor-text rounded-md border border-transparent px-1 transition-[background,box-shadow] duration-200 hover:bg-[oklch(0.62_0.24_27/0.1)] hover:shadow-[0_0_16px_oklch(0.62_0.24_27/0.12)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[color:var(--color-primary)] ${typography} ${className}`.trim()}
        aria-label={ariaLabel ? `Edit ${ariaLabel}` : "Edit value"}
        title="Click to type a value"
        onClick={(e) => {
          e.stopPropagation();
          setDraft(displayValue);
          setFocused(true);
        }}
      >
        {displayValue}
      </button>
    );
  }

  return (
    <input
      ref={inputRef}
      data-testid="param-value-input"
      type="text"
      autoComplete="off"
      autoCorrect="off"
      spellCheck={false}
      aria-label={ariaLabel ? `Edit ${ariaLabel}` : "Edit value"}
      value={draft}
      className={`min-h-[1.25rem] min-w-[3ch] rounded border border-[color:var(--color-primary)]/45 bg-[oklch(0.1_0.008_252)] px-1 text-center font-led tabular-nums text-[color:var(--color-led)] shadow-[inset_0_1px_3px_oklch(0_0_0/0.4)] focus:outline-none focus:ring-1 focus:ring-[color:var(--color-primary)]/25 ${typography} ${className}`.trim()}
      style={{ width: `${Math.max(3, draft.length + 1)}ch` }}
      onClick={(e) => e.stopPropagation()}
      onChange={(e) => setDraft(e.target.value)}
      onBlur={commit}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          (e.currentTarget as HTMLInputElement).blur();
        } else if (e.key === "Escape") {
          e.preventDefault();
          setDraft(displayValue);
          setFocused(false);
        }
        e.stopPropagation();
      }}
    />
  );
}
