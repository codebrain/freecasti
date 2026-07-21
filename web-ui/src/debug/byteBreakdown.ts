import type { ProgUiRuntime } from "@/prog/uiState";
import { decodeProgUiFromBytes } from "@/prog/uiState";
import type { ControlDef } from "@/spec/controls";
import { labelForEncoded } from "@/debug/change";
import { formatValueLabel } from "@/spec/labels";
import type { DumpSpec, SpecField } from "@/spec/types";
import { decodeAtOffsets } from "@/sysex/encodings";
import {
  BRICASTI_MFR_ID,
  PROGRAM_DUMP_HEADER,
  SYSTEM_DUMP_HEADER,
  SYSEX_END,
  SYSEX_START,
} from "@/sysex/frame";
import type { ActiveTab } from "@/hooks/useSysexOutput";
import type { RegBlobLayout } from "@/sysex/registerBasisBlob";
import {
  decodeRegisterBasisBlob,
  payloadValue,
} from "@/sysex/registerBasisBlob";

export interface ByteBreakdownSubRow {
  label: string;
  meaning: string;
}

export interface ByteBreakdownRow {
  start: number;
  end: number;
  offsets: number[];
  label: string;
  meaning: string;
  subRows?: ByteBreakdownSubRow[];
}

interface Region {
  start: number;
  end: number;
  label: string;
  meaning: string;
  subRows?: ByteBreakdownSubRow[];
}

