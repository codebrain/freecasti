import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../..",
);
export const SYSEX_ROOT = path.join(repo, "sysex");

/** Mirrors ``m7_sysex.types.is_prog_corpus_relative``. */
export function isProgCorpusRelative(rel: string): boolean {
  const parts = rel.replace(/\\/g, "/").split("/");
  if (!parts.length) return false;
  if (parts[0] === "prog") {
    if (parts.length < 2) return false;
    if (
      parts[1] === "edit" ||
      parts[1] === "full sweep" ||
      parts[1] === "menus" ||
      parts[1] === "_edit"
    ) {
      return false;
    }
    return true;
  }
  if (parts[0]?.startsWith("_") && parts[0] !== "_presets") return false;
  return parts[0] !== "_system" && parts[0] !== "system";
}

function walkSyx(dir: string, prefix: string, out: string[]): void {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const rel = prefix ? `${prefix}/${name}` : name;
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      walkSyx(full, rel, out);
      continue;
    }
    if (name.endsWith(".syx")) out.push(rel.replace(/\\/g, "/"));
  }
}

export function listProgCorpusDumps(): string[] {
  const found: string[] = [];
  walkSyx(SYSEX_ROOT, "", found);
  return found.filter(isProgCorpusRelative).sort();
}

export function listSystemDumps(): string[] {
  const found: string[] = [];
  walkSyx(path.join(SYSEX_ROOT, "system"), "system", found);
  return found
    .filter((rel) => !rel.split("/").includes("_system"))
    .sort();
}

export function listProgMenuDumps(): string[] {
  const menusDir = path.join(SYSEX_ROOT, "prog", "menus");
  if (!fs.existsSync(menusDir)) return [];
  return fs
    .readdirSync(menusDir)
    .filter((name) => name.endsWith(".syx"))
    .map((name) => `prog/menus/${name}`)
    .sort();
}

export function readSysexDump(rel: string): Uint8Array {
  return new Uint8Array(fs.readFileSync(path.join(SYSEX_ROOT, rel)));
}
