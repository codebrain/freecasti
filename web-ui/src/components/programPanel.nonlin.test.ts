/**
 * @vitest-environment happy-dom
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach } from "vitest";
import { ProgramPanel } from "@/components/ProgramPanel";
import { applyPreset } from "@/presets/applyPreset";
import {
  algorithmConstraintsFrom,
  isParameterActive,
} from "@/presets/algorithms";
import { groupPresetsByBank, resolveProgramBankIndex } from "@/presets/catalog";
import { expandPresetCatalog } from "@/presets/compact";
import { expandCompactSpec } from "@/spec/compact";
import {
  buildParameterToFieldId,
  buildProgControlGroups,
} from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { PROG_PARAM_ORDER } from "@/spec/param-order";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

function loadRuntimeCatalog() {
  const runtime = JSON.parse(
    fs.readFileSync(path.join(repo, "web-ui/public/m7-runtime.json"), "utf8"),
  );
  return expandPresetCatalog(runtime.presets);
}

function loadCompactProgSpec(): DumpSpec {
  const runtime = JSON.parse(
    fs.readFileSync(path.join(repo, "web-ui/public/m7-runtime.json"), "utf8"),
  );
  return expandCompactSpec(runtime.prog);
}

describe("ProgramPanel NonLin inactive controls", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("marks inactive parameters aria-disabled when NonLin is selected", () => {
    const catalog = loadRuntimeCatalog();
    const banks = groupPresetsByBank(catalog);
    const nonLinIdx = banks.findIndex((b) => b.name === "NonLin");
    const nonLinEntry = banks[nonLinIdx]!.presets[0];
    const spec = loadCompactProgSpec();
    const paramToField = buildParameterToFieldId(spec);
    const state = applyPreset(nonLinEntry, paramToField);
    const groups = buildProgControlGroups(spec);
    const constraints = algorithmConstraintsFrom(catalog);
    const bankIndex = resolveProgramBankIndex(banks, nonLinIdx, state.encoded);
    const isParameterActiveFn = (parameter: string | undefined) =>
      isParameterActive(bankIndex, parameter, constraints);

    expect(isParameterActiveFn("reverb time")).toBe(false);
    expect(isParameterActiveFn("size")).toBe(true);

    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ProgramPanel, {
          groups,
          state,
          variant: "core-only",
          isParameterActive: isParameterActiveFn,
          onChange: () => {},
        }),
      );
    });

    const controls = container.querySelectorAll("[data-param-control]");
    expect(controls.length).toBeGreaterThan(0);

    const disabled = [...controls].filter(
      (el) => el.getAttribute("aria-disabled") === "true",
    );
    const enabled = [...controls].filter(
      (el) => el.getAttribute("aria-disabled") !== "true",
    );

    expect(disabled.length).toBeGreaterThan(0);
    expect(enabled.length).toBeGreaterThan(0);
    expect(disabled.length + enabled.length).toBe(controls.length);
  });

  it("uses neutral grey styling on disabled controls (no red LED ticks or labels)", () => {
    const catalog = loadRuntimeCatalog();
    const banks = groupPresetsByBank(catalog);
    const nonLinIdx = banks.findIndex((b) => b.name === "NonLin");
    const nonLinEntry = banks[nonLinIdx]!.presets[0];
    const spec = loadCompactProgSpec();
    const paramToField = buildParameterToFieldId(spec);
    const state = applyPreset(nonLinEntry, paramToField);
    const groups = buildProgControlGroups(spec);
    const constraints = algorithmConstraintsFrom(catalog);
    const bankIndex = resolveProgramBankIndex(banks, nonLinIdx, state.encoded);
    const isParameterActiveFn = (parameter: string | undefined) =>
      isParameterActive(bankIndex, parameter, constraints);

    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ProgramPanel, {
          groups,
          state,
          variant: "core-only",
          isParameterActive: isParameterActiveFn,
          onChange: () => {},
        }),
      );
    });

    const disabledEl = container.querySelector(
      '[data-param-control][aria-disabled="true"]',
    );
    expect(disabledEl).not.toBeNull();

    for (const line of disabledEl!.querySelectorAll("line")) {
      expect(line.getAttribute("stroke")).not.toBe("var(--color-led)");
      expect(line.getAttribute("stroke")).not.toBe("var(--color-led-dim)");
    }

    expect(disabledEl!.querySelector(".knob-hero-label")).not.toBeNull();
    expect(disabledEl!.querySelector(".param-label-inactive")).not.toBeNull();
    expect(disabledEl!.querySelector(".led-text")).toBeNull();
    expect(disabledEl!.querySelector(".control-value-inactive")).not.toBeNull();
    expect(disabledEl!.querySelector(".knob-hero-label-muted")).toBeNull();
    expect(disabledEl!.className).toContain("opacity-45");
    expect(disabledEl!.className).toContain("cursor-not-allowed");
  });

  it("keeps all core controls active on Halls", () => {
    const catalog = loadRuntimeCatalog();
    const banks = groupPresetsByBank(catalog);
    const hallsIdx = banks.findIndex((b) => b.name === "Halls");
    const hallsEntry = banks[hallsIdx]!.presets[0];
    const spec = loadCompactProgSpec();
    const state = applyPreset(hallsEntry, buildParameterToFieldId(spec));
    const groups = buildProgControlGroups(spec);
    const constraints = algorithmConstraintsFrom(catalog);
    const bankIndex = resolveProgramBankIndex(banks, hallsIdx, state.encoded);
    const isParameterActiveFn = (parameter: string | undefined) =>
      isParameterActive(bankIndex, parameter, constraints);

    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ProgramPanel, {
          groups,
          state,
          variant: "core-only",
          isParameterActive: isParameterActiveFn,
          onChange: () => {},
        }),
      );
    });

    const disabled = container.querySelectorAll(
      '[data-param-control][aria-disabled="true"]',
    );
    expect(disabled.length).toBe(0);
  });
});

describe("NonLin factory preset identity", () => {
  it("sets bank_index 10 and greys out reverb time via UI bank index", () => {
    const catalog = loadRuntimeCatalog();
    const banks = groupPresetsByBank(catalog);
    const nonLinIdx = banks.findIndex((b) => b.name === "NonLin");
    const entry = catalog.presets.find((p) => p.bank === "NonLin")!;
    const spec = loadCompactProgSpec();
    const state = applyPreset(entry, buildParameterToFieldId(spec));
    expect(state.encoded.bank_index).toBe(10);

    const bankIndex = resolveProgramBankIndex(banks, nonLinIdx, {
      bank_index: 0,
    });
    const constraints = algorithmConstraintsFrom(catalog);
    expect(isParameterActive(bankIndex, "reverb time", constraints)).toBe(false);
    expect(isParameterActive(bankIndex, "size", constraints)).toBe(true);

    for (const param of PROG_PARAM_ORDER) {
      const active = isParameterActive(bankIndex, param, constraints);
      if (constraints.nonlin.params.includes(param)) {
        expect(active, param).toBe(true);
      } else {
        expect(active, param).toBe(false);
      }
    }
  });
});
