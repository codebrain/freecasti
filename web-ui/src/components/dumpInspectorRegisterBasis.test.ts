/**
 * @vitest-environment happy-dom
 */
import fs from "node:fs";
import path from "node:path";
import { createElement } from "react";
import { createRoot } from "react-dom/client";
import { act } from "react";
import { afterEach, describe, expect, it } from "vitest";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { buildByteBreakdown } from "@/debug/byteBreakdown";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";
import { SYSEX_ROOT } from "@/test/corpusSysex";
import { importSyxBytes } from "@/sysex/importSyx";
import { buildProgramDump } from "@/sysex/serialize";
import { verifyProgramDumpChecksum } from "@/sysex/frame";
import { decodeRegisterBasisBlob } from "@/sysex/registerBasisBlob";
import { DumpInspector } from "./DumpInspector";

(globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT =
  true;

const REG_ROOT = path.join(SYSEX_ROOT, "prog", "edit", "registers");

function readSample(name: string): Uint8Array {
  return new Uint8Array(fs.readFileSync(path.join(REG_ROOT, name)));
}

describe("DumpInspector register basis (end to end)", () => {
  const runtime = loadRuntimeFixture();
  const regBlob = runtime.regBlob!;
  const progControls = allProgControls(runtime.prog);
  const sysControls = buildSystemControls(runtime.system);

  let container: HTMLDivElement | null = null;
  let root: ReturnType<typeof createRoot> | null = null;

  afterEach(() => {
    if (root) {
      act(() => {
        root!.unmount();
      });
    }
    container?.remove();
    container = null;
    root = null;
  });

  async function renderInspector(bytes: Uint8Array): Promise<HTMLDivElement> {
    container = document.createElement("div");
    document.body.appendChild(container);
    root = createRoot(container);
    await act(async () => {
      root!.render(
        createElement(DumpInspector, {
          bytes,
          progSpec: runtime.prog,
          progControls,
          sysControls,
          progUi: runtime.progUi,
          regBlob,
        }),
      );
    });
    return container;
  }

  it("renders decoded basis with a divergence flag on the unstored-edit capture", async () => {
    const raw = readSample("samples/charset-b1s1-rt5s-unstored-edit.syx");
    const basis = decodeRegisterBasisBlob(raw, regBlob)!;
    const el = await renderInspector(raw);

    const section = el.querySelector('[data-testid="register-basis-section"]');
    expect(section).not.toBeNull();
    const text = section!.textContent ?? "";
    expect(text).toContain("Register basis");
    expect(text).toContain(basis.name);
    expect(text).toContain(`store #${basis.storeCounter}`);
    // reverb time + 3 delay fields were edited after the store.
    expect(text).toContain("4 unstored edits");
    expect(text).toContain("unstored edit");
    expect(text).toContain("reverb time");
  });

  it("renders a clean basis (no divergence) on the stored capture", async () => {
    const raw = readSample("samples/charset-b1s1-rt5s-stored.syx");
    const basis = decodeRegisterBasisBlob(raw, regBlob)!;
    const el = await renderInspector(raw);

    const section = el.querySelector('[data-testid="register-basis-section"]');
    expect(section).not.toBeNull();
    const text = section!.textContent ?? "";
    expect(text).toContain(basis.name);
    expect(text).not.toContain("unstored edit");
  });

  it("omits the section for factory dumps", async () => {
    const factory = new Uint8Array(
      fs.readFileSync(
        path.join(SYSEX_ROOT, "prog", "presets", "Halls.Large Hall.syx"),
      ),
    );
    const el = await renderInspector(factory);
    expect(
      el.querySelector('[data-testid="register-basis-section"]'),
    ).toBeNull();
  });

  it("byte breakdown emits blob sub-rows with stored values and divergences", () => {
    const raw = readSample("samples/charset-b1s1-rt5s-unstored-edit.syx");
    const basis = decodeRegisterBasisBlob(raw, regBlob)!;
    const rows = buildByteBreakdown(raw, runtime.prog, "prog", {
      controls: progControls,
      progUi: runtime.progUi,
      regBlob,
    });
    const blobRow = rows.find((row) => row.offsets.includes(24))!;
    expect(blobRow.meaning).toContain(basis.name);
    expect(blobRow.meaning).toContain(`store #${basis.storeCounter}`);
    const subRows = blobRow.subRows!;
    expect(subRows.length).toBeGreaterThanOrEqual(20);
    const nameRow = subRows.find((r) => r.label.startsWith("name"))!;
    expect(nameRow.meaning).toBe(`"${basis.name}"`);
    const counterRow = subRows.find((r) =>
      r.label.startsWith("store counter"),
    )!;
    expect(counterRow.meaning).toContain(String(basis.storeCounter));
    const rtRow = subRows.find((r) => r.label.startsWith("reverb time"))!;
    expect(rtRow.meaning).toContain("unstored edit");
    expect(rtRow.meaning).toContain("live:");
  });

  it("import -> serialize keeps the blob byte-identical with a valid checksum", () => {
    const raw = readSample("samples/charset-b1s1-rt5s-stored.syx");
    const imported = importSyxBytes(raw, runtime.prog, progControls, sysControls);
    expect(imported.family).toBe("prog");
    const rebuilt = buildProgramDump(
      imported.progState!,
      runtime.prog.fields,
      raw,
      runtime.progUi,
    );
    expect(rebuilt.length).toBe(raw.length);
    for (let i = regBlob.blob_offset; i < regBlob.blob_offset + regBlob.blob_length; i++) {
      expect(rebuilt[i], `offset ${i}`).toBe(raw[i]);
    }
    expect(verifyProgramDumpChecksum(rebuilt)).toBe(true);
    expect(decodeRegisterBasisBlob(rebuilt, regBlob)).toEqual(
      decodeRegisterBasisBlob(raw, regBlob),
    );
  });
});
