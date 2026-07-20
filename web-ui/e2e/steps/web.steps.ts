/**
 * Step definitions for @target-specific features only. These may use the concrete web
 * drivers (and through them Playwright's page); portable steps must not.
 */
import { expect } from "@playwright/test";
import { Given, Then, When } from "../fixtures";

// ---- app shell --------------------------------------------------------------

Given("the runtime assets are unavailable", async ({ webEditor }) => {
  await webEditor.page.route("**/m7-runtime.json", (route) =>
    route.fulfill({ status: 500, body: "unavailable" }),
  );
});

When("the editor is opened anyway", async ({ webEditor, webMidi }) => {
  await webMidi.installTransport();
  await webEditor.page.goto("/");
});

Then("a load error explains how to sync the assets", async ({ webEditor }) => {
  await expect(webEditor.page.getByText("python run.py")).toBeVisible();
});

When("the user opens the help dialog", async ({ webEditor }) => {
  await webEditor.page.getByRole("button", { name: "Help", exact: true }).click();
});

Then("the help dialog is shown", async ({ webEditor }) => {
  await expect(webEditor.page.getByRole("dialog")).toBeVisible();
});

Then("the help dialog is closed", async ({ webEditor }) => {
  await expect(webEditor.page.getByRole("dialog")).toHaveCount(0);
});

When("the user clicks the help Close button", async ({ webEditor }) => {
  await webEditor.page
    .getByRole("dialog")
    .getByRole("button", { name: "Close", exact: true })
    .click();
});

When("the user presses the {string} key", async ({ webEditor }, key: string) => {
  await webEditor.page.keyboard.press(key);
});

Then("the footer shows the legal disclaimer", async ({ webEditor }) => {
  await expect(
    webEditor.page.getByText("Provided as-is. Use at your own risk."),
  ).toBeVisible();
});

// ---- rendering mode ---------------------------------------------------------

When("the user switches rendering to {string}", async ({ webEditor }, mode: string) => {
  await webEditor.debugPanel().getByRole("radio", { name: mode }).click();
});

Then("the rendering mode is {string}", async ({ webEditor }, mode: string) => {
  await webEditor.openDebugPanel();
  await expect(
    webEditor.debugPanel().getByRole("radio", { name: mode }),
  ).toHaveAttribute("aria-checked", "true");
});

// ---- debug panel ------------------------------------------------------------

When("the user opens the debug panel", async ({ webEditor }) => {
  await webEditor.openDebugPanel();
});

Then("the debug panel is shown", async ({ webEditor }) => {
  await expect.poll(() => webEditor.debugPanelVisible()).toBe(true);
});

Then(
  "the last change shows {string} changing to {string}",
  async ({ webEditor }, label: string, value: string) => {
    const section = webEditor
      .debugPanel()
      .locator("section", { hasText: "Last change" });
    await expect(section).toContainText(label);
    await expect(section).toContainText(value);
  },
);

Then("the MIDI log shows a transmitted program dump", async ({ webEditor }) => {
  const newest = webEditor.debugPanel().locator("li").first();
  await expect(newest).toContainText("TX");
  await expect(newest).toContainText("program 157 B");
});

When("the user clears the MIDI log", async ({ webEditor }) => {
  await webEditor
    .debugPanel()
    .getByRole("button", { name: "Clear MIDI log" })
    .click();
});

Then("the MIDI log is empty", async ({ webEditor }) => {
  await expect(webEditor.debugPanel().getByText("No SysEx yet")).toBeVisible();
});

// ---- gestures ---------------------------------------------------------------

When("the user drags the {string} dial up", async ({ webEditor }, name: string) => {
  await webEditor.dragDial(name, 60);
});

When(
  "the user scrolls the mouse wheel up over the {string} dial",
  async ({ webEditor }, name: string) => {
    await webEditor.wheelDial(name, -120);
  },
);

When("the user double-clicks the {string} dial", async ({ webEditor }, name: string) => {
  await webEditor.doubleClickDial(name);
});

When("the user clicks the {string} dial", async ({ webEditor }, name: string) => {
  await webEditor.clickDial(name);
});

When(
  "the user starts typing {string} into {string} and presses Escape",
  async ({ webEditor }, draft: string, name: string) => {
    const input = await webEditor.beginTypingParameter(name, draft);
    await input.press("Escape");
  },
);
