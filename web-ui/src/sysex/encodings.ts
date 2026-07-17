export function nibbleHilo(b0: number, b1: number): number {
  return ((b0 & 0x0f) << 4) | (b1 & 0x0f);
}

export function nibbleLohi(b0: number, b1: number): number {
  return (b0 & 0x0f) | ((b1 & 0x0f) << 4);
}

export function midi14Be(b0: number, b1: number): number {
  return ((b0 & 0x7f) << 7) | (b1 & 0x7f);
}

export function midi14Le(b0: number, b1: number): number {
  return (b0 & 0x7f) | ((b1 & 0x7f) << 7);
}

export function encodeAtOffsets(
  encoded: number,
  encoding: string,
  nOffsets = 1,
): number[] {
  const enc = encoded | 0;
  switch (encoding) {
    case "raw_u8":
      if (nOffsets !== 1) throw new Error("raw_u8 expects 1 offset");
      return [enc & 0xff];
    case "nibble_hilo":
      if (nOffsets !== 2) throw new Error("nibble_hilo expects 2 offsets");
      return [(enc >> 4) & 0x0f, enc & 0x0f];
    case "nibble_lohi":
      if (nOffsets !== 2) throw new Error("nibble_lohi expects 2 offsets");
      return [enc & 0x0f, (enc >> 4) & 0x0f];
    case "midi14_be":
      if (nOffsets !== 2) throw new Error("midi14_be expects 2 offsets");
      return [(enc >> 7) & 0x7f, enc & 0x7f];
    case "midi14_le":
      if (nOffsets !== 2) throw new Error("midi14_le expects 2 offsets");
      return [enc & 0x7f, (enc >> 7) & 0x7f];
    case "raw_bytes": {
      const width = Math.max(1, nOffsets);
      const out = new Array<number>(width).fill(0);
      let v = enc;
      for (let i = width - 1; i >= 0; i--) {
        out[i] = v & 0xff;
        v >>= 8;
      }
      return out;
    }
    default:
      throw new Error(`unknown encoding: ${encoding}`);
  }
}

export function decodeAtOffsets(
  data: Uint8Array,
  offsets: number[],
  encoding: string,
): number {
  const raw = offsets.map((o) => data[o]);
  switch (encoding) {
    case "raw_u8":
      return raw[0];
    case "nibble_hilo":
      return nibbleHilo(raw[0], raw[1]);
    case "nibble_lohi":
      return nibbleLohi(raw[0], raw[1]);
    case "midi14_be":
      return midi14Be(raw[0], raw[1]);
    case "midi14_le":
      return midi14Le(raw[0], raw[1]);
    case "raw_bytes": {
      let v = 0;
      for (const b of raw) v = (v << 8) | b;
      return v;
    }
    default:
      throw new Error(`unknown encoding: ${encoding}`);
  }
}
