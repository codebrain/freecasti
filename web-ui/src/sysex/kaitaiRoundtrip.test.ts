import { describe, expect, it } from "vitest";
import {
  listProgCorpusDumps,
  listProgMenuDumps,
  listSystemDumps,
  readSysexDump,
} from "@/test/corpusSysex";
import {
  assertChecksumMatchesNative,
  assertMessageRoundtrip,
  loadSpecFields,
  parseProgDump,
  parseSystemDump,
  splitSysexMessages,
  verifyChecksum,
} from "@/test/kaitaiSupport";
import { serializeParsedDump } from "@/sysex/kaitaiEncode";
import {
  PROGRAM_MESSAGE_LENGTH,
  SYSTEM_MESSAGE_LENGTH,
  writeProgramDumpChecksum,
} from "@/sysex/frame";

const PROG_FIELDS = loadSpecFields("prog");
const SYSTEM_FIELDS = loadSpecFields("system");
const PROG_DUMPS = listProgCorpusDumps();
const PROG_MENU_DUMPS = listProgMenuDumps();
const SYSTEM_DUMPS = listSystemDumps();

const PROG_SAMPLE = "prog/parameters/diffusion/low.syx";
const SYSTEM_SAMPLE = "system/midi channel/1.syx";
const PRESET_SAMPLE = "prog/presets/Chambers.Large Chamber.syx";
const FULL_SWEEP_SAMPLE = "prog/full sweep/reverb time.syx";

describe("kaitai parsers compile", () => {
  it("loads generated program and system parser modules", async () => {
    const mod = await import("@/generated/sysex-parsers/index.js");
    expect(mod.M7ProgramDump).toBeTypeOf("function");
    expect(mod.M7SystemDump).toBeTypeOf("function");
  });
});

describe("kaitai parse roundtrip (field wire bytes)", () => {
  it.each(PROG_DUMPS)("prog %s", (rel) => {
    const raw = readSysexDump(rel);
    expect(raw.length).toBe(PROGRAM_MESSAGE_LENGTH);
    expect(verifyChecksum(raw, "prog")).toBe(true);
    const parsed = parseProgDump(raw);
    assertMessageRoundtrip(parsed, raw, PROG_FIELDS, rel);
    assertChecksumMatchesNative(parsed, raw, "prog");
  });

  it.each(PROG_MENU_DUMPS)("prog menu %s", (rel) => {
    const raw = readSysexDump(rel);
    const parsed = parseProgDump(raw);
    assertMessageRoundtrip(parsed, raw, PROG_FIELDS, rel);
    assertChecksumMatchesNative(parsed, raw, "prog");
  });

  it.each(SYSTEM_DUMPS)("system %s", (rel) => {
    const raw = readSysexDump(rel);
    expect(raw.length).toBe(SYSTEM_MESSAGE_LENGTH);
    expect(verifyChecksum(raw, "system")).toBe(true);
    const parsed = parseSystemDump(raw);
    assertMessageRoundtrip(parsed, raw, SYSTEM_FIELDS, rel);
    assertChecksumMatchesNative(parsed, raw, "system");
  });
});

describe("full sweep concatenated dumps", () => {
  it("roundtrips every message in reverb time sweep", () => {
    const raw = readSysexDump(FULL_SWEEP_SAMPLE);
    const messages = splitSysexMessages(raw);
    expect(messages).toHaveLength(137);
    for (const msg of messages) {
      expect(msg.length).toBe(PROGRAM_MESSAGE_LENGTH);
      expect(verifyChecksum(msg, "prog")).toBe(true);
      const parsed = parseProgDump(msg);
      assertMessageRoundtrip(parsed, msg, PROG_FIELDS, FULL_SWEEP_SAMPLE);
      assertChecksumMatchesNative(parsed, msg, "prog");
    }
  });

  it("serializes every message in reverb time sweep", () => {
    const raw = readSysexDump(FULL_SWEEP_SAMPLE);
    for (const msg of splitSysexMessages(raw)) {
      const parsed = parseProgDump(msg);
      const encoded = serializeParsedDump(parsed, PROG_FIELDS);
      expect(encoded).toEqual(msg);
    }
  });
});

describe("kaitai serialize roundtrip (parse → serialize → bytes)", () => {
  it("prog diffusion sample matches capture", () => {
    const raw = readSysexDump(PROG_SAMPLE);
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    expect(encoded).toEqual(raw);
  });

  it("system midi channel sample matches capture", () => {
    const raw = readSysexDump(SYSTEM_SAMPLE);
    const parsed = parseSystemDump(raw);
    const encoded = serializeParsedDump(parsed, SYSTEM_FIELDS, { system: true });
    expect(encoded).toEqual(raw);
  });

  it("preset re-parse is byte-identical", () => {
    const raw = readSysexDump(PRESET_SAMPLE);
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    const again = parseProgDump(encoded);
    expect(serializeParsedDump(again, PROG_FIELDS)).toEqual(encoded);
    expect(encoded).toEqual(raw);
  });

  it("repairs corrupt checksum on serialize", () => {
    const raw = new Uint8Array(readSysexDump(PROG_SAMPLE));
    raw[152] = (raw[152]! + 1) % 16;
    expect(verifyChecksum(raw, "prog")).toBe(false);
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    expect(verifyChecksum(encoded, "prog")).toBe(true);
    expect(encoded).not.toEqual(raw);
    expect(encoded.subarray(0, 152)).toEqual(raw.subarray(0, 152));
  });

  it("writeProgramDumpChecksum matches serializer", () => {
    const raw = new Uint8Array(readSysexDump(PROG_SAMPLE));
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    const buf = new Uint8Array(encoded);
    buf.fill(0, 152, 156);
    writeProgramDumpChecksum(buf);
    expect(buf).toEqual(encoded);
  });

  it.each(PROG_MENU_DUMPS)("prog menu %s", (rel) => {
    const raw = readSysexDump(rel);
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    expect(encoded).toEqual(raw);
    const reparsed = parseProgDump(encoded);
    expect(serializeParsedDump(reparsed, PROG_FIELDS)).toEqual(encoded);
  });

  it.each(PROG_DUMPS)("prog %s", (rel) => {
    const raw = readSysexDump(rel);
    const parsed = parseProgDump(raw);
    const encoded = serializeParsedDump(parsed, PROG_FIELDS);
    expect(encoded).toEqual(raw);
    const reparsed = parseProgDump(encoded);
    expect(serializeParsedDump(reparsed, PROG_FIELDS)).toEqual(encoded);
  });

  it.each(SYSTEM_DUMPS)("system %s", (rel) => {
    const raw = readSysexDump(rel);
    const parsed = parseSystemDump(raw);
    const encoded = serializeParsedDump(parsed, SYSTEM_FIELDS, { system: true });
    expect(encoded).toEqual(raw);
    const reparsed = parseSystemDump(encoded);
    expect(serializeParsedDump(reparsed, SYSTEM_FIELDS, { system: true })).toEqual(
      encoded,
    );
  });
});

describe("corpus inventory", () => {
  it("includes hundreds of prog dumps and system/menu series", () => {
    expect(PROG_DUMPS.length).toBeGreaterThan(300);
    expect(SYSTEM_DUMPS.length).toBeGreaterThan(60);
    expect(PROG_MENU_DUMPS.length).toBeGreaterThanOrEqual(19);
  });
});
