import type { ReactNode } from "react";
import { ControlTooltip } from "@/components/ControlTooltip";
import { TempoInput } from "@/components/TempoInput";
import type { ActiveTab } from "@/hooks/useSysexOutput";
import {
  appHeaderClass,
  toolbarBpmShellClass,
  toolbarButtonClass,
  toolbarSegmentButtonClass,
  toolbarSegmentTrackClass,
} from "@/components/toolbarButtons";

interface AppHeaderToolbarProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  tempoBpm: number;
  onTempoBpmChange: (bpm: number) => void;
  onHelpOpen: () => void;
  debugOpen: boolean;
  onDebugToggle: () => void;
}

export function AppHeaderBar({ children }: { children: ReactNode }) {
  return <header className={appHeaderClass}>{children}</header>;
}

export function AppHeaderToolbar({
  activeTab,
  onTabChange,
  tempoBpm,
  onTempoBpmChange,
  onHelpOpen,
  debugOpen,
  onDebugToggle,
}: AppHeaderToolbarProps) {
  return (
    <div className="flex flex-wrap items-center gap-2.5 sm:gap-3">
      <div
        className={toolbarSegmentTrackClass}
        role="tablist"
        aria-label="Editor section"
      >
        <ControlTooltip
          placement="bottom"
          description="Program — reverb, reflections, delay, and crossover parameters for the active preset."
        >
          <button
            type="button"
            role="tab"
            id="header-tab-prog"
            aria-selected={activeTab === "prog"}
            aria-controls="editor-panel"
            className={toolbarSegmentButtonClass(activeTab === "prog", "start")}
            onClick={() => onTabChange("prog")}
          >
            Program
          </button>
        </ControlTooltip>
        <ControlTooltip
          placement="bottom"
          description="System — MIDI channel and bank, wet/dry levels, audio routing, and display format."
        >
          <button
            type="button"
            role="tab"
            id="header-tab-system"
            aria-selected={activeTab === "system"}
            aria-controls="editor-panel"
            className={toolbarSegmentButtonClass(activeTab === "system", "end")}
            onClick={() => onTabChange("system")}
          >
            System
          </button>
        </ControlTooltip>
      </div>

      <ControlTooltip
        placement="bottom"
        description="Master tempo for metronome sync on predelay, reverb time, and delay time."
      >
        <div className={toolbarBpmShellClass}>
          <TempoInput
            variant="inline"
            bpm={tempoBpm}
            onBpmChange={onTempoBpmChange}
          />
        </div>
      </ControlTooltip>

      <div className="flex items-center gap-1.5">
        <ControlTooltip
          placement="bottom"
          description="How to use the editor — presets, controls, MIDI, tempo, and limitations."
        >
          <button
            type="button"
            className={toolbarButtonClass(false)}
            onClick={onHelpOpen}
          >
            Help
          </button>
        </ControlTooltip>
        <ControlTooltip
          placement="bottom"
          description="SysEx debug panel — hex dump, structure validation, checksum, MIDI log, and timing discrepancies."
        >
          <button
            type="button"
            className={toolbarButtonClass(debugOpen)}
            aria-pressed={debugOpen}
            onClick={onDebugToggle}
          >
            Debug
          </button>
        </ControlTooltip>
      </div>
    </div>
  );
}
