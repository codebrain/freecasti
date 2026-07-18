import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readSyxFromBuffer } from "@/sysex/syxIo";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);

export function loadMenuSyx(name: string): Uint8Array {
  const file = path.join(repo, "sysex/prog/menus", `${name}.syx`);
  return readSyxFromBuffer(fs.readFileSync(file));
}
