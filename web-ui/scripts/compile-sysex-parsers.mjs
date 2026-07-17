import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";

const require = createRequire(import.meta.url);
const StructCompiler = require("m7-sysex-compiler");

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repo = path.resolve(root, "..");
const outDir = path.join(root, "src", "generated", "sysex-parsers");
const specs = [
  {
    ksy: path.join(repo, "specification", "prog", "m7_program_dump.ksy"),
    exportName: "M7ProgramDump",
  },
  {
    ksy: path.join(repo, "specification", "system", "m7_system_dump.ksy"),
    exportName: "M7SystemDump",
  },
];

fs.mkdirSync(outDir, { recursive: true });

function sanitizeParserJs(content) {
  return content
    .replace(
      /^\/\/ This is a generated file[^\n]*\n\n/m,
      "// Generated SysEx parser — edit .ksy specs and run npm run compile-parsers\n\n",
    )
    .replace(/kaitai-struct\/KaitaiStream/g, "m7/binary-stream")
    .replace(/\bKaitaiStream\b/g, "BinaryStream");
}

const compiler = new StructCompiler();
const written = new Set();

for (const { ksy, exportName } of specs) {
  if (!fs.existsSync(ksy)) {
    console.error(`Missing ${ksy} — run python run.py from repo root first.`);
    process.exit(1);
  }
  const ksyObj = parseYaml(fs.readFileSync(ksy, "utf8"));
  const files = await compiler.compile("javascript", ksyObj, null, false);
  for (const [name, content] of Object.entries(files)) {
    const outPath = path.join(outDir, name);
    fs.writeFileSync(outPath, sanitizeParserJs(content));
    written.add(name);
    console.log("wrote", name);
  }
  if (![...written].some((n) => n.includes(exportName))) {
    console.warn(`expected output for ${exportName} from ${ksy}`);
  }
}

const jsFiles = [...written].filter((n) => n.endsWith(".js"));
const indexLines = jsFiles.map((name) => {
  const base = name.replace(/\.js$/, "");
  return `import ${base}Mod from './${base}.js';\nexport const ${base} = ${base}Mod.default ?? ${base}Mod;`;
});
fs.writeFileSync(path.join(outDir, "index.js"), indexLines.join("\n") + "\n");
console.log("SysEx parsers written to", outDir);
