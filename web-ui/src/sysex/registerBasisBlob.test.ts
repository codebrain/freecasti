import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { SYSEX_ROOT } from "@/test/corpusSysex";
import { parseProgDump, splitSysexMessages } from "@/test/kaitaiSupport";
import {
  blobKind,
  decodeRegisterBasisBlob,
  decodeRegisterName,
  extractBits,
  sliceBlob,
  storedVsLive,
  type RegBlobLayout,
} from "./registerBasisBlob";

const REG_ROOT = path.join(SYSEX_ROOT, "prog", "edit", "registers");

interface RegisterFrame {
  label: string;
  raw: Uint8Array;
}

function listRegisterFrames(): RegisterFrame[] {
  const frames: RegisterFrame[] = [];
  const walk = (dir: string, prefix: string) => {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      const rel = prefix ? `${prefix}/${name}` : name;
      if (fs.statSync(full).isDirectory()) {
        walk(full, rel);
        continue;
      }
      if (!name.endsWith(".syx")) continue;
      const data = new Uint8Array(fs.readFileSync(full));
      splitSysexMessages(data).forEach((raw, i) => {
        frames.push({ label: `${rel}[${i}]`, raw });
      });
    }
  };
  walk(REG_ROOT, "");
  return frames;
}

/** Captures whose payload diverges from the blob (unstored edits). */
const DIVERGENT: Record<string, string[]> = {
  "samples/rooms-studio-a-b1s1-delay-edit.syx": [
    "delay_level",
    "delay_time",
    "delay_modulation",
  ],
  "samples/charset-b1s1-renamed.syx": [
    "delay_level",
    "delay_time",
    "delay_modulation",
  ],
  "samples/charset-b1s1-rt5s-unstored-edit.syx": [
    "reverb_time",
    "delay_level",
    "delay_time",
    "delay_modulation",
  ],
};

function asciiName(frame: Uint8Array): string {
  let out = "";
  for (let i = 8; i <= 21; i++) out += String.fromCharCode(frame[i]!);
  return out.replace(/ +$/, "");
}

function readSample(name: string): Uint8Array {
  return new Uint8Array(fs.readFileSync(path.join(REG_ROOT, name)));
}

