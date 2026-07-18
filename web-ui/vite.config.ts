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

const base = process.env.VITE_BASE_PATH ?? "./";

export default defineConfig({
  plugins: [react(), tailwindcss(), sysexParserResolve()],
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
