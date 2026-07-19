import { describe, expect, it } from "vitest";
import { specIdToParserKey } from "@/sysex/kaitaiFieldId";

describe("specIdToParserKey", () => {
  it("maps snake_case ids to Kaitai JavaScript property names", () => {
    expect(specIdToParserKey("program_name")).toBe("programName");
    expect(specIdToParserKey("display")).toBe("display");
    expect(specIdToParserKey("sysex_start")).toBe("sysexStart");
  });
});
