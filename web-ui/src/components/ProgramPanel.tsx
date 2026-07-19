import type { ReactNode } from "react";
import type { ControlDef, ControlGroup } from "@/spec/controls";

import type { ParamChange } from "@/debug/change";

import { commitProgIndividualFieldChange } from "@/prog/applyFieldChange";
import {
  delayControlLabel,
  partitionProgGroups,
  shortSubgroupLabel,
} from "@/prog/layoutLabels";

import { displayParameterLabel } from "@/spec/labels";

import type { ProgSerializeState } from "@/sysex/serialize";

import { ParamControl } from "./ParamControl";



interface ProgramPanelProps {

  groups: ControlGroup[];

  state: ProgSerializeState;

  onChange: (next: ProgSerializeState, change: ParamChange) => void;

  isParameterActive?: (parameter: string | undefined) => boolean;

  variant?: "all" | "core-only" | "rest-only";

  selectedFieldId?: string | null;

  onSelectField?: (fieldId: string) => void;

  lockedFieldIds?: ReadonlySet<string>;

  onToggleFieldLock?: (fieldId: string) => void;

  tempoBpm?: number;

  tempoModeFields?: ReadonlySet<string>;

  onToggleTempoMode?: (fieldId: string) => void;

  /** Rendered beside Frequency Dependent Decay Time (rest / all variants). */
  sidePanel?: ReactNode;

}



export function ProgramPanel({

  groups,

  state,

  onChange,

  isParameterActive = () => true,

  variant = "all",

  selectedFieldId = null,

  onSelectField,

  lockedFieldIds = new Set(),

  onToggleFieldLock,

  tempoBpm = 120,

  tempoModeFields = new Set(),

  onToggleTempoMode,

  sidePanel,

}: ProgramPanelProps) {

  const controlByField = new Map<string, ControlDef>();

  for (const group of groups) {

    for (const control of group.controls) {

      controlByField.set(control.fieldId, control);

    }

    for (const sub of group.subgroups ?? []) {

      for (const control of sub.controls) {

        controlByField.set(control.fieldId, control);

      }

    }

  }



  const setField = (fieldId: string, encoded: number) => {
    const result = commitProgIndividualFieldChange(
      state,
      fieldId,
      encoded,
      controlByField.get(fieldId),
      {
        isParameterActive,
        tempoModeFields,
        tempoBpm,
      },
    );

    if (result.kind === "change") {

      onChange(result.state, result.change);

    }

  };



  const tempoProps = (fieldId: string) => ({

    tempoBpm,

    tempoMode: tempoModeFields.has(fieldId),

    onToggleTempoMode: onToggleTempoMode

      ? () => onToggleTempoMode(fieldId)

      : undefined,

  });



  const renderControls = (

    controls: ControlDef[],

    size = 48,

    options?: { label?: (control: ControlDef) => string; featured?: boolean },

  ) => (

    <div
      className={`flex justify-center gap-x-2.5 gap-y-3 ${
        controls.length <= 3 ? "flex-nowrap" : "flex-wrap"
      }`}
    >

      {controls.map((c) => (

        <ParamControl

          key={c.fieldId}

          control={c}

          encoded={state.encoded[c.fieldId] ?? c.entries[0].encoded}

          onChange={(enc) => setField(c.fieldId, enc)}

          size={size}

          label={options?.label?.(c)}

          featured={options?.featured}

          disabled={!isParameterActive(c.parameter)}

          selected={selectedFieldId === c.fieldId}

          onSelect={() => onSelectField?.(c.fieldId)}

          locked={lockedFieldIds.has(c.fieldId)}

          onToggleLock={() => onToggleFieldLock?.(c.fieldId)}

          {...tempoProps(c.fieldId)}

        />

      ))}

    </div>

  );



  const renderCore = (controls: ControlDef[]) => {

    const reverbTime = controls.find((c) => c.parameter === "reverb time");

    const others = controls.filter((c) => c.parameter !== "reverb time");



    return (

      <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-center sm:justify-center">

        {reverbTime && (

          <div className="flex shrink-0 flex-col items-center sm:pr-6">

            <ParamControl

              control={reverbTime}

              encoded={

                state.encoded[reverbTime.fieldId] ?? reverbTime.entries[0].encoded

              }

              onChange={(enc) => setField(reverbTime.fieldId, enc)}

              size={112}

              featured

              disabled={!isParameterActive(reverbTime.parameter)}

              selected={selectedFieldId === reverbTime.fieldId}

              onSelect={() => onSelectField?.(reverbTime.fieldId)}

              locked={lockedFieldIds.has(reverbTime.fieldId)}

              onToggleLock={() => onToggleFieldLock?.(reverbTime.fieldId)}

              {...tempoProps(reverbTime.fieldId)}

            />

          </div>

        )}

        {renderControls(others, 48)}

      </div>

    );

  };



  const renderGroup = (
    group: ControlGroup,
    options?: { wide?: boolean },
  ) => (
    <div
      key={group.title}
      className={`panel-raised flex h-full flex-col rounded-md px-3 py-5 ${
        options?.wide && group.subgroups?.length ? "lg:col-span-2" : ""
      }`}
    >

      <div className="label-caps mb-4 text-center">
        {displayParameterLabel(undefined, group.title)}
        <div className="panel-group-rule" aria-hidden />
      </div>

      <div className="flex flex-1 flex-col justify-center">

      {group.subgroups ? (

        <div className="grid grid-cols-1 items-stretch gap-6 sm:grid-cols-2">

          {group.subgroups.map((sub) => (

            <div key={sub.title} className="flex flex-col justify-center">

              <div className="label-caps mb-3 text-center text-[0.6rem] opacity-90">

                {sub.title}

              </div>

              {renderControls(sub.controls, 48, {

                label: (c) => shortSubgroupLabel(sub.title, c.label),

              })}

            </div>

          ))}

        </div>

      ) : (

        renderControls(group.controls, 48, {

          label:

            group.title === "Delay"

              ? (c) => delayControlLabel(c.label)

              : undefined,

        })

      )}

      </div>

    </div>

  );



  const { core, trio, fddt, remainder } = partitionProgGroups(groups);



  const showCore = variant === "all" || variant === "core-only";

  const showRest = variant === "all" || variant === "rest-only";



  return (

    <div
      className={
        variant === "core-only"
          ? "flex min-h-0 flex-1 flex-col"
          : variant === "all"
            ? "space-y-8"
            : ""
      }
    >

      {showCore && core && (

        <div className="panel-raised flex flex-1 flex-col rounded-md px-4 py-5 md:px-6">

          <div className="flex flex-1 flex-col justify-center">
            {renderCore(core.controls)}
          </div>

        </div>

      )}



      {showRest && (

        <div className="space-y-6">

          {trio.length > 0 && (

            <div className="grid grid-cols-1 items-stretch gap-6 md:grid-cols-3">

              {trio.map((group) => renderGroup(group))}

            </div>

          )}

          {remainder.length > 0 && (
            <div className="grid grid-cols-1 items-stretch gap-6 lg:grid-cols-2">
              {remainder.map((group) => renderGroup(group, { wide: true }))}
            </div>
          )}

          {(fddt || sidePanel) && (
            <div className="grid grid-cols-1 items-stretch gap-6 lg:grid-cols-2">
              {fddt && renderGroup(fddt)}
              {sidePanel}
            </div>
          )}

        </div>

      )}

    </div>

  );

}


