import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it, beforeEach } from "vitest";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { importSyxBytes } from "@/sysex/importSyx";
import { buildProgramDump } from "@/sysex/serialize";
import { readSyxFromBuffer } from "@/sysex/syxIo";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

describe("importSyxBytes", () => {
  let progSpec: DumpSpec;
  let sysSpec: DumpSpec;
  let progTemplate: Uint8Array;

  beforeEach(() => {
    progSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    sysSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/system/m7_system_dump.spec.json"),
        "utf8",
      ),
    );
    progTemplate = loadSerializeSkeletons().prog;
  });

  it("imports program dump from skeleton", () => {
    const bytes = readSyxFromBuffer(loadSerializeSkeletons().prog);
    const result = importSyxBytes(
      bytes,
      progSpec,
      allProgControls(progSpec),
      buildSystemControls(sysSpec),
    );
    expect(result.family).toBe("prog");
    expect(result.progState?.encoded).toBeDefined();
    expect(result.progState?.ui).toEqual({ mode: "idle" });
  });

  it("imports system dump from skeleton", () => {
    const bytes = readSyxFromBuffer(loadSerializeSkeletons().system);
    const result = importSyxBytes(
      bytes,
      progSpec,
      allProgControls(progSpec),
      buildSystemControls(sysSpec),
    );
    expect(result.family).toBe("system");
    expect(result.sysState).toBeDefined();
  });

  it("rejects unrecognized dump family", () => {
    const framed = new Uint8Array(157);
    framed[0] = 0xf0;
    framed[framed.length - 1] = 0xf7;
    framed[6] = 0x99;
    expect(() =>
      importSyxBytes(
        framed,
        progSpec,
        allProgControls(progSpec),
        buildSystemControls(sysSpec),
      ),
    ).toThrow(/unrecognized/);
  });

  it("roundtrip: build → import matches encoded diffusion", () => {
    const diffusion = progSpec.fields.find((f) => f.parameter === "diffusion")!;
    const state = {
      programName: "Roundtrip",
      encoded: {
        [diffusion.id]: 7,
        bank_index: 0,
        program_slot: 0,
        bank_index_mirror: 0,
      },
    };
    const built = buildProgramDump(state, progSpec.fields, progTemplate);
    const imported = importSyxBytes(
      built,
      progSpec,
      allProgControls(progSpec),
      buildSystemControls(sysSpec),
    );
    expect(imported.progState?.encoded[diffusion.id]).toBe(7);
    expect(imported.progState?.programName).toBe("Roundtrip");
  });
});
