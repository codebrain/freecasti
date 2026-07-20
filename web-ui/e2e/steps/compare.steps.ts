import { expect } from "@playwright/test";
import type { CompareSlot } from "../drivers/editorDriver";
import { Then, When } from "../fixtures";

Then("compare slot {string} is active", async ({ editor }, slot: string) => {
  await expect.poll(() => editor.activeCompareSlot()).toBe(slot as CompareSlot);
});

When("the user activates compare slot {string}", async ({ editor }, slot: string) => {
  await editor.selectCompareSlot(slot as CompareSlot);
});

When("the user swaps the compare slots", async ({ editor }) => {
  await editor.swapCompareSlots();
});
