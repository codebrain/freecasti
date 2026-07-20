import { expect, type Page } from "@playwright/test";
import type { MidiDriver } from "../midiDriver";
import {
  FAKE_INPUT_ID,
  FAKE_OUTPUT_ID,
  installFakeWebMidi,
  removeWebMidiSupport,
} from "./fakeWebMidi";

interface FakeMidiHandle {
  sent: number[][];
  receive(bytes: number[]): void;
  clear(): void;
}

declare global {
  interface Window {
    __fakeMidi?: FakeMidiHandle;
  }
}

/** MidiDriver implementation backed by the fake Web MIDI shim. */
export class WebMidiDriver implements MidiDriver {
  private available = true;
  private fakeInstalled = false;

  constructor(private readonly page: Page) {}

  async setTransportAvailable(available: boolean): Promise<void> {
    this.available = available;
    if (!available) {
      // Init scripts run in registration order, so registering the removal
      // after the fake makes the removal win on the next navigation.
      await this.page.addInitScript(removeWebMidiSupport);
    } else if (this.fakeInstalled) {
      await this.page.addInitScript(installFakeWebMidi);
    }
  }

  /** Called by the editor driver before the first navigation. */
  async installTransport(): Promise<void> {
    if (this.fakeInstalled) return;
    this.fakeInstalled = true;
    if (this.available) {
      await this.page.addInitScript(installFakeWebMidi);
    } else {
      await this.page.addInitScript(removeWebMidiSupport);
    }
  }

  private midiToggle() {
    return this.page.getByRole("button", { name: /^MIDI O(n|ff)$/ });
  }

  async connect(): Promise<void> {
    const toggle = this.midiToggle();
    if ((await toggle.getAttribute("aria-pressed")) !== "true") {
      await toggle.click();
    }
    await this.page.getByLabel("MIDI output port").selectOption(FAKE_OUTPUT_ID);
    await this.page.getByLabel("MIDI input port").selectOption(FAKE_INPUT_ID);
  }

  async disconnect(): Promise<void> {
    const toggle = this.midiToggle();
    if ((await toggle.getAttribute("aria-pressed")) === "true") {
      await toggle.click();
    }
  }

  async transportReportedUnavailable(): Promise<boolean> {
    const note = this.page.getByText("Web MIDI not supported in this browser");
    if (!(await note.isVisible())) return false;
    return this.midiToggle().isDisabled();
  }

  async receiveFromDevice(bytes: Uint8Array): Promise<void> {
    await this.page.evaluate((data) => {
      window.__fakeMidi?.receive(data);
    }, Array.from(bytes));
  }

  async sentMessages(): Promise<Uint8Array[]> {
    const sent = await this.page.evaluate(() => window.__fakeMidi?.sent ?? []);
    return sent.map((message) => new Uint8Array(message));
  }

  async clearSentMessages(): Promise<void> {
    await this.page.evaluate(() => window.__fakeMidi?.clear());
  }

  async waitForSentCount(count: number, timeoutMs = 15_000): Promise<Uint8Array[]> {
    await expect
      .poll(async () => (await this.sentMessages()).length, {
        timeout: timeoutMs,
        message: `waiting for the device to receive ${count} message(s)`,
      })
      .toBeGreaterThanOrEqual(count);
    return this.sentMessages();
  }

  async lastReceiveWasEcho(): Promise<boolean> {
    // The echo classification is surfaced to the user in the debug panel's
    // MIDI log; open it (if needed) and inspect the newest entry.
    const openButton = this.page.getByRole("button", { name: "Open debug panel" });
    if (await openButton.isVisible()) {
      await openButton.click();
    }
    const panel = this.page.locator('aside[aria-label="Debug panel"]');
    const newest = panel.locator("li").first();
    await expect(newest).toBeVisible();
    const text = (await newest.textContent()) ?? "";
    return text.includes("RX") && text.includes("echo match");
  }
}
