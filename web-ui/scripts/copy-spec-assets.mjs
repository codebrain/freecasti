import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const result = spawnSync(
  "python",
  [
    "-c",
    "from pathlib import Path; from m7_sysex.export.web_ui import sync_web_ui_assets; sync_web_ui_assets(Path('.'))",
  ],
  { cwd: repo, stdio: "inherit" },
);
if (result.status !== 0) {
  process.exit(result.status ?? 1);
}
