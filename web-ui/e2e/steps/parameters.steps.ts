import { expect } from "@playwright/test";
import type { DataTable } from "playwright-bdd";
import { Then, When } from "../fixtures";

When(
  "the user sets {string} to {string}",
  async ({ editor }, name: string, value: string) => {
    await editor.setParameter(name, value);
  },
);

Then("{string} shows {string}", async ({ editor }, name: string, value: string) => {
  await expect.poll(() => editor.parameterValue(name)).toBe(value);
});

Then(
  "{string} does not show {string}",
  async ({ editor }, name: string, value: string) => {
    await expect.poll(() => editor.parameterValue(name)).not.toBe(value);
  },
);

Then(
  "the only values available for {string} are:",
  async ({ editor }, name: string, table: DataTable) => {
    const expected = table.raw().map((row) => row[0]);
    expect(await editor.parameterValues(name)).toEqual(expected);
  },
);

Then("parameter {string} is editable", async ({ editor }, name: string) => {
  await expect.poll(() => editor.parameterEditable(name)).toBe(true);
});

Then("parameter {string} is not editable", async ({ editor }, name: string) => {
  await expect.poll(() => editor.parameterEditable(name)).toBe(false);
});

When("the user locks {string}", async ({ editor }, name: string) => {
  await editor.lockParameter(name);
});

When("the user unlocks {string}", async ({ editor }, name: string) => {
  await editor.unlockParameter(name);
});
