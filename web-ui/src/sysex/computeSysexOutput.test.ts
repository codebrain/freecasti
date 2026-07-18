import { describe, expect, it } from "vitest";
import { commitProgIndividualFieldChange } from "@/prog/applyFieldChange";
import { computeSysexOutput } from "@/sysex/computeSysexOutput";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { hydrateProgramFromBytes, hydrateSystemFromBytes } from "@/sysex/hydrate";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

describe("computeSysexOutput", () => {
  const runtime = loadRuntimeFixture();
  const skeletons = loadSerializeSkeletons();
  const progState = hydrateProgramFromBytes(
    skeletons.prog,
    runtime.prog,
    allProgControls(runtime.prog),
  );
  const sysState = hydrateSystemFromBytes(
    skeletons.system,
    buildSystemControls(runtime.system),
  );

  it("builds valid prog bytes with passing checksum", () => {
    const out = computeSysexOutput(
      progState,
      sysState,
      "prog",
      runtime.prog,
      runtime.system,
      runtime.templates.prog,
      runtime.templates.system,
      runtime.progUi,
    );
    expect(out.progBytes?.length).toBe(157);
    expect(out.progChecksumOk).toBe(true);
    expect(out.activeBytes).toBe(out.progBytes);
    expect(out.activeChecksumOk).toBe(true);
  });

  it("selects system bytes on the system tab", () => {
    const out = computeSysexOutput(
      progState,
      sysState,
      "system",
      runtime.prog,
      runtime.system,
      runtime.templates.prog,
      runtime.templates.system,
    );
    expect(out.sysBytes?.length).toBe(77);
    expect(out.activeBytes).toBe(out.sysBytes);
    expect(out.activeChecksumOk).toBe(out.sysChecksumOk);
  });

  function sysexForProgState(state: typeof progState) {
    return computeSysexOutput(
      state,
      sysState,
      "prog",
      runtime.prog,
      runtime.system,
      runtime.templates.prog,
      runtime.templates.system,
      runtime.progUi,
    );
  }

  it("patches menu UI bytes when a parameter is edited", () => {
    const progUi = runtime.progUi!;
    const idleBytes = sysexForProgState(progState).progBytes!;
    expect(idleBytes[99]).toBe(0);
    expect(idleBytes[147]).toBe(progUi.idle["147"]);

    const size = allProgControls(runtime.prog).find((c) => c.parameter === "size")!;
    const nextEncoded =
      size.entries.find((e) => e.encoded !== progState.encoded[size.fieldId])
        ?.encoded ?? size.entries[1]!.encoded;
    const changed = commitProgIndividualFieldChange(progState, size.fieldId, nextEncoded, size);
    expect(changed.kind).toBe("change");

    const editedBytes = sysexForProgState(
      changed.kind === "change" ? changed.state : progState,
    ).progBytes!;
    expect(editedBytes[92]).toBe(2);
    expect(editedBytes[99]).toBe(1);
    expect(editedBytes[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
    expect(editedBytes[147]).toBe(progUi.by_parameter["size"]!.edit!["147"]);
    expect(editedBytes[147]).not.toBe(idleBytes[147]);
  });

  it("patches browse menu UI bytes when a parameter is selected", () => {
    const progUi = runtime.progUi!;
    const browseState = {
      ...progState,
      ui: { mode: "browse" as const, parameter: "size" },
    };
    const bytes = sysexForProgState(browseState).progBytes!;
    expect(bytes[92]).toBe(2);
    expect(bytes[99]).toBe(1);
    expect(bytes[146]).toBe(progUi.by_parameter["size"]!.browse!["146"]);
    expect(bytes[147]).toBe(progUi.by_parameter["size"]!.browse!["147"]);
  });

  it("patches reverb time menu cursor when index 0 matches idle", () => {
    const progUi = runtime.progUi!;
    const reverb = allProgControls(runtime.prog).find(
      (c) => c.parameter === "reverb time",
    )!;
    const nextEncoded =
      reverb.entries.find((e) => e.encoded !== progState.encoded[reverb.fieldId])
        ?.encoded ?? reverb.entries[1]!.encoded;
    const changed = commitProgIndividualFieldChange(
      progState,
      reverb.fieldId,
      nextEncoded,
      reverb,
    );
    expect(changed.kind).toBe("change");

    const editedBytes = sysexForProgState(
      changed.kind === "change" ? changed.state : progState,
    ).progBytes!;
    expect(editedBytes[98]).toBe(0);
    expect(editedBytes[99]).toBe(0);
    expect(editedBytes[146]).toBe(progUi.by_parameter["reverb time"]!.edit!["146"]);
    expect(editedBytes[147]).toBe(progUi.by_parameter["reverb time"]!.edit!["147"]);
    expect(editedBytes[146]).not.toBe(progUi.idle["146"]);
  });

  it("returns null bytes when templates are missing", () => {
    const out = computeSysexOutput(
      progState,
      sysState,
      "prog",
      runtime.prog,
      runtime.system,
      null,
      null,
    );
    expect(out.progBytes).toBeNull();
    expect(out.progChecksumOk).toBe(false);
  });
});
