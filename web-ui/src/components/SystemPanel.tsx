import type { ControlDef } from "@/spec/controls";
import type { ParamChange } from "@/debug/change";
import { buildParamChange } from "@/debug/change";
import { ParamControl } from "./ParamControl";

const SYSTEM_SECTIONS: {
  title: string;
  parameters: string[];
  layout?: "row" | "col";
  span?: "full";
  hideControlLabels?: boolean;
}[] = [
  { title: "Levels", parameters: ["wet gain", "dry gain", "output level"], layout: "row" },
  { title: "Audio", parameters: ["audio routing", "audio format"] },
  { title: "MIDI & Display", parameters: ["midi channel", "display level"] },
  { title: "MIDI Bank", parameters: ["midi bank"], span: "full", hideControlLabels: true },
];

interface SystemPanelProps {
  controls: ControlDef[];
  state: Record<string, number>;
  onChange: (next: Record<string, number>, change: ParamChange) => void;
  selectedFieldId?: string | null;
  onSelectField?: (fieldId: string) => void;
}

export function SystemPanel({
  controls,
  state,
  onChange,
  selectedFieldId = null,
  onSelectField,
}: SystemPanelProps) {
  const controlByField = new Map(controls.map((c) => [c.fieldId, c]));
  const controlByParameter = new Map(
    controls
      .filter((c) => c.parameter)
      .map((c) => [c.parameter!, c] as const),
  );

  const setField = (fieldId: string, encoded: number) => {
    const beforeEncoded = state[fieldId];
    if (beforeEncoded === encoded) return;
    const control = controlByField.get(fieldId);
    if (!control) return;
    onChange(
      { ...state, [fieldId]: encoded },
      buildParamChange(control, beforeEncoded ?? encoded, encoded),
    );
  };

  const renderControl = (control: ControlDef, hideLabel = false) => (
    <ParamControl
      key={control.fieldId}
      control={control}
      encoded={state[control.fieldId] ?? control.entries[0].encoded}
      onChange={(enc) => setField(control.fieldId, enc)}
      size={58}
      selected={selectedFieldId === control.fieldId}
      onSelect={() => onSelectField?.(control.fieldId)}
      hideLabel={hideLabel}
    />
  );

  const sectionContentClass = (
    sectionControls: ControlDef[],
    layout: "row" | "col" = "col",
  ) => {
    const buttonsOnly = sectionControls.every((c) => c.widget === "buttons");
    const knobsOnly = sectionControls.every((c) => c.widget !== "buttons");
    if (buttonsOnly) {
      return "flex flex-col items-center gap-6";
    }
    if (knobsOnly && layout === "row") {
      return "flex flex-row flex-wrap items-start justify-center gap-x-1 gap-y-4";
    }
    if (knobsOnly) {
      return "flex flex-col items-center gap-4";
    }
    return "flex flex-col items-center gap-6";
  };

  const isRowKnobSection = (sectionControls: ControlDef[], layout?: "row" | "col") =>
    layout === "row" && sectionControls.every((c) => c.widget !== "buttons");

  const renderSectionControls = (
    sectionControls: ControlDef[],
    layout: "row" | "col" = "col",
    hideControlLabels = false,
  ) => {
    if (layout === "row") {
      const knobs = sectionControls.filter((c) => c.widget !== "buttons");
      const buttons = sectionControls.filter((c) => c.widget === "buttons");
      if (knobs.length && buttons.length) {
        return (
          <div className="flex w-full flex-col items-center gap-6">
            <div className="flex flex-row flex-wrap items-start justify-center gap-x-1 gap-y-4">
              {knobs.map((control) => (
                <div key={control.fieldId} className="shrink-0">
                  {renderControl(control, hideControlLabels)}
                </div>
              ))}
            </div>
            {buttons.map((control) => (
              <div key={control.fieldId} className="flex w-full justify-center">
                {renderControl(control, hideControlLabels)}
              </div>
            ))}
          </div>
        );
      }
    }

    const rowKnobs = isRowKnobSection(sectionControls, layout);
    return sectionControls.map((control) => (
      <div
        key={control.fieldId}
        className={rowKnobs ? "shrink-0" : "flex w-full justify-center"}
      >
        {renderControl(control, hideControlLabels)}
      </div>
    ));
  };

  return (
    <div className="mx-auto grid max-w-6xl grid-cols-1 gap-6 lg:grid-cols-3 lg:items-stretch">
      {SYSTEM_SECTIONS.map((section) => {
        const sectionControls = section.parameters
          .map((parameter) => controlByParameter.get(parameter))
          .filter((control): control is ControlDef => control !== undefined);
        if (!sectionControls.length) return null;

        return (
          <div
            key={section.title}
            className={`panel-raised flex h-full flex-col rounded-md px-4 py-5 md:px-6${
              section.span === "full" ? " lg:col-span-3" : ""
            }`}
          >
            <div className="label-caps mb-4 text-center">
              {section.title}
              <div className="panel-group-rule" aria-hidden />
            </div>
            <div
              className={`flex flex-1 justify-center ${sectionContentClass(sectionControls, section.layout)}`}
            >
              {renderSectionControls(
                sectionControls,
                section.layout,
                section.hideControlLabels,
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
