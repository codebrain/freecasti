import { useEffect, useState } from "react";
import {
  clampTempoBpm,
  commitTempoBpmDraft,
  sanitizeTempoDraft,
  TEMPO_BPM_MAX,
  TEMPO_BPM_MIN,
} from "./tempoBpm";

interface TempoInputProps {
  bpm: number;
  onBpmChange: (bpm: number) => void;
  variant?: "inline" | "panel";
}

export function TempoInput({
  bpm,
  onBpmChange,
  variant = "panel",
}: TempoInputProps) {
  const inline = variant === "inline";
  const [focused, setFocused] = useState(false);
  const [draft, setDraft] = useState("");

  useEffect(() => {
    if (!focused) {
      setDraft(String(bpm));
    }
  }, [bpm, focused]);

  const displayValue = focused ? draft : String(bpm);

  const commit = () => {
    const next = commitTempoBpmDraft(draft, bpm);
    setDraft(String(next));
    if (next !== bpm) {
      onBpmChange(next);
    }
  };

  return (
    <label
      className={`flex items-center gap-2 ${
        inline ? "text-xs" : "justify-center border-t border-border/60 pt-4 mt-2 w-full"
      }`}
    >
      <span className={`label-caps ${inline ? "text-[0.6rem] opacity-70" : "text-[0.6rem]"}`}>
        BPM
      </span>
      <input
        type="text"
        inputMode="numeric"
        autoComplete="off"
        autoCorrect="off"
        spellCheck={false}
        name="m7-tempo-bpm"
        aria-label="Tempo BPM"
        value={displayValue}
        onFocus={(e) => {
          setDraft(String(bpm));
          setFocused(true);
          e.currentTarget.select();
        }}
        onChange={(e) => {
          setDraft(sanitizeTempoDraft(e.target.value));
        }}
        onBlur={() => {
          setFocused(false);
          commit();
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            (e.currentTarget as HTMLInputElement).blur();
          } else if (e.key === "ArrowUp") {
            e.preventDefault();
            const base = commitTempoBpmDraft(draft, bpm);
            const next = clampTempoBpm(base + 1);
            setDraft(String(next));
            onBpmChange(next);
          } else if (e.key === "ArrowDown") {
            e.preventDefault();
            const base = commitTempoBpmDraft(draft, bpm);
            const next = clampTempoBpm(base - 1);
            setDraft(String(next));
            onBpmChange(next);
          }
        }}
        className={`rounded border bg-input font-led text-center tabular-nums transition-colors focus:border-[color:var(--color-primary)]/45 focus:outline-none focus:ring-1 focus:ring-[color:var(--color-primary)]/25 ${
          inline
            ? "w-[3.25rem] border-[oklch(0.22_0.01_252)] bg-[oklch(0.08_0.007_252)] px-1 py-0.5 text-xs shadow-[inset_0_1px_3px_oklch(0_0_0/0.4)] focus:bg-[oklch(0.1_0.008_252)]"
            : "w-16 border-border px-2 py-1 text-sm"
        }`}
        title={`${TEMPO_BPM_MIN}–${TEMPO_BPM_MAX} BPM`}
      />
      {!inline && (
        <span className="font-led text-[0.65rem] opacity-50">
          Metronome on time controls
        </span>
      )}
    </label>
  );
}
