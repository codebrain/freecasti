import {
  verifyProgramDumpChecksum,
  verifySystemDumpChecksum,
} from "./frame";

export interface VerifyResult {
  checksumOk: boolean;
  parseError: string | null;
  parseSummary: string | null;
}

function formatParseError(err: unknown): string {
  const raw = err instanceof Error ? err.message : String(err);
  return raw
    .replace(/BinaryStream\./g, "")
    .replace(/Validation\w+Error/g, "validation error")
    .trim();
}

async function loadBinaryStream() {
  const mod = await import("@/shims/binary-stream");
  return mod.default;
}

async function parseDumpStructure(
  bytes: Uint8Array,
  family: "prog" | "system",
): Promise<{ summary: string | null; error: string | null }> {
  try {
    const Stream = await loadBinaryStream();
    const mod = await import("@/generated/sysex-parsers/index.js");
    if (family === "prog" && mod.M7ProgramDump) {
      const buf =
        bytes.buffer instanceof ArrayBuffer
          ? bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
          : bytes;
      const parsed = new mod.M7ProgramDump(new Stream(buf));
      const name = String(parsed.program_name ?? "").replace(/\s+$/, "");
      return { summary: `program "${name}" (${bytes.length} B)`, error: null };
    }
    if (family === "system" && mod.M7SystemDump) {
      const buf =
        bytes.buffer instanceof ArrayBuffer
          ? bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
          : bytes;
      new mod.M7SystemDump(new Stream(buf));
      return { summary: `system dump (${bytes.length} B)`, error: null };
    }
    return { summary: `${family} dump (${bytes.length} B)`, error: null };
  } catch (err) {
    return {
      summary: null,
      error: formatParseError(err),
    };
  }
}

export async function verifyDump(
  bytes: Uint8Array,
  family: "prog" | "system",
): Promise<VerifyResult> {
  const checksumOk =
    family === "prog"
      ? verifyProgramDumpChecksum(bytes)
      : verifySystemDumpChecksum(bytes);

  const { summary, error } = await parseDumpStructure(bytes, family);
  return {
    checksumOk,
    parseError: error,
    parseSummary: summary,
  };
}
