import { describe, expect, it } from "vitest";
import { expandCompactSpec, isCompactSpec } from "@/spec/compact";

describe("expandCompactSpec", () => {
  it("expands tuple value maps and short encodings", () => {
    const raw = {
      n: 10,
      f: [
        { id: "reverb_time", s: 100, e: "nh", p: "reverb time", m: [[40, "2.2 s"]] },
        { id: "program_name", s: 8, e: "as", z: 16 },
      ],
    };
    expect(isCompactSpec(raw)).toBe(true);
    const spec = expandCompactSpec(raw);
    expect(spec.message_length).toBe(10);
    expect(spec.fields[0].encoding).toBe("nibble_hilo");
    expect(spec.fields[0].value_map?.entries[0]).toEqual({
      encoded: 40,
      label: "2.2 s",
    });
    expect(spec.fields[1].end).toBe(23);
  });
});
