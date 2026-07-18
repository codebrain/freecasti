/**
 * @vitest-environment happy-dom
 */
import { describe, expect, it } from "vitest";
import {
  clampSendOnChangeThrottleMs,
  commitSendOnChangeThrottleDraft,
  readStoredSendOnChangeThrottleMs,
  SEND_ON_CHANGE_THROTTLE_MS_DEFAULT,
  SEND_ON_CHANGE_THROTTLE_MS_MAX,
} from "./sendOnChangeThrottle";

describe("sendOnChangeThrottle", () => {
  it("clamps throttle values", () => {
    expect(clampSendOnChangeThrottleMs(-1)).toBe(0);
    expect(clampSendOnChangeThrottleMs(500)).toBe(500);
    expect(clampSendOnChangeThrottleMs(99_999)).toBe(
      SEND_ON_CHANGE_THROTTLE_MS_MAX,
    );
  });

  it("commits drafts with fallback", () => {
    expect(commitSendOnChangeThrottleDraft("", 500)).toBe(500);
    expect(commitSendOnChangeThrottleDraft("250", 500)).toBe(250);
    expect(commitSendOnChangeThrottleDraft("abc", 500)).toBe(500);
  });

  it("reads stored throttle from localStorage", () => {
    localStorage.setItem("m7.midi.sendOnChangeThrottleMs", "750");
    expect(readStoredSendOnChangeThrottleMs()).toBe(750);
    localStorage.removeItem("m7.midi.sendOnChangeThrottleMs");
    expect(readStoredSendOnChangeThrottleMs()).toBe(SEND_ON_CHANGE_THROTTLE_MS_DEFAULT);
    expect(SEND_ON_CHANGE_THROTTLE_MS_DEFAULT).toBe(15);
  });
});
