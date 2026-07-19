import fs from "node:fs";
import path from "node:path";
import { repoRoot } from "@/test/presetFixtures";
import { expandRuntimeBundle } from "@/runtime/expandRuntime";

export function loadRuntimeFixture() {
  const raw = JSON.parse(
    fs.readFileSync(
      path.join(repoRoot, "web-ui/public/m7-runtime.json"),
      "utf8",
    ),
  );
  return expandRuntimeBundle(raw);
}
