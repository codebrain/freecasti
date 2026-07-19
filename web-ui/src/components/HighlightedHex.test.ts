import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { createElement } from "react";

import { HighlightedHex } from "./HighlightedHex";

describe("HighlightedHex", () => {
  it("renders every byte including ASCII spaces", () => {
    const data = new Uint8Array([0x41, 0x20, 0x20, 0x20, 0x20, 0x42]);
    const html = renderToStaticMarkup(
      createElement(HighlightedHex, {
        data,
        offsets: [0, 1, 2, 3, 4, 5],
      }),
    );
    expect(html).toContain("41");
    expect(html).toContain("20");
    expect(html).toContain("42");
    expect(html).not.toContain("(...)");
    expect((html.match(/20/g) ?? []).length).toBeGreaterThanOrEqual(4);
  });
});
