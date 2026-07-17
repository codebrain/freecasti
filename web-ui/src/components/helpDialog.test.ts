/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach } from "vitest";
import { HelpDialog } from "./HelpDialog";

describe("HelpDialog", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("renders nothing when closed", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(createElement(HelpDialog, { open: false, onClose: () => {} }));
    });

    expect(document.querySelector('[role="dialog"]')).toBeNull();
  });

  it("shows help sections when open", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(createElement(HelpDialog, { open: true, onClose: () => {} }));
    });

    const dialog = document.querySelector('[role="dialog"]');
    expect(dialog).not.toBeNull();
    expect(dialog?.textContent).toContain("NonLin bank");
    expect(dialog?.textContent).toContain("MIDI is off");
    expect(dialog?.textContent).toContain("Padlock");
    expect(dialog?.textContent).toContain("Future State Studios accepts no liability");
  });
});
