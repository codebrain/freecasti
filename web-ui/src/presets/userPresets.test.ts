import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it, beforeEach } from "vitest";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import type { DumpSpec } from "@/spec/types";
import { hydrateProgramFromBytes } from "@/sysex/hydrate";
import type { ProgSerializeState } from "@/sysex/serialize";
import { readSyxFromBuffer } from "@/sysex/syxIo";
import { loadSerializeSkeletons } from "@/test/serializeSkeletons";
import {
  deleteUserPreset,
  getUserPreset,
  listUserPresets,
  LS_USER_PRESETS,
  progBytesFromSaved,
  saveUserPreset,
  type StorageLike,
} from "@/presets/userPresets";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

import { makeMemoryStorage } from "@/test/memoryStorage";

describe("userPresets", () => {
  let storage: StorageLike;
  let progState: ProgSerializeState;
  let progBytes: Uint8Array;
  let sysState: Record<string, number>;
  let sysBytes: Uint8Array;

  beforeEach(() => {
    storage = makeMemoryStorage();
    const progSpec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/prog/m7_program_dump.spec.json"),
        "utf8",
      ),
    );
    const sysSpec: DumpSpec = JSON.parse(
      fs.readFileSync(
        path.join(repo, "specification/system/m7_system_dump.spec.json"),
        "utf8",
      ),
    );
    const skeletons = loadSerializeSkeletons();
    progBytes = readSyxFromBuffer(skeletons.prog);
    sysBytes = readSyxFromBuffer(skeletons.system);
    progState = hydrateProgramFromBytes(
      progBytes,
      progSpec,
      allProgControls(progSpec),
    );
    sysState = Object.fromEntries(
      buildSystemControls(sysSpec).map((c) => [c.fieldId, c.entries[0].encoded]),
    );
  });

  it("starts empty", () => {
    expect(listUserPresets(storage)).toEqual([]);
  });

  it("save and list presets in localStorage", () => {
    const saved = saveUserPreset(
      storage,
      "My Hall",
      progState,
      progBytes,
      sysState,
      sysBytes,
    );
    expect(saved.name).toBe("My Hall");
    expect(listUserPresets(storage)).toHaveLength(1);
    expect(storage.getItem(LS_USER_PRESETS)).toContain("My Hall");
  });

  it("load restores byte-identical prog dump", () => {
    const saved = saveUserPreset(storage, "Test", progState, progBytes);
    const loaded = getUserPreset(storage, saved.id)!;
    const bytes = progBytesFromSaved(loaded);
    expect(Array.from(bytes)).toEqual(Array.from(progBytes));
  });

  it("delete removes preset", () => {
    const saved = saveUserPreset(storage, "Gone", progState, progBytes);
    deleteUserPreset(storage, saved.id);
    expect(listUserPresets(storage)).toHaveLength(0);
    expect(getUserPreset(storage, saved.id)).toBeUndefined();
  });

  it("rejects empty name", () => {
    expect(() => saveUserPreset(storage, "  ", progState, progBytes)).toThrow(
      /name is required/,
    );
  });
});
