import { SYSEX_END, SYSEX_START } from "./frame";

export function parseSyxBytes(data: Uint8Array): Uint8Array {
  if (!data.length) {
    throw new Error("empty SysEx file");
  }
  if (data[0] !== SYSEX_START || data[data.length - 1] !== SYSEX_END) {
    throw new Error("not a SysEx file (expected F0 … F7)");
  }
  return data;
}

export async function readSyxFromFile(file: Blob): Promise<Uint8Array> {
  const buf = await file.arrayBuffer();
  return parseSyxBytes(new Uint8Array(buf));
}

export function readSyxFromBuffer(buffer: ArrayBufferLike | Uint8Array): Uint8Array {
  const data = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  return parseSyxBytes(data);
}

export function bytesToBase64(bytes: Uint8Array): string {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(bytes).toString("base64");
  }
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

export function base64ToBytes(b64: string): Uint8Array {
  if (typeof Buffer !== "undefined") {
    return new Uint8Array(Buffer.from(b64, "base64"));
  }
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

export function suggestSyxFilename(
  family: "prog" | "system",
  programName?: string,
): string {
  if (family === "prog" && programName) {
    const safe = programName.replace(/[^\w .-]+/g, "").trim();
    if (safe) return `${safe}.syx`;
  }
  return family === "prog" ? "m7-program.syx" : "m7-system.syx";
}

export interface DownloadSyxOptions {
  bytes: Uint8Array;
  filename: string;
  createObjectURL?: (blob: Blob) => string;
  revokeObjectURL?: (url: string) => void;
  createAnchor?: () => HTMLAnchorElement;
  clickLink?: (anchor: HTMLAnchorElement) => void;
}

/** Trigger a browser download of a .syx blob (injectable for tests). */
export function downloadSyx({
  bytes,
  filename,
  createObjectURL = URL.createObjectURL.bind(URL),
  revokeObjectURL = URL.revokeObjectURL.bind(URL),
  createAnchor = () => document.createElement("a"),
  clickLink = (a) => a.click(),
}: DownloadSyxOptions): void {
  // Copy so the part is a Uint8Array<ArrayBuffer> (BlobPart rejects
  // ArrayBufferLike-backed views under TS 5.7 typed-array generics).
  const blob = new Blob([new Uint8Array(bytes)], {
    type: "application/octet-stream",
  });
  const url = createObjectURL(blob);
  const a = createAnchor();
  a.href = url;
  a.download = filename;
  clickLink(a);
  revokeObjectURL(url);
}
