/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach, vi } from "vitest";
import { PresetSummary } from "./PresetSelector";

describe("PresetSummary", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("shows preset identity beside the A/B compare controls", () => {
    const onSelectAb = vi.fn();
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(PresetSummary, {
          programName: "Large Hall",
          bankName: "Halls",
          activeAb: "a",
          abTooltips: {
            a: "Slot A (active) — Large Hall · Halls.",
            b: "Switch to slot B — Large Hall · Halls.",
          },
          onSelectAb,
        }),
      );
    });

    expect(container.textContent).toContain("Large Hall");
    expect(container.textContent).toContain("Halls");

    const buttons = container.querySelectorAll("button");
    expect(buttons).toHaveLength(2);

    act(() => {
      buttons[1]?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });
    expect(onSelectAb).toHaveBeenCalledWith("b");
  });
});
