import { describe, expect, it } from "vitest";
import {
  allProgControls,
  buildProgControlGroups,
  buildSystemControls,
  buildParameterToFieldId,
  defaultEncodedState,
} from "@/spec/controls";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("spec controls", () => {
  const runtime = loadRuntimeFixture();

  it("maps parameters to field ids", () => {
    const map = buildParameterToFieldId(runtime.prog);
    expect(map.get("reverb time")).toBeTruthy();
    expect(map.get("size")).toBeTruthy();
  });

  it("orders program groups with Core first and FDDT subgroup", () => {
    const groups = buildProgControlGroups(runtime.prog);
    expect(groups[0]?.title).toBe("Core");
    const fd = groups.find((g) => g.title.includes("Frequency"));
    expect(fd?.subgroups?.map((s) => s.title)).toEqual(["LF RT", "HF RT"]);
  });

  it("flattens all prog controls for hydrate/serialize", () => {
    const controls = allProgControls(runtime.prog);
    expect(controls.length).toBeGreaterThan(15);
    expect(controls.every((c) => c.entries.length > 0)).toBe(true);
  });

  it("limits display level buttons to encoded <= 4", () => {
    const sysControls = buildSystemControls(runtime.system);
    const display = sysControls.find((c) => c.parameter === "display level")!;
    expect(display.widget).toBe("buttons");
    expect(display.buttonEntries?.length).toBeGreaterThan(0);
    expect(display.buttonEntries?.every((e) => e.encoded <= 4)).toBe(true);
    expect(display.buttonEntries!.length).toBeLessThanOrEqual(display.entries.length);
  });

  it("exposes midi bank as a button list with 14 banks", () => {
    const sysControls = buildSystemControls(runtime.system);
    const midiBank = sysControls.find((c) => c.parameter === "midi bank")!;
    expect(midiBank.widget).toBe("buttons");
    expect(midiBank.entries).toHaveLength(14);
    expect(midiBank.entries[0]?.label).toBe("halls");
    expect(midiBank.entries[13]?.label).toBe("favs");
  });

  it("builds default encoded state from first table entries", () => {
    const sysControls = buildSystemControls(runtime.system);
    const defaults = defaultEncodedState(sysControls);
    for (const control of sysControls) {
      expect(defaults[control.fieldId]).toBe(control.entries[0]?.encoded);
    }
  });
});
