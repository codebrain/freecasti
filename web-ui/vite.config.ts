import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";

const root = __dirname;
const binaryStreamUmd = path.resolve(root, "src/shims/binary-stream.umd.cjs");
const binaryStreamShim = path.resolve(root, "src/shims/binary-stream.ts");

function sysexParserResolve(): Plugin {
  return {
    name: "sysex-parser-resolve",
    resolveId(source) {
      if (source === "m7/binary-stream") {
        return binaryStreamUmd;
      }
      if (source === "m7/binary-stream/shim") {
        return binaryStreamShim;
      }
      return null;
    },
  };
}

/**
 * Dev-server CJS interop. The kaitai runtime (binary-stream.umd.cjs) and the
 * generated parsers are UMD modules; @rollup/plugin-commonjs converts them in
 * production builds, but the dev server serves source files as ESM, which
 * fails with "does not provide an export named 'default'". Wrap them as ESM
 * when serving.
 */
function sysexUmdDevInterop(): Plugin {
  return {
    name: "sysex-umd-dev-interop",
    apply: "serve",
    transform(code, id) {
      const file = id.split("?")[0].replace(/\\/g, "/");
      const isRuntime = file.endsWith("/shims/binary-stream.umd.cjs");
      const isParser =
        /\/generated\/sysex-parsers\/[^/]+\.js$/.test(file) &&
        code.includes("define.amd");
      if (!isRuntime && !isParser) return null;
      const prelude = isParser
        ? 'import __BinaryStream from "../../shims/binary-stream";\n' +
          "const require = () => __BinaryStream;\n" +
          "const module = { exports: {} };\n"
        : "const module = { exports: {} };\n";
      return {
        code: `${prelude}${code}\nexport default module.exports;`,
        map: null,
      };
    },
  };
}

const base = process.env.VITE_BASE_PATH ?? "./";

export default defineConfig({
  plugins: [react(), tailwindcss(), sysexParserResolve(), sysexUmdDevInterop()],
  base,
  resolve: {
    alias: {
      "@": path.resolve(root, "./src"),
      "m7/binary-stream": path.resolve(root, "src/shims/binary-stream.umd.cjs"),
      "iconv-lite": path.resolve(root, "src/shims/iconv-lite.ts"),
      zlib: path.resolve(root, "src/shims/zlib.ts"),
    },
  },
  build: {
    target: "es2022",
    outDir: "dist",
    assetsDir: "assets",
    emptyOutDir: true,
    cssMinify: true,
    modulePreload: { polyfill: false },
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/react-dom")) return "vendor-react-dom";
          if (id.includes("node_modules/react/")) return "vendor-react";
          if (id.includes("generated/sysex-parsers")) return "sysex-parsers";
          if (
            id.includes("shims/binary-stream") ||
            id.includes("shims/iconv-lite") ||
            id.includes("shims/zlib")
          ) {
            return "sysex-runtime";
          }
        },
      },
    },
    commonjsOptions: {
      defaultIsModuleExports: true,
      include: [
        /node_modules/,
        /generated\/sysex-parsers/,
        /shims\/binary-stream\.umd\.cjs/,
      ],
    },
  },
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
});
