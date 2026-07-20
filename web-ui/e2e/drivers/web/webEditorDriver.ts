import fs from "node:fs/promises";
import { expect, type Locator, type Page } from "@playwright/test";
import type { CompareSlot, EditorDriver, EditorView } from "../editorDriver";
import type { WebMidiDriver } from "./webMidiDriver";

/**
 * Domain parameter name (lowercase spec name) → label the web UI displays.
 * Mirrors PARAMETER_DISPLAY_LABELS in src/spec/labels.ts.
 */
const DISPLAY_LABELS: Record<string, string> = {
  "early to reverb mix": "Early/Late",
  "early rolloff": "Early",
  modulation: "MOD",
  "audio routing": "Routing",
  "audio format": "Format",
  "display level": "Display",
  "midi channel": "Channel",
  "midi bank": "MIDI Bank",
  "wet gain": "Wet Gain",
  "dry gain": "Dry Gain",
  "output level": "Output Level",
};

function canonicalParam(name: string): string {
  return name.trim().toLowerCase();
}

/** EditorDriver implementation that drives the web UI through Playwright. */
export class WebEditorDriver implements EditorDriver {
  constructor(
    readonly page: Page,
    private readonly midi: WebMidiDriver,
  ) {}

  // ---- lifecycle ----------------------------------------------------------

  async start(): Promise<void> {
    // Each Playwright browser context starts with empty storage, so a plain
    // navigation is a fresh session.
    await this.midi.installTransport();
    await this.page.goto("/");
    await this.waitUntilReady();
  }

  async restart(): Promise<void> {
    await this.page.reload();
    await this.waitUntilReady();
  }

  private async waitUntilReady(): Promise<void> {
    await expect(
      this.page.getByRole("tab", { name: "Program", exact: true }),
    ).toBeVisible({ timeout: 20_000 });
  }

  // ---- views --------------------------------------------------------------

  private viewTab(view: EditorView): Locator {
    const name = view === "program" ? "Program" : "System";
    return this.page.getByRole("tab", { name, exact: true });
  }

  async activeView(): Promise<EditorView> {
    const selected = await this.viewTab("program").getAttribute("aria-selected");
    return selected === "true" ? "program" : "system";
  }

  async openView(view: EditorView): Promise<void> {
    await this.viewTab(view).click();
    await expect(this.viewTab(view)).toHaveAttribute("aria-selected", "true");
  }

  // ---- programs -----------------------------------------------------------

  async programName(): Promise<string> {
    return (await this.page.getByTestId("program-name").textContent())?.trim() ?? "";
  }

  async selectFactoryProgram(bank: string, program: string): Promise<void> {
    const bankList = this.page.getByRole("listbox", { name: "Preset banks" });
    // Option names include the preset count ("Halls v1 30"), so anchor at the start.
    const escaped = bank.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    await bankList.getByRole("option", { name: new RegExp(`^${escaped}\\b`) }).click();
    const programList = this.page.getByRole("listbox", { name: /^Programs in / });
    await programList.getByRole("option", { name: program, exact: true }).click();
  }

  // ---- parameters ---------------------------------------------------------

  paramContainer(name: string): Locator {
    return this.page.locator(
      `[data-testid="param-control"][data-param="${canonicalParam(name)}"]`,
    );
  }

  displayLabel(name: string): string {
    const canonical = canonicalParam(name);
    return DISPLAY_LABELS[canonical] ?? canonical;
  }

  async parameterValue(name: string): Promise<string> {
    const container = this.paramContainer(name);
    await expect(container).toBeVisible();
    const checkedRadio = container.locator('[role="radio"][aria-checked="true"]');
    if ((await checkedRadio.count()) > 0) {
      return (await checkedRadio.textContent())?.trim() ?? "";
    }
    const value = container.getByTestId("param-value").first();
    return (await value.textContent())?.trim() ?? "";
  }

  async setParameter(name: string, value: string): Promise<void> {
    const container = this.paramContainer(name);
    await container.scrollIntoViewIfNeeded();
    if ((await container.locator('[role="radio"]').count()) > 0) {
      await container.getByRole("radio", { name: value, exact: true }).click();
      return;
    }
    await container.locator('button[data-testid="param-value"]').click();
    const input = container.getByTestId("param-value-input");
    await input.fill(value);
    await input.press("Enter");
  }

