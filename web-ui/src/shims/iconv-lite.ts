/** Browser shim for the generated parser runtime's optional Node ``iconv-lite`` require. */

function toBytes(buf: ArrayLike<number> | Uint8Array): Uint8Array {
  return buf instanceof Uint8Array ? buf : Uint8Array.from(buf);
}

export function decode(buf: ArrayLike<number> | Uint8Array, encoding: string): string {
  const bytes = toBytes(buf);
  const enc = encoding.toLowerCase();
  if (enc === "ascii" || enc === "latin1" || enc === "iso-8859-1") {
    return String.fromCharCode(...bytes);
  }
  return new TextDecoder(encoding).decode(bytes);
}

export default { decode };
