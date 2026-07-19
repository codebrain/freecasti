import { describe, expect, it } from "vitest";
import {
  DEFAULT_ALGORITHM_CONSTRAINTS,
  algorithmConstraintsFrom,
  isNonLinBank,
  isParameterActive,
} from "./algorithms";

describe("program algorithms", () => {
  it("identifies NonLin bank", () => {
    expect(isNonLinBank(10)).toBe(true);
    expect(isNonLinBank(0)).toBe(false);
  });

  it("falls back when catalog algorithms are missing or empty", () => {
    expect(algorithmConstraintsFrom(null)).toEqual(DEFAULT_ALGORITHM_CONSTRAINTS);
    expect(algorithmConstraintsFrom({ algorithms: {} })).toEqual(
      DEFAULT_ALGORITHM_CONSTRAINTS,
    );
    expect(
      algorithmConstraintsFrom({
        algorithms: { nonlin: { bank_index: 10, params: [] } },
      }),
    ).toEqual(DEFAULT_ALGORITHM_CONSTRAINTS);
  });

  it("uses catalog algorithms when present", () => {
    const custom = {
      nonlin: { bank_index: 10, params: ["size"] as string[] },
    };
    expect(algorithmConstraintsFrom({ algorithms: custom })).toEqual(custom);
  });

  it("allows only NonLin parameters on bank 10", () => {
    const c = DEFAULT_ALGORITHM_CONSTRAINTS;
    expect(isParameterActive(10, "size", c)).toBe(true);
    expect(isParameterActive(10, "predelay", c)).toBe(true);
    expect(isParameterActive(10, "rolloff", c)).toBe(true);
    expect(isParameterActive(10, "early select", c)).toBe(true);
    expect(isParameterActive(10, "early to reverb mix", c)).toBe(true);
    expect(isParameterActive(10, "early rolloff", c)).toBe(true);
    expect(isParameterActive(10, "reverb time", c)).toBe(false);
    expect(isParameterActive(10, "diffusion", c)).toBe(false);
    expect(isParameterActive(10, "delay time", c)).toBe(false);
    expect(isParameterActive(10, "lf rt crossover", c)).toBe(false);
  });

  it("allows all parameters on classic banks", () => {
    expect(isParameterActive(0, "reverb time")).toBe(true);
    expect(isParameterActive(6, "delay time")).toBe(true);
  });
});
