/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach } from "vitest";
import { ParamLabel } from "./ParamLabel";

describe("ParamLabel disabled styling", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("keeps hero typography classes when disabled", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ParamLabel, {
          label: "Reverb Time",
          disabled: true,
          className: "knob-hero-label label-caps",
        }),
      );
    });

    const labelRoot = container.firstElementChild!;
    expect(labelRoot.classList.contains("knob-hero-label")).toBe(true);
    expect(labelRoot.classList.contains("label-caps")).toBe(true);
    expect(labelRoot.classList.contains("param-label-inactive")).toBe(true);
    expect(labelRoot.classList.contains("knob-hero-label-muted")).toBe(false);
  });

  it("uses the same typography classes for enabled and disabled hero labels", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    const heroClass = "knob-hero-label label-caps";

    act(() => {
      root.render(
        createElement(ParamLabel, {
          label: "Reverb Time",
          disabled: false,
          className: heroClass,
        }),
      );
    });
    const enabledClasses = [...container.firstElementChild!.classList].sort();

    act(() => {
      root.render(
        createElement(ParamLabel, {
          label: "Reverb Time",
          disabled: true,
          className: heroClass,
        }),
      );
    });
    const disabledClasses = [...container.firstElementChild!.classList]
      .filter((c) => c !== "param-label-inactive" && c !== "cursor-not-allowed")
      .sort();

    expect(disabledClasses).toEqual(enabledClasses);
  });
});
