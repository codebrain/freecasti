import type { DumpSpec, SpecField, ValueMapEntry } from "./types";
import { progDescriptions, systemDescriptions } from "./descriptions";

export interface ControlDef {
  fieldId: string;
  label: string;
  parameter?: string;
  description?: string;
  encoding: string;
  offsets: number[];
  entries: ValueMapEntry[];
  widget: "knob" | "buttons";
  /** Entries shown when `widget` is `buttons` (defaults to `entries`). */
  buttonEntries?: ValueMapEntry[];
  /** Index into entries for the current encoded value */
  entryIndex: (encoded: number) => number;
}

export interface ControlGroup {
  title: string;
  controls: ControlDef[];
  subgroups?: ControlGroup[];
}

const PROG_SECTION_PARAMS: {
  title: string;
  parameters?: string[];
  subgroups?: { title: string; parameters: string[] }[];
}[] = [
  {
    title: "Core",
    parameters: [
      "reverb time",
      "size",
      "predelay",
      "diffusion",
      "density",
      "modulation",
    ],
  },
  {
    title: "Reflections",
    parameters: ["early select", "early to reverb mix"],
  },
  {
    title: "Delay",
    parameters: ["delay time", "delay level", "delay modulation"],
  },
  {
    title: "Rolloff",
    parameters: ["rolloff", "early rolloff", "vlf cut"],
  },
  {
    title: "Frequency Dependent Decay Time",
    subgroups: [
      {
        title: "LF RT",
        parameters: ["lf rt crossover", "lf rt multiply"],
      },
      {
        title: "HF RT",
        parameters: ["hf rt crossover", "hf rt multiply"],
      },
    ],
  },
];

const SYSTEM_PARAM_ORDER = [
  "wet gain",
  "dry gain",
  "audio routing",
  "audio format",
  "output level",
  "display level",
  "midi channel",
  "midi bank",
];

/** Parameters rendered as button lists instead of knobs. */
const BUTTON_LIST_PARAMS = new Set([
  "audio routing",
  "audio format",
  "display level",
  "output level",
  "midi bank",
]);

function buttonEntriesFor(
  parameter: string | undefined,
  entries: ValueMapEntry[],
): ValueMapEntry[] | undefined {
  if (parameter === "display level") {
    return entries.filter((e) => e.encoded <= 4);
  }
  return undefined;
}

function widgetFor(parameter: string | undefined): "knob" | "buttons" {
  if (parameter && BUTTON_LIST_PARAMS.has(parameter)) {
    return "buttons";
  }
  return "knob";
}

function isUserControl(field: SpecField): boolean {
  return Boolean(field.value_map?.entries?.length);
}

function buildControl(field: SpecField, descriptions: Map<string, string>): ControlDef {
  const entries = field.value_map!.entries;
  const widget = widgetFor(field.parameter);
  const buttonEntries = buttonEntriesFor(field.parameter, entries);
  return {
    fieldId: field.id,
    label: field.label,
    parameter: field.parameter,
    description: descriptions.get(field.id),
    encoding: field.encoding ?? "raw_u8",
    offsets: field.offsets,
    entries,
    widget,
    buttonEntries,
    entryIndex(encoded: number) {
      const idx = entries.findIndex((e) => e.encoded === encoded);
      return idx >= 0 ? idx : 0;
    },
  };
}

export function buildParameterToFieldId(spec: DumpSpec): Map<string, string> {
  const map = new Map<string, string>();
  for (const field of spec.fields) {
    if (field.parameter) {
      map.set(field.parameter, field.id);
    }
  }
  return map;
}

export function buildProgControlGroups(spec: DumpSpec): ControlGroup[] {
  const byParam = new Map<string, ControlDef>();
  for (const field of spec.fields) {
    if (isUserControl(field) && field.parameter) {
      byParam.set(field.parameter, buildControl(field, progDescriptions));
    }
  }

  const groups: ControlGroup[] = [];
  for (const section of PROG_SECTION_PARAMS) {
    if (section.subgroups) {
      const subgroups: ControlGroup[] = [];
      for (const sub of section.subgroups) {
        const controls = sub.parameters
          .map((p) => byParam.get(p))
          .filter((c): c is ControlDef => c !== undefined);
        if (controls.length) {
          subgroups.push({ title: sub.title, controls });
        }
      }
      if (subgroups.length) {
        groups.push({ title: section.title, controls: [], subgroups });
      }
      continue;
    }
    const controls = (section.parameters ?? [])
      .map((p) => byParam.get(p))
      .filter((c): c is ControlDef => c !== undefined);
    if (controls.length) {
      groups.push({ title: section.title, controls });
    }
  }
  return groups;
}

export function buildSystemControls(spec: DumpSpec): ControlDef[] {
  const byParam = new Map<string, ControlDef>();
  for (const field of spec.fields) {
    if (isUserControl(field) && field.parameter) {
      if (!byParam.has(field.parameter)) {
        byParam.set(field.parameter, buildControl(field, systemDescriptions));
      }
    }
  }
  return SYSTEM_PARAM_ORDER.map((p) => byParam.get(p)).filter(
    (c): c is ControlDef => c !== undefined,
  );
}

export function defaultEncodedState(controls: ControlDef[]): Record<string, number> {
  const state: Record<string, number> = {};
  for (const c of controls) {
    state[c.fieldId] = c.entries[0]?.encoded ?? 0;
  }
  return state;
}

export function allProgControls(spec: DumpSpec): ControlDef[] {
  return buildProgControlGroups(spec).flatMap((g) => [
    ...g.controls,
    ...(g.subgroups?.flatMap((s) => s.controls) ?? []),
  ]);
}
