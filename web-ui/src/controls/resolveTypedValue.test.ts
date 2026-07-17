import { describe, expect, it } from "vitest";
import { buildSystemControls, buildProgControlGroups } from "@/spec/controls";
import {
  normalizeBareNumeric,
  parseEntryNumeric,
  parseNumericFromUserInput,
  resolveTypedControlValue,
} from "@/controls/resolveTypedValue";
import { formatEarlyLateMixLabel } from "@/spec/labels";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("resolveTypedValue", () => {
  const runtime = loadRuntimeFixture();
  const sysControls = buildSystemControls(runtime.system);
  const progControls = buildProgControlGroups(runtime.prog).flatMap((g) => [
    ...g.controls,
    ...(g.subgroups?.flatMap((s) => s.controls) ?? []),
  ]);

  it("matches enum labels case-insensitively", () => {
    const routing = sysControls.find((c) => c.parameter === "audio routing")!;
    expect(resolveTypedControlValue(routing, "stereo")).toBe(0);
    expect(resolveTypedControlValue(routing, "Mono L")).toBe(1);
    expect(resolveTypedControlValue(routing, "not-a-mode")).toBeNull();
  });

  it("snaps wet gain to the nearest dB step", () => {
    const wet = sysControls.find((c) => c.parameter === "wet gain")!;
    expect(resolveTypedControlValue(wet, "-45 dB")).toBe(31);
    expect(resolveTypedControlValue(wet, "-45")).toBe(31);
    expect(resolveTypedControlValue(wet, "45")).toBe(31);
    expect(resolveTypedControlValue(wet, "-45.3")).toBe(30);
    expect(resolveTypedControlValue(wet, "full")).toBe(121);
    expect(resolveTypedControlValue(wet, "off")).toBe(0);
  });

  it("snaps predelay times without unit suffixes", () => {
    const predelay = progControls.find((c) => c.parameter === "predelay")!;
    expect(resolveTypedControlValue(predelay, "100")).toBe(
      resolveTypedControlValue(predelay, "100 ms"),
    );
    expect(resolveTypedControlValue(predelay, "108")).toBe(
      resolveTypedControlValue(predelay, "108 ms"),
    );
    expect(resolveTypedControlValue(predelay, "9999")).toBe(85);
  });

  it("snaps rolloff in Hz without a unit suffix", () => {
    const rolloff = progControls.find((c) => c.parameter === "rolloff")!;
    expect(resolveTypedControlValue(rolloff, "800")).toBe(
      resolveTypedControlValue(rolloff, "800 Hz"),
    );
    expect(resolveTypedControlValue(rolloff, "12000")).toBe(
      resolveTypedControlValue(rolloff, "12000 Hz"),
    );
  });

  it("snaps output level using bare attenuation magnitudes", () => {
    const output = sysControls.find((c) => c.parameter === "output level")!;
    expect(resolveTypedControlValue(output, "8")).toBe(
      resolveTypedControlValue(output, "-8 dB"),
    );
    expect(resolveTypedControlValue(output, "16")).toBe(
      resolveTypedControlValue(output, "-16 dB"),
    );
  });

  it("snaps reverb time from seconds or milliseconds without units", () => {
    const rt = progControls.find((c) => c.parameter === "reverb time")!;
    expect(resolveTypedControlValue(rt, "2.2")).toBe(
      resolveTypedControlValue(rt, "2.2 s"),
    );
    expect(resolveTypedControlValue(rt, "2200")).toBe(
      resolveTypedControlValue(rt, "2200 ms"),
    );
  });

  it("matches midi bank names", () => {
    const bank = sysControls.find((c) => c.parameter === "midi bank")!;
    expect(resolveTypedControlValue(bank, "halls")).toBe(0);
    expect(resolveTypedControlValue(bank, "nonlin")).toBe(10);
    expect(resolveTypedControlValue(bank, "nope")).toBeNull();
  });

  it("matches early/late mix slash and percent labels", () => {
    const mix = progControls.find((c) => c.parameter === "early to reverb mix")!;
    expect(resolveTypedControlValue(mix, "20/20")).toBe(20);
    expect(resolveTypedControlValue(mix, "20/0")).toBe(40);
    const display = formatEarlyLateMixLabel("10/20");
    expect(display).toBeTruthy();
    expect(resolveTypedControlValue(mix, display!)).toBe(10);
  });

  it("resolves tempo divisions when tempo mode is active", () => {
    const predelay = progControls.find((c) => c.parameter === "predelay")!;
    const resolved = resolveTypedControlValue(predelay, "1/4", {
      tempoActive: true,
      tempoBpm: 120,
    });
    expect(resolved).not.toBeNull();
    expect(
      resolveTypedControlValue(predelay, "500", {
        tempoActive: true,
        tempoBpm: 120,
      }),
    ).toBe(resolveTypedControlValue(predelay, "500 ms"));
  });

  describe("normalizeBareNumeric", () => {
    it("assumes dB attenuation for bare positive gain values", () => {
      expect(normalizeBareNumeric(45, "wet gain")).toBe(-45);
      expect(normalizeBareNumeric(-45, "wet gain")).toBe(-45);
    });

    it("assumes milliseconds for delay-time parameters", () => {
      expect(normalizeBareNumeric(500, "predelay")).toBe(500);
      expect(normalizeBareNumeric(2200, "delay time")).toBe(2200);
    });

    it("assumes Hz for rolloff parameters", () => {
      expect(normalizeBareNumeric(800, "rolloff")).toBe(800);
    });

    it("treats small reverb-time values as seconds and large as ms", () => {
      expect(normalizeBareNumeric(2.2, "reverb time")).toBe(2200);
      expect(normalizeBareNumeric(2200, "reverb time")).toBe(2200);
    });
  });

  it("parseEntryNumeric reads device labels", () => {
    expect(parseEntryNumeric("-45 dB")).toBe(-45);
    expect(parseEntryNumeric("500 ms")).toBe(500);
    expect(parseNumericFromUserInput("2.2", "reverb time")).toBe(2200);
  });
});
