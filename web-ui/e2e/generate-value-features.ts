/**
 * Regenerates `e2e/features/parameter-values/` — one feature file per
 * parameter, exhaustively listing every value the editor may offer. The
 * tables are derived from the same runtime spec the app itself renders
 * (`public/m7-runtime.json`) and formatted with the app's own display rules,
 * so the features pin the exact strings a user must see on any target.
 *
 * Run with: npm run gen:value-features
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  allProgControls,
  buildSystemControls,
  type ControlDef,
} from "@/spec/controls";
import { formatValueLabel } from "@/spec/labels";
import { expandRuntimeBundle } from "@/runtime/expandRuntime";

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(here, "features", "parameter-values");

const runtime = expandRuntimeBundle(
  JSON.parse(
    fs.readFileSync(path.join(here, "..", "public", "m7-runtime.json"), "utf8"),
  ),
);

/** The ordered list of value strings the editor displays for a control. */
function displayedValues(control: ControlDef): string[] {
  const entries =
    control.widget === "buttons"
      ? (control.buttonEntries ?? control.entries)
      : control.entries;
  const labels = entries.map((e) => formatValueLabel(e.label, control.parameter));
  // A stepped walk through the dial observes adjacent identical displays as
  // a single value; collapse them the same way.
  const collapsed = labels.filter((label, i) => i === 0 || label !== labels[i - 1]);
  if (collapsed.length !== labels.length) {
    console.warn(
      `warning: ${control.parameter}: ${labels.length - collapsed.length} adjacent duplicate display value(s) collapsed`,
    );
  }
  return collapsed;
}

function featureFile(control: ControlDef, view: "program" | "system"): string {
  const parameter = control.parameter!;
  const values = displayedValues(control);
  const lines = [
    "# GENERATED FILE — do not edit by hand.",
    "# Regenerate with: npm run gen:value-features (web-ui)",
    "# @slow: walking a whole value table needs more than the default timeout.",
    "@core @parameter-values @slow",
    `Feature: Allowable values for "${parameter}"`,
    `  The device supports a fixed table of ${values.length} steps for`,
    `  "${parameter}". The editor must offer exactly these values, in this`,
    "  order, and nothing else.",
    "",
    `  Scenario: Every value the editor may offer for "${parameter}"`,
    "    Given the editor is started",
  ];
  if (view === "system") {
    lines.push('    And the user opens the "system" view');
  }
  lines.push(`    Then the only values available for "${parameter}" are:`);
  for (const value of values) {
    lines.push(`      | ${value} |`);
  }
  lines.push("");
  return lines.join("\n");
}

fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const targets: { control: ControlDef; view: "program" | "system" }[] = [
  ...allProgControls(runtime.prog).map((control) => ({
    control,
    view: "program" as const,
  })),
  ...buildSystemControls(runtime.system).map((control) => ({
    control,
    view: "system" as const,
  })),
];

for (const { control, view } of targets) {
  const slug = control.parameter!.replace(/\s+/g, "-");
  const file = path.join(outDir, `${slug}.feature`);
  fs.writeFileSync(file, featureFile(control, view));
  console.log(
    `${path.relative(path.join(here, ".."), file)}: ${displayedValues(control).length} values (${view})`,
  );
}
