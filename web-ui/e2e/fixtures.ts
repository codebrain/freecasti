import { test as base, createBdd } from "playwright-bdd";
import type { EditorDriver } from "./drivers/editorDriver";
import type { MidiDriver } from "./drivers/midiDriver";
import { WebEditorDriver } from "./drivers/web/webEditorDriver";
import { WebMidiDriver } from "./drivers/web/webMidiDriver";

/** Mutable scratch space shared between the steps of one scenario. */
export interface ScenarioContext {
  exportedFile?: Uint8Array;
  sentCountMark?: number;
}

interface Fixtures {
  /** Target-agnostic drivers — the only surface portable steps may use. */
  editor: EditorDriver;
  midi: MidiDriver;
  /** Concrete web drivers for @target-specific-only steps. */
  webEditor: WebEditorDriver;
  webMidi: WebMidiDriver;
  ctx: ScenarioContext;
}

export const test = base.extend<Fixtures>({
  webMidi: async ({ page }, use) => {
    await use(new WebMidiDriver(page));
  },
  webEditor: async ({ page, webMidi }, use) => {
    await use(new WebEditorDriver(page, webMidi));
  },
  editor: async ({ webEditor }, use) => {
    await use(webEditor);
  },
  midi: async ({ webMidi }, use) => {
    await use(webMidi);
  },
  ctx: async ({}, use) => {
    await use({});
  },
});

export const { Given, When, Then } = createBdd(test);
