import { ControlSelectFrame } from "@/components/ControlSelectFrame";
import { ParamButtonControl } from "./ParamButtonControl";
import { ParamDialControl } from "./ParamDialControl";
import type { ParamWidgetControlProps } from "./types";

export type ParamControlProps = ParamWidgetControlProps;

/** Routes to dial or button control based on spec widget type. */
export function ParamControl({
  control,
  selected = false,
  disabled = false,
  onSelect,
  ...widgetProps
}: ParamControlProps) {
  const widget =
    control.widget === "buttons" ? (
      <ParamButtonControl
        control={control}
        disabled={disabled}
        selected={selected}
        {...widgetProps}
      />
    ) : (
      <ParamDialControl
        control={control}
        disabled={disabled}
        selected={selected}
        onSelect={onSelect}
        {...widgetProps}
      />
    );

  return (
    <ControlSelectFrame
      selected={selected}
      disabled={disabled}
      onSelect={onSelect ?? (() => {})}
    >
      {widget}
    </ControlSelectFrame>
  );
}
