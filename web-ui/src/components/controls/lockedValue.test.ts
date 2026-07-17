/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { afterEach, describe, expect, it } from "vitest";
import { LockedValue } from "./LockedValue";

describe("LockedValue", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("shows a glowing red value when active", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(LockedValue, {
          valueLabel: "Stereo",
        }),
      );
    });

    expect(container.querySelector(".led-text")).not.toBeNull();
    expect(container.querySelector(".control-value-inactive")).toBeNull();
  });

  it("shows a grey value when disabled", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(LockedValue, {
          valueLabel: "Stereo",
          disabled: true,
        }),
      );
    });

    expect(container.querySelector(".control-value-inactive")).not.toBeNull();
    expect(container.querySelector(".led-text")).toBeNull();
    expect(container.textContent).toContain("Stereo");
  });
});
