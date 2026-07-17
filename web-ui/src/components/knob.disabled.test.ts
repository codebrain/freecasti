/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach } from "vitest";
import { Knob } from "./Knob";

describe("Knob disabled styling", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("renders tick markers in neutral grey when disabled", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(Knob, {
          value: 5,
          min: 0,
          max: 10,
          disabled: true,
          featured: true,
          onChange: () => {},
        }),
      );
    });

    const strokes = [...container.querySelectorAll("line")].map((line) =>
      line.getAttribute("stroke"),
    );
    expect(strokes.length).toBeGreaterThan(0);
    for (const stroke of strokes) {
      expect(stroke).not.toBe("var(--color-led)");
      expect(stroke).not.toBe("var(--color-led-dim)");
    }
    expect(container.querySelector(".led-text")).toBeNull();
    expect(container.querySelector(".control-value-inactive")).not.toBeNull();
  });

  it("keeps the value glowing red when locked and active", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(Knob, {
          value: 5,
          min: 0,
          max: 10,
          locked: true,
          displayValue: "2.4 s",
          onChange: () => {},
        }),
      );
    });

    expect(container.querySelector(".control-value-inactive")).toBeNull();
    expect(container.querySelector(".led-text")).not.toBeNull();
    expect(container.textContent).toContain("2.4 s");
  });

  it("greys the value when locked and disabled", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(Knob, {
          value: 5,
          min: 0,
          max: 10,
          disabled: true,
          locked: true,
          displayValue: "2.4 s",
          onChange: () => {},
        }),
      );
    });

    expect(container.querySelector(".control-value-inactive")).not.toBeNull();
    expect(container.querySelector(".led-text")).toBeNull();
    expect(container.textContent).toContain("2.4 s");
  });
});
