import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  allProgControls,
  buildParameterToFieldId,
  buildSystemControls,
} from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import {
  detectDumpFamily,
  hydrateProgramFromBytes,
  hydrateSystemFromBytes,
} from "@/sysex/hydrate";
import { buildProgramDump, buildSystemDump } from "@/sysex/serialize";
import { readSyxFromBuffer } from "@/sysex/syxIo";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

describe("hydrate roundtrip", () => {
  it("skeleton prog dump matches serialize after hydrate", () => {
    const spec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const original = loadSerializeSkeletons().prog;
    const controls = allProgControls(spec);
    const state = hydrateProgramFromBytes(original, spec, controls);
    const rebuilt = buildProgramDump(state, spec.fields, original);
    expect(rebuilt.length).toBe(original.length);
    for (let i = 8; i < 152; i++) {
      expect(rebuilt[i]).toBe(original[i]);
    }
  });
});

describe("detectDumpFamily", () => {
  it("recognizes program and system dumps", () => {
    const prog = new Uint8Array(157);
    prog[6] = 0x01;
    const sys = new Uint8Array(77);
    sys[6] = 0x02;
    expect(detectDumpFamily(prog)).toBe("prog");
    expect(detectDumpFamily(sys)).toBe("system");
    expect(detectDumpFamily(new Uint8Array(10))).toBeNull();
  });
});

describe("hydrateSystemFromBytes", () => {
  it("reads system parameters from skeleton syx", () => {
    const sysSpec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/system/m7_system_dump.spec.json"),
        "utf8",
      ),
    );
    const controls = buildSystemControls(sysSpec);
    const bytes = readSyxFromBuffer(loadSerializeSkeletons().system.buffer);
    const state = hydrateSystemFromBytes(bytes, controls);
    const midiField = sysSpec.fields.find((f) => f.parameter === "midi channel")!;
    expect(state[midiField.id]).toBeDefined();
  });

  it("roundtrips system serialize after hydrate", () => {
    const sysSpec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/system/m7_system_dump.spec.json"),
        "utf8",
      ),
    );
    const controls = buildSystemControls(sysSpec);
    const original = loadSerializeSkeletons().system;
    const state = hydrateSystemFromBytes(original, controls);
    const rebuilt = buildSystemDump(state, sysSpec.fields, original);
    for (let i = 8; i < 72; i++) {
      expect(rebuilt[i]).toBe(original[i]);
    }
  });
});
