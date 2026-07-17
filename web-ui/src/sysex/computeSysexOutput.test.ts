import { describe, expect, it } from "vitest";
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
