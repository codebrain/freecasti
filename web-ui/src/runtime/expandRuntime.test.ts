import { describe, expect, it } from "vitest";
import { decodeBase64Template, expandRuntimeBundle } from "@/runtime/expandRuntime";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import fs from "node:fs";
import path from "node:path";
import { repoRoot } from "@/test/presetFixtures";

describe("expandRuntime", () => {
  it("expands compact runtime JSON into specs, presets, and templates", () => {
    const raw = JSON.parse(
      fs.readFileSync(path.join(repoRoot, "web-ui/public/m7-runtime.json"), "utf8"),
    );
    const bundle = expandRuntimeBundle(raw);
    expect(bundle.prog.fields.length).toBeGreaterThan(0);
    expect(bundle.system.fields.length).toBeGreaterThan(0);
    expect(bundle.presets.presets.length).toBeGreaterThan(100);
    expect(bundle.templates.prog.length).toBe(157);
    expect(bundle.templates.system.length).toBe(77);
  });

  it("matches loadRuntimeFixture helper", () => {
    const bundle = loadRuntimeFixture();
    expect(bundle.presets.presets.length).toBeGreaterThan(100);
  });

  it("decodes base64 templates byte-for-byte", () => {
    const bundle = loadRuntimeFixture();
    const decoded = decodeBase64Template(
      Buffer.from(bundle.templates.prog).toString("base64"),
    );
    expect(decoded).toEqual(bundle.templates.prog);
  });
});
