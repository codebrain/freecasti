import { expect } from "@playwright/test";
import { Then, When } from "../fixtures";
import {
  isProgramDump,
  isSystemDump,
  programChecksumValid,
  systemChecksumValid,
} from "../support/sysex";

When(
  "the user selects factory program {string} from bank {string}",
  async ({ editor }, program: string, bank: string) => {
    await editor.selectFactoryProgram(bank, program);
  },
);

When(
  "the user saves the current program as {string}",
  async ({ editor }, name: string) => {
    await editor.saveUserPreset(name);
  },
);

When("the user loads the saved preset {string}", async ({ editor }, name: string) => {
  await editor.loadUserPreset(name);
});

When("the user deletes the saved preset {string}", async ({ editor }, name: string) => {
  await editor.deleteUserPreset(name);
});

Then("the saved presets include {string}", async ({ editor }, name: string) => {
  await expect.poll(() => editor.savedPresetNames()).toContain(name);
});

Then("the saved presets do not include {string}", async ({ editor }, name: string) => {
  await expect.poll(() => editor.savedPresetNames()).not.toContain(name);
});

When("the user exports the current program to a file", async ({ editor, ctx }) => {
  ctx.exportedFile = await editor.exportProgramFile();
});

When("the user exports the system settings to a file", async ({ editor, ctx }) => {
  ctx.exportedFile = await editor.exportSystemFile();
});

When("the user imports the exported file", async ({ editor, ctx }) => {
  if (!ctx.exportedFile) throw new Error("no file was exported in this scenario");
  await editor.importFile(ctx.exportedFile);
});

Then("the exported file is a well-formed program dump", async ({ ctx }) => {
  const bytes = ctx.exportedFile;
  if (!bytes) throw new Error("no file was exported in this scenario");
  expect(isProgramDump(bytes)).toBe(true);
  expect(programChecksumValid(bytes)).toBe(true);
});

Then("the exported file is a well-formed system dump", async ({ ctx }) => {
  const bytes = ctx.exportedFile;
  if (!bytes) throw new Error("no file was exported in this scenario");
  expect(isSystemDump(bytes)).toBe(true);
  expect(systemChecksumValid(bytes)).toBe(true);
});
