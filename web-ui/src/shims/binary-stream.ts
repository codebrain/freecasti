/**
 * ESM wrapper around the vendored binary stream UMD build.
 */
// @ts-expect-error UMD build has no types
import * as streamMod from "./binary-stream.umd.js";

const BinaryStream =
  (streamMod as { default?: typeof streamMod }).default ?? streamMod;

export { BinaryStream };
export default BinaryStream;
