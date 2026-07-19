import { describe, expect, it } from "vitest";
import { parseMidiReceive } from "@/app/midiReceive";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";

describe("parseMidiReceive", () => {
  const runtime = loadRuntimeFixture();
  const { banks } = loadPresetCatalogFixture();
  const skeletons = loadSerializeSkeletons();
  const progControls = allProgControls(runtime.prog);
  const sysControls = buildSystemControls(runtime.system);

  it("hydrates program dumps with bank selector indices", () => {
    const parsed = parseMidiReceive(
      skeletons.prog,
      runtime.prog,
      progControls,
      sysControls,
      banks,
    );
    expect(parsed?.family).toBe("prog");
    if (parsed?.family === "prog") {
      expect(parsed.state.programName.length).toBeGreaterThan(0);
      expect(parsed.state.ui).toEqual({ mode: "idle" });
      expect(parsed.bankIdx).toBeGreaterThanOrEqual(0);
    }
  });

  it("hydrates system dumps", () => {
    const parsed = parseMidiReceive(
      skeletons.system,
      runtime.prog,
      progControls,
      sysControls,
      banks,
    );
    expect(parsed?.family).toBe("system");
    if (parsed?.family === "system") {
      expect(Object.keys(parsed.state).length).toBeGreaterThan(0);
    }
  });

  it("returns null for unrelated bytes", () => {
    expect(
      parseMidiReceive(new Uint8Array([0, 1, 2]), runtime.prog, progControls, sysControls, banks),
    ).toBeNull();
  });
});
