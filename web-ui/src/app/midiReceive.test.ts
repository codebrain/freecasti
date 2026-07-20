import { describe, expect, it } from "vitest";
import { parseMidiReceive } from "@/app/midiReceive";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadPresetCatalogFixture } from "@/test/presetFixtures";
import { readSysexDump } from "@/test/corpusSysex";
import type { RegBlobLayout } from "@/sysex/registerBasisBlob";

describe("parseMidiReceive", () => {
  const runtime = loadRuntimeFixture();
  const { banks } = loadPresetCatalogFixture();
  const skeletons = loadSerializeSkeletons();
  const progControls = allProgControls(runtime.prog);
  const sysControls = buildSystemControls(runtime.system);
  const regBlob = runtime.regBlob as RegBlobLayout;

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

  it("uses stored register settings when the dump has a register basis frame", () => {
    // Payload carries an unstored 5.0 s reverb-time edit (encoded 76); the
    // blob holds the stored register value (encoded 10).
    const raw = readSysexDump(
      "prog/edit/registers/samples/charset-b1s1-rt5s-unstored-edit.syx",
    );
    const parsed = parseMidiReceive(
      raw,
      runtime.prog,
      progControls,
      sysControls,
      banks,
      regBlob,
    );
    expect(parsed?.family).toBe("prog");
    if (parsed?.family === "prog") {
      expect(parsed.state.encoded.reverb_time).toBe(10);
    }

    // Without the blob layout the live payload wins.
    const withoutLayout = parseMidiReceive(
      raw,
      runtime.prog,
      progControls,
      sysControls,
      banks,
    );
    if (withoutLayout?.family === "prog") {
      expect(withoutLayout.state.encoded.reverb_time).toBe(76);
    }
  });

  it("leaves factory dumps untouched by the register basis layout", () => {
    const withLayout = parseMidiReceive(
      skeletons.prog,
      runtime.prog,
      progControls,
      sysControls,
      banks,
      regBlob,
    );
    const withoutLayout = parseMidiReceive(
      skeletons.prog,
      runtime.prog,
      progControls,
      sysControls,
      banks,
    );
    expect(withLayout).toEqual(withoutLayout);
  });

  it("returns null for unrelated bytes", () => {
    expect(
      parseMidiReceive(new Uint8Array([0, 1, 2]), runtime.prog, progControls, sysControls, banks),
    ).toBeNull();
  });
});
