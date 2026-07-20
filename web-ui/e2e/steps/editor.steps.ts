import { expect } from "@playwright/test";
import type { EditorView } from "../drivers/editorDriver";
import { Given, Then, When } from "../fixtures";

Given("the editor is started", async ({ editor }) => {
  await editor.start();
});

When("the editor is restarted", async ({ editor }) => {
  await editor.restart();
});

When("the user opens the {string} view", async ({ editor }, view: string) => {
  await editor.openView(view as EditorView);
});

Then("the {string} view is active", async ({ editor }, view: string) => {
  await expect.poll(() => editor.activeView()).toBe(view);
});

Then("a program name is shown", async ({ editor }) => {
  await expect.poll(() => editor.programName()).not.toBe("");
});

Then("the program name is {string}", async ({ editor }, name: string) => {
  await expect.poll(() => editor.programName()).toBe(name);
});
