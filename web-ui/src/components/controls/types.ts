import type { ControlDef } from "@/spec/controls";

/** Shared props for program/system parameter widgets (dial or button list). */
export interface ParamWidgetControlProps {
  control: ControlDef;
  encoded: number;
  onChange: (encoded: number) => void;
  size?: number;
  label?: string;
  featured?: boolean;
  disabled?: boolean;
  selected?: boolean;
  onSelect?: () => void;
  locked?: boolean;
  onToggleLock?: () => void;
  hideLabel?: boolean;
  tempoBpm?: number;
  tempoMode?: boolean;
  onToggleTempoMode?: () => void;
}
