import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { buildSystemControls } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { hydrateSystemFromBytes } from "@/sysex/hydrate";
import { buildProgramDump, buildSystemDump } from "@/sysex/serialize";
import {
  verifyProgramDumpChecksum,
  verifySystemDumpChecksum,
} from "@/sysex/frame";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

function loadSpec(): DumpSpec {
  const p = path.join(
    repo,
    "specification/prog/m7_program_dump.spec.json",
  );
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function loadTemplate(): Uint8Array {
  return loadSerializeSkeletons().prog;
}

describe("serialize", () => {
  it("patches diffusion and yields valid checksum", () => {
    const spec = loadSpec();
    const template = loadTemplate();
    const diffusionField = spec.fields.find((f) => f.parameter === "diffusion")!;
    const state = {
      programName: "Test",
      encoded: {
        [diffusionField.id]: 7,
        bank_index: 0,
        program_slot: 0,
        bank_index_mirror: 0,
      },
    };
    const out = buildProgramDump(state, spec.fields, template);
    expect(out.length).toBe(157);
    expect(verifyProgramDumpChecksum(out)).toBe(true);
    expect(out[107]).toBe(7);
  });

  it("bank_index_mirror tracks bank low nibble", () => {
    const spec = loadSpec();
    const template = loadTemplate();
    const out = buildProgramDump(
      {
        programName: "Bank",
        encoded: { bank_index: 11, program_slot: 0, bank_index_mirror: 0 },
      },
      spec.fields,
      template,
    );
    expect(out[137]).toBe(11 & 0x0f);
  });

  it("writes program name into the dump", () => {
    const spec = loadSpec();
    const template = loadTemplate();
    const out = buildProgramDump(
      {
        programName: "My Patch",
        encoded: { bank_index: 0, program_slot: 0, bank_index_mirror: 0 },
      },
      spec.fields,
      template,
    );
    const name = new TextDecoder("ascii").decode(out.subarray(8, 88));
    expect(name.startsWith("My Patch")).toBe(true);
    expect(verifyProgramDumpChecksum(out)).toBe(true);
  });
});

function loadSystemSpec(): DumpSpec {
  return JSON.parse(
    fs.readFileSync(
      path.join(repo, "specification/system/m7_system_dump.spec.json"),
      "utf8",
    ),
  );
}

function loadSystemTemplate(): Uint8Array {
  return loadSerializeSkeletons().system;
}

describe("buildSystemDump", () => {
  it("patches wet gain and yields valid checksum", () => {
    const spec = loadSystemSpec();
    const template = loadSystemTemplate();
    const wetField = spec.fields.find((f) => f.parameter === "wet gain")!;
    const controls = buildSystemControls(spec);
    const wetControl = controls.find((c) => c.fieldId === wetField.id)!;
    const encoded = wetControl.entries[2]?.encoded ?? wetControl.entries[0].encoded;
    const out = buildSystemDump({ [wetField.id]: encoded }, spec.fields, template);
    expect(out.length).toBe(77);
    expect(verifySystemDumpChecksum(out)).toBe(true);
    expect(out[wetField.start]).toBeDefined();
  });

  it("roundtrips system state through hydrate", () => {
    const spec = loadSystemSpec();
    const template = loadSystemTemplate();
    const controls = buildSystemControls(spec);
    const wetField = spec.fields.find((f) => f.parameter === "wet gain")!;
    const state = Object.fromEntries(
      controls.map((c) => [c.fieldId, c.entries[0].encoded]),
    );
    state[wetField.id] = controls.find((c) => c.fieldId === wetField.id)!.entries[2].encoded;
    const built = buildSystemDump(state, spec.fields, template);
    const hydrated = hydrateSystemFromBytes(built, controls);
    expect(hydrated[wetField.id]).toBe(state[wetField.id]);
    expect(verifySystemDumpChecksum(built)).toBe(true);
  });
});
