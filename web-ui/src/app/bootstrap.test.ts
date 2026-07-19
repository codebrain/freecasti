import { describe, expect, it } from "vitest";
import { bootstrapAppState } from "@/app/bootstrap";
import { makeMemoryStorage } from "@/test/memoryStorage";
import { loadRuntimeFixture } from "@/test/runtimeFixtures";

describe("bootstrapAppState", () => {
  it("creates default A/B store and system state on empty storage", () => {
    const runtime = loadRuntimeFixture();
    const storage = makeMemoryStorage();
    const result = bootstrapAppState(runtime.prog, runtime.system, runtime.presets, storage);
    expect(result.abStore.active).toBe("a");
    expect(result.abStore.a.state.programName).toBeTruthy();
    expect(Object.keys(result.sysState).length).toBeGreaterThan(0);
  });

  it("restores persisted A/B store when present", () => {
    const runtime = loadRuntimeFixture();
    const storage = makeMemoryStorage();
    const custom = {
      active: "b" as const,
      a: {
        bankIdx: 0,
        presetSlot: 0,
        state: { programName: "Slot A", encoded: { bank_index: 0, program_slot: 0 } },
      },
      b: {
        bankIdx: 0,
        presetSlot: 1,
        state: { programName: "Slot B", encoded: { bank_index: 0, program_slot: 1 } },
      },
    };
    storage.setItem("m7.state.progAb", JSON.stringify(custom));
    const result = bootstrapAppState(runtime.prog, runtime.system, runtime.presets, storage);
    expect(result.abStore.active).toBe("b");
    expect(result.abStore.b.state.programName).toBe("Slot B");
  });
});