function range(start: number, end: number): number[] {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

function overlaps(a: Region, start: number, end: number): boolean {
  return a.start <= end && a.end >= start;
}

function readAscii(data: Uint8Array, start: number, length: number): string {
  const slice = data.subarray(start, start + length);
  return new TextDecoder("ascii")
    .decode(slice)
    .replace(/\0/g, "")
    .replace(/\s+$/, "");
}

function decodeFieldMeaning(
  field: SpecField,
  data: Uint8Array,
  control?: ControlDef,
): string {
  if (field.encoding === "ascii_space_padded") {
    const text = readAscii(data, field.start, field.size ?? field.end - field.start + 1);
    return text || "(blank)";
  }
  if (field.encoding === "raw_bytes" || field.id === "register_basis_blob") {
    const length = field.size ?? field.end - field.start + 1;
    const slice = data.subarray(field.start, field.start + length);
    if (slice.every((b) => b === 0x20)) return "factory spaces (0x20)";
    if (slice.every((b) => b <= 0x0f)) return `nibbles (${length} B)`;
    return `${length} B`;
  }
  const encoding = field.encoding ?? "raw_u8";
  const encoded = decodeAtOffsets(data, field.offsets, encoding);
  if (control) {
    return labelForEncoded(control, encoded);
  }
  const entry = field.value_map?.entries.find((e) => e.encoded === encoded);
  if (entry) {
    return formatValueLabel(entry.label, field.parameter);
  }
  return String(encoded);
}

function frameRegions(family: ActiveTab): Region[] {
  const header =
    family === "prog"
      ? Array.from(PROGRAM_DUMP_HEADER)
      : Array.from(SYSTEM_DUMP_HEADER);
  return [
    {
      start: 0,
      end: 0,
      label: "SysEx start",
      meaning: `0x${SYSEX_START.toString(16).toUpperCase()}`,
    },
    {
      start: 1,
      end: 3,
      label: "Manufacturer ID",
      meaning: `Bricasti (${Array.from(BRICASTI_MFR_ID)
        .map((b) => b.toString(16).toUpperCase().padStart(2, "0"))
        .join(" ")})`,
    },
    {
      start: 4,
      end: 7,
      label: family === "prog" ? "Program dump header" : "System dump header",
      meaning: header
        .map((b) => b.toString(16).toUpperCase().padStart(2, "0"))
        .join(" "),
    },
  ];
}

function trailerRegions(family: ActiveTab): Region[] {
  if (family === "prog") {
    return [
      {
        start: 152,
        end: 155,
        label: "Checksum",
        meaning: "CRC16 ARC (nibbles)",
      },
      {
        start: 156,
        end: 156,
        label: "SysEx end",
        meaning: `0x${SYSEX_END.toString(16).toUpperCase()}`,
      },
    ];
  }
  return [
    {
      start: 72,
      end: 75,
      label: "Checksum",
      meaning: "CRC16 ARC (nibbles)",
    },
    {
      start: 76,
      end: 76,
      label: "SysEx end",
      meaning: `0x${SYSEX_END.toString(16).toUpperCase()}`,
    },
  ];
}

const PROG_MENU_NAV_OFFSETS = new Set([92, 98, 99, 146, 147]);

function describeMenuBrowse(
  data: Uint8Array,
  progUi: ProgUiRuntime | null,
): string {
  const byte = data[92]!;
  if (byte === 8) return "favorites screen";
  if (progUi) {
    const ui = decodeProgUiFromBytes(data, progUi);
    if (ui.mode === "idle") return "idle";
    if (ui.mode === "edit") return "value edit";
    if (ui.mode === "browse") return "menu highlighted";
  }

  if (byte === 2) return "menu highlighted";
  if (byte === 0) return "idle or value edit";
  return `flag ${byte}`;
}

function describeFavoriteSlot(data: Uint8Array): string {
  const byte = data[94]!;
  if (byte === 8) return "not from a favorite";
  if (byte % 2 === 0 && byte <= 6) return `favorite ${byte / 2 + 1}`;
  return `flag ${byte}`;
}

function describeDisplay(data: Uint8Array, field?: SpecField): string {
  const page = data[146]!;
  const pos = data[147]!;
  const encoded = (page << 4) | pos;
  const entry = field?.value_map?.entries.find((e) => e.encoded === encoded);
  if (entry) {
    return `${encoded} — ${entry.label}`;
  }
  return `${encoded} (page ${page}, pos ${pos})`;
}

function describeMenuIndex(
  data: Uint8Array,
  progUi: ProgUiRuntime | null,
): string {
  const index = (data[98]! << 4) | data[99]!;
  const parameter = progUi?.menu_order[index];
  const base = parameter
    ? `${index} — ${parameter}`
    : index === 0
      ? "0 — reverb time or none"
      : String(index);
  if (!progUi) return base;
  const ui = decodeProgUiFromBytes(data, progUi);
  if (ui.mode === "idle") return `${base}; UI idle`;
  if (ui.mode === "browse") return `${base}; browsing ${ui.parameter}`;
  return `${base}; editing ${ui.parameter}`;
}

function describeRegisterBasisBlob(
  data: Uint8Array,
  regBlob?: RegBlobLayout | null,
): string {
  const blob = data.subarray(24, 88);
  if (blob.every((b) => b === 0x20)) return "factory spaces (0x20)";
  if (blob.every((b) => b <= 0x0f)) {
    if (regBlob) {
      const basis = decodeRegisterBasisBlob(data, regBlob);
      if (basis) {
        return `stored register snapshot — "${basis.name}", store #${basis.storeCounter}`;
      }
    }
    return "nibble-packed register basis";
  }
  return "mixed bytes";
}

function labelForStoredValue(
  encoded: number,
  payloadField: SpecField | undefined,
): string {
  const entry = payloadField?.value_map?.entries.find(
    (e) => e.encoded === encoded,
  );
  if (entry) {
    return `${formatValueLabel(entry.label, payloadField?.parameter)} (${encoded})`;
  }
  return String(encoded);
}

export function buildRegisterBasisSubRows(
  data: Uint8Array,
  regBlob: RegBlobLayout,
  fieldsById: Map<string, SpecField>,
): ByteBreakdownSubRow[] {
  const basis = decodeRegisterBasisBlob(data, regBlob);
  if (!basis) return [];
  const rows: ByteBreakdownSubRow[] = [];
  for (const field of regBlob.fields) {
    const bits = `bits ${field.bit}–${field.bit + field.width - 1}`;
    if (field.id === "name") {
      rows.push({ label: `name (${bits})`, meaning: `"${basis.name}"` });
      continue;
    }
    if (field.id === "pad" || field.id === "tail") continue;
    const stored = basis.values[field.id]!;
    if (field.id === "store_marker") continue;
    if (field.id === "store_counter") {
      rows.push({
        label: `store counter (${bits})`,
        meaning: `${stored} store${stored === 1 ? "" : "s"} to this register slot`,
      });
      continue;
    }
    const payloadField = field.payloadField
      ? fieldsById.get(field.payloadField)
      : undefined;
    let meaning = labelForStoredValue(stored, payloadField);
    const live = payloadValue(data, field);
    if (live != null && live !== stored) {
      meaning += ` — unstored edit, live: ${labelForStoredValue(live, payloadField)}`;
    }
    rows.push({ label: `${field.label} (${bits})`, meaning });
  }
  return rows;
}

function describeRegisterBank(data: Uint8Array): string {
  const bank = data[93]!;
  return `Bank ${bank} (B${bank})`;
}

function describeRegister(data: Uint8Array): string {
  return `Register ${data[95]!}`;
}

function progSupplementaryRegions(
  data: Uint8Array,
  progUi: ProgUiRuntime | null,
  displayField?: SpecField,
  regBlob?: RegBlobLayout | null,
): Region[] {
  return [
    {
      start: 24,
      end: 87,
      label: "register basis blob",
      meaning: describeRegisterBasisBlob(data, regBlob),
    },
    {
      start: 92,
      end: 92,
      label: "panel mode flag",
      meaning: describeMenuBrowse(data, progUi),
    },
    {
      start: 93,
      end: 93,
      label: "register bank",
      meaning: describeRegisterBank(data),
    },
    {
      start: 94,
      end: 94,
      label: "favorite slot",
      meaning: describeFavoriteSlot(data),
    },
    {
      start: 95,
      end: 95,
      label: "register",
      meaning: describeRegister(data),
    },
    {
      start: 96,
      end: 97,
      label: "algorithm/family flag",
      meaning: String((data[96]! << 4) | data[97]!),
    },
    {
      start: 98,
      end: 99,
      label: "selected menu index",
      meaning: describeMenuIndex(data, progUi),
    },
    {
      start: 140,
      end: 143,
      label: "reserved",
      meaning: "always 0",
    },
    {
      start: 144,
      end: 145,
      label: "family-flag mirror",
      meaning: String((data[144]! << 4) | data[145]!),
    },
    {
      start: 146,
      end: 147,
      label: "display",
      meaning: describeDisplay(data, displayField),
    },
    {
      start: 148,
      end: 151,
      label: "reserved",
      meaning: "padding before checksum",
    },
  ];
}

function fieldRegion(
  field: SpecField,
  data: Uint8Array,
  controlByFieldId: Map<string, ControlDef>,
  blobContext?: {
    regBlob: RegBlobLayout;
    fieldsById: Map<string, SpecField>;
  } | null,
): Region {
  if (field.id === "register_basis_blob" && blobContext) {
    return {
      start: field.start,
      end: field.end,
      label: field.parameter ?? field.label,
      meaning: describeRegisterBasisBlob(data, blobContext.regBlob),
      subRows: buildRegisterBasisSubRows(
        data,
        blobContext.regBlob,
        blobContext.fieldsById,
      ),
    };
  }
  return {
    start: field.start,
    end: field.end,
    label: field.parameter ?? field.label,
    meaning: decodeFieldMeaning(field, data, controlByFieldId.get(field.id)),
  };
}

function mergeRegions(regions: Region[], messageLength: number): Region[] {
  const sorted = [...regions].sort((a, b) => a.start - b.start || a.end - b.end);
  const merged: Region[] = [];
  let cursor = 0;

  for (const region of sorted) {
    if (region.start > cursor) {
      merged.push({
        start: cursor,
        end: region.start - 1,
        label: "padding",
        meaning: "—",
      });
    }
    if (region.end >= cursor) {
      merged.push(region);
      cursor = region.end + 1;
    }
  }

  if (cursor < messageLength) {
    merged.push({
      start: cursor,
      end: messageLength - 1,
      label: "padding",
      meaning: "—",
    });
  }

  return merged;
}

export function buildByteBreakdown(
  data: Uint8Array,
  spec: DumpSpec,
  family: ActiveTab,
  options: {
    controls?: ControlDef[];
    progUi?: ProgUiRuntime | null;
    regBlob?: RegBlobLayout | null;
  } = {},
): ByteBreakdownRow[] {
  const controlByFieldId = new Map(
    (options.controls ?? []).map((c) => [c.fieldId, c]),
  );
  const progUi = options.progUi ?? null;
  const blobContext =
    family === "prog" && options.regBlob
      ? {
          regBlob: options.regBlob,
          fieldsById: new Map(spec.fields.map((f) => [f.id, f])),
        }
      : null;

  const specFields =
    family === "prog" && progUi
      ? spec.fields.filter(
          (field) =>
            !Array.from(
              { length: field.end - field.start + 1 },
              (_, i) => field.start + i,
            ).some((offset) => PROG_MENU_NAV_OFFSETS.has(offset)),
        )
      : spec.fields;

  const regions: Region[] = [
    ...frameRegions(family),
    ...specFields.map((field) =>
      fieldRegion(field, data, controlByFieldId, blobContext),
    ),
  ];

  if (family === "prog") {
    const displayField = spec.fields.find((field) => field.id === "display");
    for (const region of progSupplementaryRegions(
      data,
      progUi,
      displayField,
      options.regBlob,
    )) {
      if (!regions.some((r) => overlaps(r, region.start, region.end))) {
        regions.push(region);
      }
    }
  }

  regions.push(...trailerRegions(family));

  const deduped: Region[] = [];
  const seen = new Set<number>();
  for (const region of regions.sort((a, b) => a.start - b.start)) {
    const fresh: number[] = [];
    for (const off of range(region.start, region.end)) {
      if (!seen.has(off)) {
        seen.add(off);
        fresh.push(off);
      }
    }
    if (!fresh.length) continue;
    deduped.push({
      start: fresh[0]!,
      end: fresh[fresh.length - 1]!,
      label: region.label,
      meaning: region.meaning,
      ...(region.subRows ? { subRows: region.subRows } : {}),
    });
  }

  const merged = mergeRegions(deduped, data.length);

  return merged.map((row) => ({
    ...row,
    offsets: range(row.start, row.end),
  }));
}
