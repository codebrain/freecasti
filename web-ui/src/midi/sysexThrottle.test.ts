import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { createSysexSendThrottle } from "./sysexThrottle";

describe("createSysexSendThrottle", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("waits min interval before first send", () => {
    const sent: Uint8Array[] = [];
    const throttle = createSysexSendThrottle((b) => sent.push(b), 500);

    throttle.enqueue(new Uint8Array([1]));
    expect(sent).toHaveLength(0);

    vi.advanceTimersByTime(499);
    expect(sent).toHaveLength(0);

    vi.advanceTimersByTime(1);
    expect(sent).toHaveLength(1);
    expect(sent[0][0]).toBe(1);

    throttle.dispose();
  });

  it("coalesces rapid updates into one send with latest bytes", () => {
    const sent: Uint8Array[] = [];
    const throttle = createSysexSendThrottle((b) => sent.push(b), 500);

    throttle.enqueue(new Uint8Array([1]));
    vi.advanceTimersByTime(200);
    throttle.enqueue(new Uint8Array([2]));
    vi.advanceTimersByTime(200);
    throttle.enqueue(new Uint8Array([3]));
    vi.advanceTimersByTime(500);

    expect(sent).toHaveLength(1);
    expect(sent[0][0]).toBe(3);

    throttle.dispose();
  });

  it("limits sustained updates to one send per interval", () => {
    const sent: Uint8Array[] = [];
    let clock = 0;
    const throttle = createSysexSendThrottle((b) => sent.push(b), 500, () => clock);

    throttle.enqueue(new Uint8Array([1]));
    clock = 500;
    vi.advanceTimersByTime(500);
    expect(sent).toHaveLength(1);

    throttle.enqueue(new Uint8Array([2]));
    clock = 600;
    vi.advanceTimersByTime(400);
    expect(sent).toHaveLength(1);

    clock = 1100;
    vi.advanceTimersByTime(100);
    expect(sent).toHaveLength(2);
    expect(sent[1][0]).toBe(2);

    throttle.dispose();
  });
});