describe("registerBasisBlob decoder (corpus)", () => {
  const runtime = loadRuntimeFixture();
  const layout = runtime.regBlob as RegBlobLayout;
  const frames = listRegisterFrames();

  it("runtime bundle ships the blob layout", () => {
    expect(layout).toBeTruthy();
    expect(layout.charset).toHaveLength(64);
    expect(layout.name_length).toBe(14);
    expect(layout.char_bits).toBe(6);
    expect(layout.blob_offset).toBe(24);
    expect(layout.blob_length).toBe(64);
    const total = layout.fields.reduce((sum, f) => sum + f.width, 0);
    expect(total).toBe(256);
  });

  it("corpus has the expected size", () => {
    expect(frames.length).toBeGreaterThanOrEqual(66);
  });

  it("decodes every register frame and matches the wire name", () => {
    for (const { label, raw } of frames) {
      const blob = sliceBlob(raw, layout);
      expect(blobKind(blob), label).toBe("register_basis");
      const basis = decodeRegisterBasisBlob(raw, layout);
      expect(basis, label).not.toBeNull();
      expect(basis!.name, label).toBe(asciiName(raw));
      expect(basis!.values["pad"], label).toBe(0);
      expect(basis!.values["tail"], label).toBe(0);
      expect(basis!.values["store_marker"], label).toBe(1);
      expect(basis!.storeCounter, label).toBeGreaterThanOrEqual(1);
      expect(basis!.storeCounter, label).toBeLessThanOrEqual(31);
    }
  });

  it("stored values equal live payload except witnessed unstored edits", () => {
    for (const { label, raw } of frames) {
      const file = label.replace(/\[\d+\]$/, "");
      const expected = (DIVERGENT[file] ?? []).slice().sort();
      const diverged = storedVsLive(raw, layout)
        .map((e) => e.id)
        .sort();
      expect(diverged, label).toEqual(expected);
    }
  });

  it("charset capture decodes &123456789ABCD", () => {
    const raw = readSample("samples/charset-b1s1-renamed.syx");
    const blob = sliceBlob(raw, layout);
    expect(decodeRegisterName(blob, layout)).toBe("&123456789ABCD");
    const codes = Array.from({ length: 14 }, (_, i) =>
      extractBits(blob, i * 6, 6),
    );
    expect(codes).toEqual([1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]);
  });

  it("stored capture carries the delay block and edited reverb time", () => {
    const raw = readSample("samples/charset-b1s1-rt5s-stored.syx");
    const basis = decodeRegisterBasisBlob(raw, layout)!;
    expect(basis.values["reverb_time"]).toBe(76); // 5.0 s, not factory 10
    expect(basis.values["delay_level"]).toBe(15);
    expect(basis.values["delay_time"]).toBe(11);
    expect(basis.values["delay_modulation"]).toBe(6);
    expect(basis.storeCounter).toBe(3);
    expect(storedVsLive(raw, layout)).toEqual([]);
  });

  it("unstored edit diverges blob vs payload", () => {
    const raw = readSample("samples/charset-b1s1-rt5s-unstored-edit.syx");
    const entries = storedVsLive(raw, layout);
    const rt = entries.find((e) => e.id === "reverb_time");
    expect(rt).toEqual({
      id: "reverb_time",
      label: "reverb time",
      stored: 10,
      live: 76,
    });
  });

  it("fullsweep store counters follow the capture history", () => {
    const data = new Uint8Array(
      fs.readFileSync(path.join(REG_ROOT, "fullsweep-rooms-studio-a.syx")),
    );
    const sweep = splitSysexMessages(data);
    expect(sweep).toHaveLength(50);
    const counters = sweep.map(
      (raw) => decodeRegisterBasisBlob(raw, layout)!.storeCounter,
    );
    expect(counters.slice(0, 3)).toEqual([3, 3, 3]);
    expect(counters.slice(3, 12)).toEqual(Array(9).fill(2));
    expect(counters.slice(12)).toEqual(Array(38).fill(1));
  });

  it("returns null for factory space-padded blobs", () => {
    const factory = new Uint8Array(
      fs.readFileSync(
        path.join(SYSEX_ROOT, "prog", "presets", "Halls.Large Hall.syx"),
      ),
    );
    expect(blobKind(sliceBlob(factory, layout))).toBe("factory_pad");
    expect(decodeRegisterBasisBlob(factory, layout)).toBeNull();
  });

  it("compiled JS Kaitai parser exposes matching blob instances", () => {
    const raw = readSample("samples/charset-b1s1-rt5s-stored.syx");
    const basis = decodeRegisterBasisBlob(raw, layout)!;
    const parsed = parseProgDump(raw) as Record<string, unknown>;
    const blob = parsed.registerBasisBlob as Record<string, unknown>;
    expect(blob.isRegisterBasis).toBe(true);
    expect(blob.tailIsZero).toBe(true);
    expect(blob.storeCounter).toBe(basis.storeCounter);
    for (const field of layout.fields) {
      if (field.id === "name" || field.id === "tail") continue;
      const key = field.id.replace(/_([a-z0-9])/g, (_, c: string) =>
        c.toUpperCase(),
      );
      expect(Number(blob[key]), field.id).toBe(basis.values[field.id]);
    }
    // Name decodes in-parser via nameCode instances.
    const blobBytes = sliceBlob(raw, layout);
    for (let i = 0; i < layout.name_length; i++) {
      const key = `nameCode${String(i).padStart(2, "0")}`;
      expect(Number(blob[key]), key).toBe(
        extractBits(blobBytes, i * layout.char_bits, layout.char_bits),
      );
    }
    // Factory dump: guard is false.
    const factory = new Uint8Array(
      fs.readFileSync(
        path.join(SYSEX_ROOT, "prog", "presets", "Halls.Large Hall.syx"),
      ),
    );
    const factoryBlob = (parseProgDump(factory) as Record<string, unknown>)
      .registerBasisBlob as Record<string, unknown>;
    expect(factoryBlob.isRegisterBasis).toBe(false);
  });
});
