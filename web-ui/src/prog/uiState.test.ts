import { describe, expect, it } from "vitest";
import {
  applyProgUiBytes,
  decodeProgUiFromBytes,
  defaultProgUiState,
  withProgUiIdle,
} from "@/prog/uiState";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { loadMenuSyx } from "@/test/menuSyx";

describe("prog uiState", () => {
  const runtime = loadRuntimeFixture();
  const progUi = runtime.progUi!;

  it("exposes idle bytes from no menu capture", () => {
    expect(progUi.idle["92"]).toBe(0);
    expect(progUi.idle["147"]).toBe(12);
    const noMenu = loadMenuSyx("no menu");
    expect(noMenu[92]).toBe(progUi.idle["92"]);
    expect(noMenu[147]).toBe(progUi.idle["147"]);
  });

  it("maps size to menu index 1 in browse mode", () => {
    const buf = new Uint8Array(157);
    applyProgUiBytes(
      buf,
      { mode: "browse", parameter: "size" },
      progUi,
    );
    expect(buf[92]).toBe(2);
    expect(buf[98]).toBe(0);
    expect(buf[99]).toBe(1);
    expect(buf[146]).toBe(progUi.by_parameter["size"]!.browse!["146"]);
    expect(buf[147]).toBe(progUi.by_parameter["size"]!.browse!["147"]);
  });

  it("maps size to menu index 1 in edit mode", () => {
    const buf = new Uint8Array(157);
    applyProgUiBytes(
      buf,
      { mode: "edit", parameter: "size" },
      progUi,
    );
    expect(buf[92]).toBe(2);
    expect(buf[98]).toBe(0);
    expect(buf[99]).toBe(1);
    expect(buf[146]).toBe(progUi.by_parameter["size"]!.edit!["146"]);
  });

  it("writes idle bytes for idle ui state", () => {
    const buf = new Uint8Array(157);
    applyProgUiBytes(buf, defaultProgUiState(), progUi);
    expect(buf[92]).toBe(0);
    expect(buf[98]).toBe(0);
    expect(buf[99]).toBe(0);
    expect(buf[146]).toBe(1);
    expect(buf[147]).toBe(12);
  });

  it("decodes edit mode when menu flag stays highlighted", () => {
    const buf = new Uint8Array(157);
    applyProgUiBytes(buf, { mode: "edit", parameter: "size" }, progUi);
    expect(buf[92]).toBe(2);
    expect(decodeProgUiFromBytes(buf, progUi)).toEqual({
      mode: "edit",
      parameter: "size",
    });
  });

  it("decodes idle vs browse reverb time from hardware captures", () => {
    const idle = decodeProgUiFromBytes(loadMenuSyx("no menu"), progUi);
    expect(idle).toEqual({ mode: "idle" });

    const reverb = decodeProgUiFromBytes(loadMenuSyx("reverb time"), progUi);
    expect(reverb).toEqual({ mode: "browse", parameter: "reverb time" });
  });

  it("withProgUiIdle replaces browse or edit UI", () => {
    const base = {
      programName: "Test",
      encoded: {},
      ui: { mode: "edit" as const, parameter: "size" },
    };
    expect(withProgUiIdle(base).ui).toEqual({ mode: "idle" });
  });
});
