import { expect } from "@playwright/test";
import { Then, When } from "../fixtures";

When("the user sets the tempo to {int} BPM", async ({ editor }, bpm: number) => {
  await editor.setTempoBpm(bpm);
});

Then("the tempo shows {int} BPM", async ({ editor }, bpm: number) => {
  await expect.poll(() => editor.tempoBpm()).toBe(bpm);
});

When("the user enables tempo mode for {string}", async ({ editor }, name: string) => {
  await editor.setTempoMode(name, true);
});

When("the user disables tempo mode for {string}", async ({ editor }, name: string) => {
  await editor.setTempoMode(name, false);
});

Then(
  "{string} reports a timing error of {float} ms",
  async ({ editor }, name: string, ms: number) => {
    await expect.poll(() => editor.timingErrorMs(name)).toBeCloseTo(ms, 1);
  },
);

Then("{string} reports no timing error", async ({ editor }, name: string) => {
  await expect.poll(() => editor.timingErrorMs(name)).toBeNull();
});
