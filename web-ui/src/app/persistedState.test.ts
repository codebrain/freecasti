import { describe, expect, it } from "vitest";
import {
  loadActiveTab,
  loadLockedFields,
  loadRestoredProgState,
  loadStoredAbStore,
  loadTempoModeFields,
} from "@/app/persistedState";
import { LS_LOCKED, LS_PROG, LS_PROG_AB, LS_TAB, LS_TEMPO_MODE } from "@/app/storageKeys";
import { makeMemoryStorage } from "@/test/memoryStorage";
import type { ProgAbStore } from "@/presets/progAbSlot";

describe("persistedState", () => {
  it("loads tempo mode field ids from JSON array", () => {
    const storage = makeMemoryStorage();
    storage.setItem(LS_TEMPO_MODE, JSON.stringify(["reverb_time", "predelay"]));
    expect(loadTempoModeFields(storage)).toEqual(
      new Set(["reverb_time", "predelay"]),
    );
  });

  it("returns empty sets for invalid JSON", () => {
    const storage = makeMemoryStorage();
    storage.setItem(LS_LOCKED, "not-json");
    expect(loadLockedFields(storage)).toEqual(new Set());
  });

  it("parses stored A/B store via parseStoredAbStore", () => {
    const storage = makeMemoryStorage();
    const store: ProgAbStore = {
      active: "a",
      a: { bankIdx: 0, presetSlot: 1, state: { programName: "A", encoded: {} } },
      b: { bankIdx: 0, presetSlot: 2, state: { programName: "B", encoded: {} } },
    };
    storage.setItem(LS_PROG_AB, JSON.stringify(store));
    expect(loadStoredAbStore(storage)?.active).toBe("a");
  });

  it("loads active tab with system fallback", () => {
    const storage = makeMemoryStorage();
    storage.setItem(LS_TAB, "system");
    expect(loadActiveTab(storage)).toBe("system");
    storage.setItem(LS_TAB, "bogus");
    expect(loadActiveTab(storage)).toBe("prog");
  });

  it("loads restored prog state JSON", () => {
    const storage = makeMemoryStorage();
    storage.setItem(
      LS_PROG,
      JSON.stringify({ programName: "Hall", encoded: { bank_index: 0 } }),
    );
    expect(loadRestoredProgState(storage)?.programName).toBe("Hall");
  });
});
