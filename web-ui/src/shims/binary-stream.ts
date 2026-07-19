import BinaryStreamModule from "./binary-stream.umd.cjs";

const BinaryStream =
  (BinaryStreamModule as { default?: typeof BinaryStreamModule }).default ??
  BinaryStreamModule;

export { BinaryStream };
export default BinaryStream;