  async parameterValues(name: string): Promise<string[]> {
    const container = this.paramContainer(name);
    await container.scrollIntoViewIfNeeded();

    // Button-list parameters show every choice at once.
    const radios = container.locator('[role="radio"]');
    if ((await radios.count()) > 0) {
      return (await radios.allTextContents()).map((t) => t.trim());
    }

    // Dials: select the control, then walk the whole range with arrow-key
    // steps inside the page (one protocol round-trip instead of hundreds).
    // First walk to the bottom with more ArrowDown presses than any value
    // table has entries, then step upward reading the readout until it
    // stops changing.
    await this.clickDial(name);
    return await this.page.evaluate(
      async ({ param, max }) => {
        const container = document.querySelector(
          `[data-testid="param-control"][data-param="${param}"]`,
        );
        const read = () =>
          container
            ?.querySelector('[data-testid="param-value"]')
            ?.textContent?.trim() ?? "";
        // A macrotask between presses lets React flush the state update the
        // app's window keydown listener made, so the next press sees it.
        const step = async (key: string) => {
          window.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true }));
          await new Promise((resolve) => setTimeout(resolve));
        };
        for (let i = 0; i < max; i++) await step("ArrowDown");
        const values: string[] = [];
        for (let i = 0; i <= max; i++) {
          const value = read();
          if (values[values.length - 1] === value) break;
          values.push(value);
          await step("ArrowUp");
        }
        return values;
      },
      { param: canonicalParam(name), max: 160 },
    );
  }

  async parameterEditable(name: string): Promise<boolean> {
    const container = this.paramContainer(name);
    await expect(container).toBeVisible();
    const radios = container.locator('[role="radio"]');
    if ((await radios.count()) > 0) {
      return !(await radios.first().isDisabled());
    }
    return (await container.locator('button[data-testid="param-value"]').count()) > 0;
  }

  async selectParameter(name: string): Promise<void> {
    const dial = this.paramContainer(name).getByTestId("knob-dial");
    await dial.scrollIntoViewIfNeeded();
    await dial.click();
  }

  async deselectParameter(): Promise<void> {
    await this.page.keyboard.press("Escape");
  }

  private lockToggle(name: string): Locator {
    return this.paramContainer(name).getByRole("button", { name: /^(Lock|Unlock) / });
  }

  async lockParameter(name: string): Promise<void> {
    const toggle = this.lockToggle(name);
    if ((await toggle.getAttribute("aria-pressed")) !== "true") {
      await toggle.click();
    }
  }

  async unlockParameter(name: string): Promise<void> {
    const toggle = this.lockToggle(name);
    if ((await toggle.getAttribute("aria-pressed")) === "true") {
      await toggle.click();
    }
  }

  // ---- A/B compare --------------------------------------------------------

  private compareSlotButton(slot: CompareSlot): Locator {
    return this.page.getByRole("button", { name: `Compare slot ${slot}`, exact: true });
  }

  async activeCompareSlot(): Promise<CompareSlot> {
    const aPressed = await this.compareSlotButton("A").getAttribute("aria-pressed");
    return aPressed === "true" ? "A" : "B";
  }

  async selectCompareSlot(slot: CompareSlot): Promise<void> {
    await this.compareSlotButton(slot).click();
    await expect(this.compareSlotButton(slot)).toHaveAttribute("aria-pressed", "true");
  }

  async swapCompareSlots(): Promise<void> {
    await this.page.getByRole("button", { name: "Swap slots A and B" }).click();
  }

  // ---- saved presets & files ----------------------------------------------

  async saveUserPreset(name: string): Promise<void> {
    await this.page.getByLabel("Name").fill(name);
    await this.page.getByRole("button", { name: "Save", exact: true }).click();
  }

  private savedPresetsSelect(): Locator {
    return this.page.getByLabel("Saved presets");
  }

  async loadUserPreset(name: string): Promise<void> {
    await this.savedPresetsSelect().selectOption({ label: name });
    await this.page.getByRole("button", { name: "Load", exact: true }).click();
  }

  async deleteUserPreset(name: string): Promise<void> {
    await this.savedPresetsSelect().selectOption({ label: name });
    await this.page.getByRole("button", { name: "Delete", exact: true }).click();
  }

  async savedPresetNames(): Promise<string[]> {
    const options = await this.savedPresetsSelect().locator("option").allTextContents();
    // Drop the "Load saved…" placeholder.
    return options.slice(1).map((label) => label.trim());
  }

  private async downloadFromButton(buttonName: string): Promise<Uint8Array> {
    const downloadPromise = this.page.waitForEvent("download");
    await this.page.getByRole("button", { name: buttonName, exact: true }).click();
    const download = await downloadPromise;
    const filePath = await download.path();
    return new Uint8Array(await fs.readFile(filePath));
  }

  async exportProgramFile(): Promise<Uint8Array> {
    return this.downloadFromButton("Download prog .syx");
  }

  async exportSystemFile(): Promise<Uint8Array> {
    return this.downloadFromButton("Download sys .syx");
  }

  async importFile(bytes: Uint8Array, filename = "import.syx"): Promise<void> {
    await this.page.locator('input[type="file"]').setInputFiles({
      name: filename,
      mimeType: "application/octet-stream",
      buffer: Buffer.from(bytes),
    });
  }

  // ---- tempo ----------------------------------------------------------------

  private tempoInput(): Locator {
    return this.page.getByLabel("Tempo BPM");
  }

  async setTempoBpm(bpm: number | string): Promise<void> {
    const input = this.tempoInput();
    await input.fill(String(bpm));
    await input.press("Enter");
  }

  async tempoBpm(): Promise<number> {
    return Number(await this.tempoInput().inputValue());
  }

  async setTempoMode(parameter: string, on: boolean): Promise<void> {
    const toggle = this.paramContainer(parameter).getByRole("button", {
      name: /^Tempo mode/,
    });
    if (((await toggle.getAttribute("aria-pressed")) === "true") !== on) {
      await toggle.click();
    }
  }

  async timingErrorMs(parameter: string): Promise<number | null> {
    // The web UI surfaces snapping errors in the debug drawer's Timing
    // section, one line per parameter: `predelay: 1/8 → 252 ms (Δ+2.0 ms)`.
    await this.openDebugPanel();
    const timing = this.debugPanel().locator("section", { hasText: "Timing" });
    if ((await timing.count()) === 0) return null;
    const item = timing.locator("li", { hasText: this.displayLabel(parameter) });
    if ((await item.count()) === 0) return null;
    const text = (await item.first().textContent()) ?? "";
    const match = text.match(/Δ([+-]?[\d.]+)\s*ms/);
    return match ? Number(match[1]) : null;
  }

  // ---- MIDI-facing editor controls ------------------------------------------

  async sendToDevice(): Promise<void> {
    await this.page.getByRole("button", { name: "Send", exact: true }).click();
  }

  async setSendOnChange(on: boolean): Promise<void> {
    const toggle = this.page.getByRole("button", { name: "On change", exact: true });
    if (((await toggle.getAttribute("aria-pressed")) === "true") !== on) {
      await toggle.click();
    }
  }

  async setSendOnChangeThrottleMs(ms: number): Promise<void> {
    const input = this.page.getByLabel("Send on change throttle milliseconds");
    await input.fill(String(ms));
    await input.press("Enter");
  }

  // ==== Web-only helpers (used by @target-specific features) =================

  dialSurface(name: string): Locator {
    return this.paramContainer(name).getByTestId("knob-dial");
  }

  private async dialCenter(name: string): Promise<{ x: number; y: number }> {
    const dial = this.dialSurface(name);
    await dial.scrollIntoViewIfNeeded();
    const box = await dial.boundingBox();
    if (!box) throw new Error(`dial for "${name}" has no bounding box`);
    return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
  }

  async dragDial(name: string, dyUp: number): Promise<void> {
    const { x, y } = await this.dialCenter(name);
    await this.page.mouse.move(x, y);
    await this.page.mouse.down();
    await this.page.mouse.move(x, y - dyUp, { steps: 8 });
    await this.page.mouse.up();
  }

  async wheelDial(name: string, deltaY: number): Promise<void> {
    const { x, y } = await this.dialCenter(name);
    await this.page.mouse.move(x, y);
    await this.page.mouse.wheel(0, deltaY);
  }

  async doubleClickDial(name: string): Promise<void> {
    await this.dialSurface(name).dblclick();
  }

  async clickDial(name: string): Promise<void> {
    await this.dialSurface(name).click();
  }

  /** Begin typing into a dial's value readout without committing. */
  async beginTypingParameter(name: string, draft: string): Promise<Locator> {
    const container = this.paramContainer(name);
    await container.locator('button[data-testid="param-value"]').click();
    const input = container.getByTestId("param-value-input");
    await input.fill(draft);
    return input;
  }

  debugPanel(): Locator {
    return this.page.locator('aside[aria-label="Debug panel"]');
  }

  async openDebugPanel(): Promise<void> {
    // The drawer stays in the DOM when closed (slid off-screen with
    // aria-hidden), so visibility is tracked via the aria-hidden attribute.
    const opener = this.page.getByRole("button", { name: "Open debug panel" });
    if (await opener.isVisible()) {
      await opener.click();
    }
    await expect(this.debugPanel()).toHaveAttribute("aria-hidden", "false");
  }

  async debugPanelVisible(): Promise<boolean> {
    return (await this.debugPanel().getAttribute("aria-hidden")) === "false";
  }
}
