/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach, vi } from "vitest";
import { AbCompareControls } from "./AbCompareControls";

const tooltips = {
  a: "Slot A (active) — Large Hall · Halls. Preset picks and parameter edits apply here.",
  b: "Switch to slot B — Small Hall · Halls. Compare two presets side by side.",
};

describe("AbCompareControls", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  function renderControls(
    active: "a" | "b",
    onSelect = vi.fn(),
    onSwap = vi.fn(),
  ) {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(AbCompareControls, {
          active,
          tooltips,
          onSelect,
          onSwap,
        }),
      );
    });

    return { onSelect, onSwap };
  }

  function sideButtons() {
    return container.querySelectorAll<HTMLButtonElement>(
      'button[aria-label^="Compare slot"]',
    );
  }

  it("exposes an A/B toggle group with pressed state", () => {
    renderControls("a");

    const group = container.querySelector('[role="group"]');
    expect(group?.getAttribute("aria-label")).toBe("Compare presets A and B");

    const buttons = sideButtons();
    expect(buttons).toHaveLength(2);
    expect(buttons[0]?.textContent).toBe("A");
    expect(buttons[1]?.textContent).toBe("B");
    expect(buttons[0]?.getAttribute("aria-pressed")).toBe("true");
    expect(buttons[1]?.getAttribute("aria-pressed")).toBe("false");
    expect(buttons[0]?.getAttribute("title")).toBeNull();
    expect(buttons[0]?.getAttribute("aria-label")).toBe("Compare slot A");
  });

  it("calls onSelect when the inactive side is clicked", () => {
    const { onSelect } = renderControls("a");

    const buttons = sideButtons();
    act(() => {
      buttons[1]?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });

    expect(onSelect).toHaveBeenCalledTimes(1);
    expect(onSelect).toHaveBeenCalledWith("b");
  });

  it("calls onSwap when the swap button is clicked", () => {
    const { onSwap } = renderControls("a");

    const swap = container.querySelector<HTMLButtonElement>(
      'button[aria-label="Swap slots A and B"]',
    );
    act(() => {
      swap?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });

    expect(onSwap).toHaveBeenCalledTimes(1);
  });
});
