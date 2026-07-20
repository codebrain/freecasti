import BinaryStreamModule from "./binary-stream.umd.cjs";

// The UMD build has no typings; byteOffset is optional at runtime.
type BinaryStreamConstructor = new (
  buffer: ArrayBuffer | Uint8Array,
  byteOffset?: number,
) => unknown;

const BinaryStream = ((BinaryStreamModule as { default?: unknown }).default ??
  BinaryStreamModule) as BinaryStreamConstructor;

export { BinaryStream };
export default BinaryStream;
