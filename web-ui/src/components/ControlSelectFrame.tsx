import type { ReactNode } from "react";
import { controlSelectFrameClass } from "@/components/controlFrame";

interface ControlSelectFrameProps {
  selected: boolean;
  disabled?: boolean;
  onSelect: () => void;
  children: ReactNode;
}

export function ControlSelectFrame({
  selected: _selected,
  disabled = false,
  onSelect,
  children,
}: ControlSelectFrameProps) {
  return (
    <div
      data-param-control=""
      aria-disabled={disabled || undefined}
      tabIndex={disabled ? -1 : 0}
      onClick={(e) => {
        if (disabled) return;
        e.stopPropagation();
        onSelect();
      }}
      onKeyDown={(e) => {
        if (disabled) return;
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelect();
        }
      }}
      className={controlSelectFrameClass(disabled)}
    >
      {children}
    </div>
  );
}
