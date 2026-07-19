import type { ControlGroup } from "@/spec/controls";

export const TRIO_GROUP_TITLES = ["Reflections", "Rolloff", "Delay"] as const;

export const FDDT_GROUP_TITLE = "Frequency Dependent Decay Time";

export type TrioGroupTitle = (typeof TRIO_GROUP_TITLES)[number];

/** Strip a subgroup prefix from a control label (e.g. "LF RT crossover" → "crossover"). */
export function shortSubgroupLabel(subgroupTitle: string, label: string): string {
  const escaped = subgroupTitle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return label.replace(new RegExp(`^${escaped}\\s+`, "i"), "");
}

/** Shorten delay parameter labels for the compact Delay panel. */
export function delayControlLabel(label: string): string {
  const short = label.replace(/^delay /i, "");
  return short === "modulation" ? "MOD" : short;
}

export interface PartitionedProgGroups {
  core: ControlGroup | undefined;
  trio: ControlGroup[];
  fddt: ControlGroup | undefined;
  remainder: ControlGroup[];
}

export function partitionProgGroups(groups: ControlGroup[]): PartitionedProgGroups {
  const core = groups.find((g) => g.title === "Core");
  const rest = groups.filter((g) => g.title !== "Core");
  const trio = TRIO_GROUP_TITLES.map((title) =>
    rest.find((g) => g.title === title),
  ).filter((g): g is ControlGroup => g !== undefined);
  const fddt = rest.find((g) => g.title === FDDT_GROUP_TITLE);
  const remainder = rest.filter(
    (g) =>
      !TRIO_GROUP_TITLES.includes(g.title as TrioGroupTitle) &&
      g.title !== FDDT_GROUP_TITLE,
  );
  return { core, trio, fddt, remainder };
}
