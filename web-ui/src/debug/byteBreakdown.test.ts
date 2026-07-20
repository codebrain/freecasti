import { describe, expect, it } from "vitest";
import { allProgControls, buildSystemControls } from "@/spec/controls";
import { buildByteBreakdown } from "@/debug/byteBreakdown";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("buildByteBreakdown", () => {
  const runtime = loadRuntimeFixture();
  const progControls = allProgControls(runtime.prog);
  const sysControls = buildSystemControls(runtime.system);

  it("covers every byte in a program dump", () => {
    const rows = buildByteBreakdown(runtime.templates.prog, runtime.prog, "prog", {
      controls: progControls,
      progUi: runtime.progUi,
    });
    const covered = new Set<number>();
    for (const row of rows) {
      for (const off of row.offsets) covered.add(off);
    }
    expect(covered.size).toBe(runtime.templates.prog.length);
    expect(rows.some((row) => row.label === "panel mode flag")).toBe(true);
    expect(rows.some((row) => row.label === "reverb time")).toBe(true);
    expect(rows.some((row) => row.label === "Checksum")).toBe(true);
  });

  it("covers every byte in a system dump", () => {
    const rows = buildByteBreakdown(
      runtime.templates.system,
      runtime.system,
      "system",
      { controls: sysControls },
    );
    const covered = new Set<number>();
    for (const row of rows) {
      for (const off of row.offsets) covered.add(off);
    }
    expect(covered.size).toBe(runtime.templates.system.length);
    expect(rows.some((row) => row.label === "wet gain")).toBe(true);
    expect(rows[0]?.label).toBe("SysEx start");
  });

  it("decodes program name and menu UI state", () => {
    // Spec-derived template is blank/idle; stage a name and an edit-mode
    // UI state (menu 3 = diffusion, display 41) like a hardware capture.
    const dump = new Uint8Array(runtime.templates.prog);
    dump.set(new TextEncoder().encode("Large Church"), 8);
    dump[92] = 0x00;
    dump[98] = 0x00;
    dump[99] = 0x03;
    dump[146] = 0x02;
    dump[147] = 0x09;
    const rows = buildByteBreakdown(dump, runtime.prog, "prog", {
      controls: progControls,
      progUi: runtime.progUi,
    });
    const nameRow = rows.find((row) => row.label === "program_name");
    expect(nameRow?.meaning).toBe("Large Church");
    const menuRow = rows.find((row) => row.label === "selected menu index");
    expect(menuRow?.meaning).toContain("diffusion");
    expect(menuRow?.meaning).toContain("editing");
    const cursorRow = rows.find((row) => row.label === "display");
    expect(cursorRow?.meaning).toContain("41");
    expect(cursorRow?.meaning).toContain("diffusion");
  });
});
