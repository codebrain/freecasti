/**
 * @vitest-environment happy-dom
 */
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { EditableValue } from "./EditableValue";

describe("EditableValue", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("opens an input when the value is clicked", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(EditableValue, {
          displayValue: "Stereo",
          onCommit: () => {},
        }),
      );
    });

    const trigger = container.querySelector("button") as HTMLButtonElement;
    act(() => {
      trigger.click();
    });

    expect(container.querySelector("input")).not.toBeNull();
  });

  it("calls onCommit when editing finishes", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    const onCommit = vi.fn();
    act(() => {
      root.render(
        createElement(EditableValue, {
          displayValue: "Stereo",
          onCommit,
        }),
      );
    });

    const trigger = container.querySelector("button") as HTMLButtonElement;
    act(() => {
      trigger.click();
    });

    const input = container.querySelector("input") as HTMLInputElement;
    act(() => {
      input.blur();
    });

    expect(onCommit).toHaveBeenCalledTimes(1);
  });

  it("does not enter edit mode when disabled", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(EditableValue, {
          displayValue: "Stereo",
          disabled: true,
          onCommit: () => {},
        }),
      );
    });

    expect(container.querySelector("button")).toBeNull();
    expect(container.querySelector("input")).toBeNull();
    expect(container.textContent).toContain("Stereo");
    expect(container.querySelector(".control-value-inactive")).not.toBeNull();
  });

  it("keeps led styling when disabled but not dimmed (locked readout)", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(EditableValue, {
          displayValue: "2.4 s",
          disabled: true,
          dimmed: false,
          onCommit: () => {},
        }),
      );
    });

    expect(container.querySelector(".led-text")).not.toBeNull();
    expect(container.querySelector(".control-value-inactive")).toBeNull();
  });
});
