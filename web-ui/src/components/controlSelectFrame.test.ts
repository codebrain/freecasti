/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach, vi } from "vitest";
import { ControlSelectFrame } from "./ControlSelectFrame";

describe("ControlSelectFrame", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  function renderFrame(disabled: boolean, onSelect = vi.fn()) {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(
          ControlSelectFrame,
          { selected: false, disabled, onSelect },
          "child",
        ),
      );
    });

    const frame = container.querySelector("[data-param-control]") as HTMLElement;
    return { frame, onSelect };
  }

  it("marks disabled controls inert and skips selection", () => {
    const { frame, onSelect } = renderFrame(true);

    expect(frame.getAttribute("aria-disabled")).toBe("true");
    expect(frame.tabIndex).toBe(-1);
    expect(frame.className).toContain("opacity-45");
    expect(frame.className).toContain("cursor-not-allowed");

    act(() => {
      frame.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      frame.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
    });

    expect(onSelect).not.toHaveBeenCalled();
  });

  it("selects on click and keyboard when enabled", () => {
    const { frame, onSelect } = renderFrame(false);

    expect(frame.getAttribute("aria-disabled")).toBeNull();
    expect(frame.tabIndex).toBe(0);

    act(() => {
      frame.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });
    expect(onSelect).toHaveBeenCalledTimes(1);

    act(() => {
      frame.dispatchEvent(new KeyboardEvent("keydown", { key: " ", bubbles: true }));
    });
    expect(onSelect).toHaveBeenCalledTimes(2);
  });
});
