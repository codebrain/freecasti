/**
 * @vitest-environment happy-dom
 */
import { createElement, type ComponentProps } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { describe, expect, it, afterEach, vi } from "vitest";
import { ParamControl } from "./ParamControl";
import type { ControlDef } from "@/spec/controls";

const dialControl: ControlDef = {
  fieldId: "size",
  label: "size",
  parameter: "size",
  encoding: "raw_u8",
  offsets: [0],
  widget: "knob",
  entries: [
    { encoded: 0, label: "0" },
    { encoded: 1, label: "1" },
    { encoded: 2, label: "2" },
  ],
  entryIndex: (enc) => Math.max(0, Math.min(2, enc)),
};

const buttonControl: ControlDef = {
  fieldId: "audio_routing",
  label: "audio routing",
  parameter: "audio routing",
  encoding: "raw_u8",
  offsets: [13],
  widget: "buttons",
  entries: [
    { encoded: 0, label: "Mono L" },
    { encoded: 1, label: "Mono R" },
    { encoded: 2, label: "Stereo" },
  ],
  entryIndex: (enc) => Math.max(0, Math.min(2, enc)),
};

describe("ParamControl disabled wiring", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  it("passes disabled styling through to the dial widget", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ParamControl, {
          control: dialControl,
          encoded: 1,
          disabled: true,
          onChange: () => {},
        }),
      );
    });

    const frame = container.querySelector("[data-param-control]");
    expect(frame?.getAttribute("aria-disabled")).toBe("true");
    expect(frame?.querySelector(".led-text")).toBeNull();
    for (const line of frame?.querySelectorAll("line") ?? []) {
      expect(line.getAttribute("stroke")).not.toBe("var(--color-led)");
    }
  });

  it("shows the red selection ring on the dial when selected", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ParamControl, {
          control: dialControl,
          encoded: 1,
          selected: true,
          onChange: () => {},
          onSelect: () => {},
        }),
      );
    });

    const ring = container.querySelector(
      'circle[stroke="var(--color-primary)"]',
    );
    expect(ring).not.toBeNull();
  });

  it("hides the selection ring when not selected", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    act(() => {
      root.render(
        createElement(ParamControl, {
          control: dialControl,
          encoded: 1,
          selected: false,
          onChange: () => {},
          onSelect: () => {},
        }),
      );
    });

    expect(
      container.querySelector('circle[stroke="var(--color-primary)"]'),
    ).toBeNull();
  });
});

describe("ParamControl selection", () => {
  let container: HTMLDivElement;
  let root: ReturnType<typeof createRoot>;

  afterEach(() => {
    act(() => {
      root.unmount();
    });
    container.remove();
  });

  function renderDial(
    props: Partial<ComponentProps<typeof ParamControl>> = {},
  ) {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    const onSelect = vi.fn();
    const onChange = vi.fn();

    act(() => {
      root.render(
        createElement(ParamControl, {
          control: dialControl,
          encoded: 0,
          onChange,
          onSelect,
          ...props,
        }),
      );
    });

    return {
      onSelect,
      onChange,
      frame: container.querySelector("[data-param-control]") as HTMLElement,
      dialHost: container.querySelector(
        ".flex.flex-col.items-center.gap-2",
      ) as HTMLElement,
    };
  }

  it("calls onSelect when the control is clicked", () => {
    const { frame, onSelect } = renderDial();

    act(() => {
      frame.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });

    expect(onSelect).toHaveBeenCalledTimes(1);
  });

  it("calls onSelect when the dial value changes", () => {
    const { dialHost, onSelect, onChange } = renderDial({ encoded: 0 });

    act(() => {
      dialHost.dispatchEvent(
        new WheelEvent("wheel", { deltaY: -100, bubbles: true }),
      );
    });

    expect(onSelect).toHaveBeenCalledTimes(1);
    expect(onChange).toHaveBeenCalledWith(1);
  });

  it("does not call onSelect when the dial value stays the same", () => {
    const { dialHost, onSelect, onChange } = renderDial({ encoded: 2 });

    act(() => {
      dialHost.dispatchEvent(
        new WheelEvent("wheel", { deltaY: -100, bubbles: true }),
      );
    });

    expect(onChange).not.toHaveBeenCalled();
    expect(onSelect).not.toHaveBeenCalled();
  });

  it("calls onSelect when a button option is clicked", () => {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);

    const onSelect = vi.fn();
    const onChange = vi.fn();

    act(() => {
      root.render(
        createElement(ParamControl, {
          control: buttonControl,
          encoded: 0,
          onChange,
          onSelect,
        }),
      );
    });

    const option = container.querySelector(
      'button[role="radio"][aria-checked="false"]',
    ) as HTMLButtonElement;

    act(() => {
      option.click();
    });

    expect(onSelect).toHaveBeenCalledTimes(1);
    expect(onChange).toHaveBeenCalledWith(1);
  });
});
