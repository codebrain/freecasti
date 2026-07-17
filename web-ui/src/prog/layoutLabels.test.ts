import { describe, expect, it } from "vitest";
import {
  delayControlLabel,
  partitionProgGroups,
  shortSubgroupLabel,
} from "@/prog/layoutLabels";
import type { ControlGroup } from "@/spec/controls";
import { buildProgControlGroups } from "@/spec/controls";
import { loadProgSpec } from "@/test/presetFixtures";

describe("layoutLabels", () => {
  it("strips subgroup prefixes from labels", () => {
    expect(shortSubgroupLabel("LF RT", "LF RT crossover")).toBe("crossover");
  });

  it("shortens delay modulation to MOD", () => {
    expect(delayControlLabel("delay modulation")).toBe("MOD");
    expect(delayControlLabel("delay time")).toBe("time");
  });

  it("partitions groups into core, trio, and remainder", () => {
    const groups = buildProgControlGroups(loadProgSpec());
    const { core, trio, fddt, remainder } = partitionProgGroups(groups);
    expect(core?.title).toBe("Core");
    expect(trio.map((g) => g.title)).toEqual(["Reflections", "Rolloff", "Delay"]);
    expect(fddt?.title).toBe("Frequency Dependent Decay Time");
    expect(remainder).toHaveLength(0);
  });

  it("handles missing core group", () => {
    const groups: ControlGroup[] = [{ title: "Delay", controls: [] }];
    const { core, trio } = partitionProgGroups(groups);
    expect(core).toBeUndefined();
    expect(trio).toHaveLength(1);
  });
});
