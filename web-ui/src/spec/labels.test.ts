import { describe, expect, it } from "vitest";
import {
  displayParameterLabel,
  formatEarlyLateMixLabel,
  formatValueLabel,
} from "./labels";

describe("displayParameterLabel", () => {
  it("overrides known parameter names", () => {
    expect(displayParameterLabel("early to reverb mix", "early to reverb mix")).toBe(
      "Early/Late",
    );
    expect(displayParameterLabel("modulation", "modulation")).toBe("MOD");
    expect(displayParameterLabel("early rolloff", "early rolloff")).toBe("Early");
    expect(displayParameterLabel("audio routing", "audio routing")).toBe("Routing");
    expect(displayParameterLabel("display level", "display level")).toBe("Display");
  });

  it("never uses roll-off spelling", () => {
    expect(displayParameterLabel(undefined, "early roll-off")).toBe("early rolloff");
  });
});

describe("formatEarlyLateMixLabel", () => {
  it("converts A/B sides to complementary percentages", () => {
    expect(formatEarlyLateMixLabel("0/20")).toBe("0% / 100%");
    expect(formatEarlyLateMixLabel("20/0")).toBe("100% / 0%");
    expect(formatEarlyLateMixLabel("20/20")).toBe("50% / 50%");
    expect(formatEarlyLateMixLabel("20/10")).toBe("67% / 33%");
    expect(formatEarlyLateMixLabel("10/20")).toBe("33% / 67%");
  });

  it("rejects invalid mix labels", () => {
    expect(formatEarlyLateMixLabel("")).toBeNull();
    expect(formatEarlyLateMixLabel("20")).toBeNull();
    expect(formatEarlyLateMixLabel("21/0")).toBeNull();
    expect(formatEarlyLateMixLabel("0/21")).toBeNull();
    expect(formatEarlyLateMixLabel("not-a-mix")).toBeNull();
  });

  it("handles zero-total edge case", () => {
    expect(formatEarlyLateMixLabel("0/0")).toBe("0% / 0%");
  });
});

describe("formatValueLabel", () => {
  it("title-cases lowercase enum words", () => {
    expect(formatValueLabel("off")).toBe("Off");
    expect(formatValueLabel("low")).toBe("Low");
    expect(formatValueLabel("full")).toBe("Full");
    expect(formatValueLabel("mono l")).toBe("Mono L");
    expect(formatValueLabel("stereo")).toBe("Stereo");
  });

  it("formats early/late mix as percentages", () => {
    expect(formatValueLabel("0/20", "early to reverb mix")).toBe("0% / 100%");
    expect(formatValueLabel("20/0", "early to reverb mix")).toBe("100% / 0%");
    expect(formatValueLabel("20/20", "early to reverb mix")).toBe("50% / 50%");
    expect(formatValueLabel("20/10", "early to reverb mix")).toBe("67% / 33%");
    expect(formatValueLabel("10/20", "early to reverb mix")).toBe("33% / 67%");
    expect(formatValueLabel("20/13", "early to reverb mix")).toBe("61% / 39%");
  });

  it("leaves early/late mix labels unchanged for other parameters", () => {
    expect(formatValueLabel("20/10", "size")).toBe("20/10");
  });

  it("leaves other numeric and unit labels unchanged", () => {
    expect(formatValueLabel("2.2 s")).toBe("2.2 s");
    expect(formatValueLabel("1.0 s")).toBe("1.0 s");
    expect(formatValueLabel("-60 dB")).toBe("-60 dB");
  });

  it("displays sub-second times as milliseconds", () => {
    expect(formatValueLabel("0.2 s")).toBe("200 ms");
    expect(formatValueLabel("0.5 s")).toBe("500 ms");
    expect(formatValueLabel("0.95 s")).toBe("950 ms");
    expect(formatValueLabel("500 ms")).toBe("500 ms");
    expect(formatValueLabel("0 ms")).toBe("0 ms");
  });

  it("formats reverb time bare seconds from the spec table", () => {
    expect(formatValueLabel("0.2", "reverb time")).toBe("200 ms");
    expect(formatValueLabel("0.95", "reverb time")).toBe("950 ms");
    expect(formatValueLabel("2.2", "reverb time")).toBe("2.2 s");
    expect(formatValueLabel("30", "reverb time")).toBe("30 s");
    expect(formatValueLabel("2.2", "size")).toBe("2.2");
  });

  it("leaves already cased names unchanged", () => {
    expect(formatValueLabel("Halls")).toBe("Halls");
    expect(formatValueLabel("NonLin")).toBe("NonLin");
    expect(formatValueLabel("Edit (receive)")).toBe("Edit (Receive)");
  });

  it("appends x suffix for multiply parameters", () => {
    expect(formatValueLabel("1", "lf rt multiply")).toBe("1x");
    expect(formatValueLabel("0.5", "hf rt multiply")).toBe("0.5x");
    expect(formatValueLabel("4", "lf rt multiply")).toBe("4x");
    expect(formatValueLabel("1", "size")).toBe("1");
  });
});
