import { describe, expect, it } from "vitest";

import { tokenizeHexOffsets } from "./HighlightedHex";

describe("tokenizeHexOffsets", () => {
  it("collapses long ASCII space runs", () => {
    const data = new Uint8Array([0x41, 0x20, 0x20, 0x20, 0x20, 0x42]);
    expect(tokenizeHexOffsets(data, [0, 1, 2, 3, 4, 5])).toEqual([
      { kind: "byte", index: 0 },
      { kind: "space_run", indices: [1, 2, 3, 4] },
      { kind: "byte", index: 5 },
    ]);
  });

  it("keeps short space runs expanded", () => {
    const data = new Uint8Array([0x41, 0x20, 0x20, 0x42]);
    expect(tokenizeHexOffsets(data, [0, 1, 2, 3])).toEqual([
      { kind: "byte", index: 0 },
      { kind: "byte", index: 1 },
      { kind: "byte", index: 2 },
      { kind: "byte", index: 3 },
    ]);
  });
});
