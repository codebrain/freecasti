/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach, vi } from "vitest";
import { AppHeaderToolbar } from "./AppHeaderToolbar";

describe("AppHeaderToolbar", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("renders segmented tabs and utility buttons with pressed states", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(AppHeaderToolbar, {
          activeTab: "prog",
          onTabChange: vi.fn(),
          tempoBpm: 120,
          onTempoBpmChange: vi.fn(),
          onHelpOpen: vi.fn(),
          debugOpen: true,
          onDebugToggle: vi.fn(),
        }),
      );
    });

    const progTab = container.querySelector("#header-tab-prog");
    const systemTab = container.querySelector("#header-tab-system");
    expect(progTab?.getAttribute("aria-selected")).toBe("true");
    expect(systemTab?.getAttribute("aria-selected")).toBe("false");
    expect(progTab?.className).toContain("color-led");
    expect(systemTab?.className).not.toContain("color-led");

    const debugBtn = [...container.querySelectorAll("button")].find(
      (btn) => btn.textContent === "Debug",
    );
    expect(debugBtn?.getAttribute("aria-pressed")).toBe("true");
    expect(debugBtn?.className).toContain("color-led");
  });
});
