/** Stub — M7 SysEx dumps do not use zlib; the parser runtime only needs this in Node. */

export function inflateSync(): never {
  throw new Error("zlib is not available in the browser");
}

export default { inflateSync };
