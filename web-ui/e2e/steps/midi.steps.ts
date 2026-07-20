import { expect } from "@playwright/test";
import { Given, Then, When } from "../fixtures";
import { progMenuHighlights, progMenuIdle } from "../support/progMenu";
import { bytesEqual, isProgramDump, isSystemDump } from "../support/sysex";

Given("a MIDI connection to the device", async ({ midi }) => {
  await midi.connect();
});

Given("send on change is disabled", async ({ editor }) => {
  await editor.setSendOnChange(false);
});

Given("send on change is enabled", async ({ editor }) => {
  await editor.setSendOnChange(true);
});

Given("the send on change throttle is {int} ms", async ({ editor }, ms: number) => {
  await editor.setSendOnChangeThrottleMs(ms);
});

When("the user sends the current settings to the device", async ({ editor }) => {
  await editor.sendToDevice();
});

Then("the device receives a program dump", async ({ midi }) => {
  await expect
    .poll(async () => {
      const sent = await midi.sentMessages();
      const last = sent[sent.length - 1];
      return last ? isProgramDump(last) : false;
    })
    .toBe(true);
});

Then("the device receives a system dump", async ({ midi }) => {
  await expect
    .poll(async () => {
      const sent = await midi.sentMessages();
      const last = sent[sent.length - 1];
      return last ? isSystemDump(last) : false;
    })
    .toBe(true);
});

Then(
  "the device receives exactly {int} message(s)",
  async ({ midi }, count: number) => {
    await midi.waitForSentCount(count);
    // The throttle could still flush a straggler; give it one full window
    // (3 s in the coalescing scenario) before asserting the final count.
    await new Promise((resolve) => setTimeout(resolve, 3_500));
    expect((await midi.sentMessages()).length).toBe(count);
  },
);

Then(
  "the last message the device received equals the exported file",
  async ({ midi, ctx }) => {
    if (!ctx.exportedFile) throw new Error("no file was exported in this scenario");
    const sent = await midi.waitForSentCount(1);
    expect(bytesEqual(sent[sent.length - 1], ctx.exportedFile)).toBe(true);
  },
);

Then("the last message the device received is a program dump", async ({ midi }) => {
  const sent = await midi.sentMessages();
  const last = sent[sent.length - 1];
  expect(last && isProgramDump(last)).toBe(true);
});

When("the user selects the {string} control", async ({ editor }, name: string) => {
  await editor.selectParameter(name);
});

When("the user deselects the control", async ({ editor }) => {
  await editor.deselectParameter();
});

Then(
  "the device display highlights {string}",
  async ({ midi }, parameter: string) => {
    await expect
      .poll(async () => {
        const sent = await midi.sentMessages();
        const last = sent[sent.length - 1];
        return last && isProgramDump(last) ? progMenuHighlights(last) : null;
      })
      .toBe(parameter);
  },
);

Then("the device display returns to idle", async ({ midi }) => {
  await expect
    .poll(async () => {
      const sent = await midi.sentMessages();
      const last = sent[sent.length - 1];
      return last && isProgramDump(last) ? progMenuIdle(last) : false;
    })
    .toBe(true);
});

When(
  "the device sends back the last message it received",
  async ({ midi, ctx }) => {
    const sent = await midi.sentMessages();
    const last = sent[sent.length - 1];
    if (!last) throw new Error("the device has not received any messages yet");
    // Remember how much had been transmitted before this injection so a later
    // step can assert the editor did not respond with a transmission of its own.
    ctx.sentCountMark = sent.length;
    await midi.receiveFromDevice(last);
  },
);

Then("the editor transmits nothing further", async ({ midi, ctx }) => {
  const mark = ctx.sentCountMark ?? (await midi.sentMessages()).length;
  // Give the send-on-change throttle ample time to flush anything pending.
  await new Promise((resolve) => setTimeout(resolve, 1_500));
  expect((await midi.sentMessages()).length).toBe(mark);
});

Given("the MIDI transport is unavailable", async ({ midi }) => {
  await midi.setTransportAvailable(false);
});

Then("the editor reports that MIDI is unavailable", async ({ midi }) => {
  await expect.poll(() => midi.transportReportedUnavailable()).toBe(true);
});
