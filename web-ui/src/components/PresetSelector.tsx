import { useLayoutEffect, useRef, useState } from "react";
import type { BankInfo } from "@/presets/types";

import type { AbSide } from "@/presets/progAbSlot";
import { AbCompareControls } from "@/components/AbCompareControls";

interface PresetSelectorProps {
  banks: BankInfo[];
  bankIndex: number;
  loadedBankIndex: number;
  loadedProgramSlot: number;
  onBankChange: (bankIdx: number) => void;
  onPresetChange: (slot: number) => void;
}

function LedDot({ active }: { active: boolean }) {
  return (
    <span
      className={`mt-1 h-2 w-2 shrink-0 rounded-full transition-all ${
        active
          ? "bg-[color:var(--color-led)] shadow-[0_0_10px_var(--color-led),0_0_3px_var(--color-led),0_0_20px_oklch(0.62_0.24_27/0.35)]"
          : "bg-[color:var(--color-led-dim)] opacity-30"
      }`}
      aria-hidden
    />
  );
}

function listItemClass(selected: boolean) {
  return `preset-list-item ${selected ? "preset-list-item--selected" : ""}`;
}

const listPanelClass = "panel-recess space-y-1 rounded-md p-1.5";

export function PresetSummary({
  programName,
  bankName,
  activeAb,
  abTooltips,
  onSelectAb,
}: {
  programName: string;
  bankName: string | undefined;
  activeAb: AbSide;
  abTooltips: Record<AbSide, string>;
  onSelectAb: (side: AbSide) => void;
}) {
  return (
    <div className="flex items-end justify-between gap-4 px-2 md:px-4">
      <div className="flex min-w-0 flex-wrap items-end gap-x-3 gap-y-1">
        <h2 className="led-text min-w-0 break-words text-2xl leading-none md:text-3xl">
          {programName}
        </h2>
        <span className="shrink-0 pb-0.5 font-led text-xs tracking-wide opacity-60 md:text-sm">
          {bankName ?? "—"}
        </span>
      </div>
      <AbCompareControls active={activeAb} tooltips={abTooltips} onSelect={onSelectAb} />
    </div>
  );
}

export function PresetSelector({
  banks,
  bankIndex,
  loadedBankIndex,
  loadedProgramSlot,
  onBankChange,
  onPresetChange,
}: PresetSelectorProps) {
  const activeBank = banks[bankIndex];
  const programs = activeBank?.presets ?? [];
  const bankListRef = useRef<HTMLDivElement>(null);
  const [bankListHeight, setBankListHeight] = useState<number | null>(null);

  useLayoutEffect(() => {
    const el = bankListRef.current;
    if (!el) return;

    const update = () => setBankListHeight(el.offsetHeight);
    update();

    const observer = new ResizeObserver(update);
    observer.observe(el);
    return () => observer.disconnect();
  }, [banks]);

  return (
    <div className="panel-raised flex h-full flex-col overflow-hidden rounded-md p-3">
      <div className="grid min-h-0 flex-1 grid-cols-2 gap-2 items-start sm:gap-3">
        <div className="flex flex-col">
          <div className="label-caps mb-2 px-1 text-[0.6rem]">Bank</div>
          <div ref={bankListRef} className={listPanelClass} role="listbox" aria-label="Preset banks">
            {banks.map((bank, bankIdx) => {
              const selected = bankIdx === bankIndex;
              return (
                <button
                  key={bank.name}
                  type="button"
                  role="option"
                  aria-selected={selected}
                  className={listItemClass(selected)}
                  onClick={() => onBankChange(bankIdx)}
                >
                  <LedDot active={selected} />
                  <span className="flex min-w-0 flex-1 items-baseline justify-between gap-2 font-medium font-led tracking-wide">
                    <span className="min-w-0 break-words">{bank.name}</span>
                    <span className="shrink-0 tabular-nums opacity-60">{bank.presets.length}</span>
                  </span>
                </button>
              );
            })}
          </div>
        </div>
        <div className="flex min-h-0 flex-col">
          <div className="label-caps mb-2 px-1 text-[0.6rem]">Program</div>
          <div
            className={`${listPanelClass} preset-list-scroll overflow-y-auto overflow-x-hidden`}
            style={bankListHeight != null ? { height: bankListHeight } : undefined}
            role="listbox"
            aria-label={`Programs in ${activeBank?.name ?? "bank"}`}
          >
            {programs.map((preset) => {
              const selected =
                activeBank?.bankIndex === loadedBankIndex &&
                preset.program_slot === loadedProgramSlot;
              return (
                <button
                  key={`${activeBank?.name}-${preset.program_slot}`}
                  type="button"
                  role="option"
                  aria-selected={selected}
                  className={listItemClass(selected)}
                  onClick={() => onPresetChange(preset.program_slot)}
                >
                  <LedDot active={selected} />
                  <span className="min-w-0 break-words font-medium font-led tracking-wide">
                    {preset.preset}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
