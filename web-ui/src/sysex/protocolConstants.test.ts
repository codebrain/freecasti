// Drift guard: TS protocol constants must match the Python-generated
// protocol-constants.json (written by `python run.py` via
// m7_sysex.export.web_ui.build_protocol_constants).
import { describe, expect, it } from "vitest";
import protocol from "@/generated/protocol-constants.json";
import { UI_OFFSETS } from "@/prog/uiState";
import {
  BRICASTI_MFR_ID,
  CHECKSUM_COVER_START,
  CHECKSUM_NIBBLE_COUNT,
  DATA_OFFSET,
  NAME_OFFSET,
  NAME_REGION_LENGTH,
  PROGRAM_DUMP_HEADER,
  PROGRAM_MESSAGE_LENGTH,
  PROGRAM_NAME_EDITABLE_LENGTH,
  PROGRAM_NAME_LENGTH,
  PROG_CHECKSUM_OFFSETS,
  REGISTER_BASIS_BLOB_LENGTH,
  REGISTER_BASIS_BLOB_OFFSET,
  SYS_CHECKSUM_OFFSETS,
  SYSEX_END,
  SYSEX_START,
  SYSTEM_CHECKSUM_COVER_END,
  SYSTEM_CHECKSUM_COVER_START,
  SYSTEM_DUMP_HEADER,
  SYSTEM_MESSAGE_LENGTH,
  SYSTEM_PAYLOAD_OFFSET,
} from "@/sysex/frame";

describe("protocol constants stay in sync with the Python spec", () => {
  it("frame.ts scalars match protocol-constants.json", () => {
    expect(SYSEX_START).toBe(protocol.sysex_start);
    expect(SYSEX_END).toBe(protocol.sysex_end);
    expect(NAME_OFFSET).toBe(protocol.name_offset);
    expect(PROGRAM_NAME_LENGTH).toBe(protocol.program_name_length);
    expect(PROGRAM_NAME_EDITABLE_LENGTH).toBe(
      protocol.program_name_editable_length,
    );
    expect(REGISTER_BASIS_BLOB_OFFSET).toBe(
      protocol.register_basis_blob_offset,
    );
    expect(REGISTER_BASIS_BLOB_LENGTH).toBe(
      protocol.register_basis_blob_length,
    );
    expect(NAME_REGION_LENGTH).toBe(protocol.name_region_length);
    expect(DATA_OFFSET).toBe(protocol.data_offset);
    expect(PROGRAM_MESSAGE_LENGTH).toBe(protocol.program_message_length);
    expect(SYSTEM_PAYLOAD_OFFSET).toBe(protocol.system_payload_offset);
    expect(SYSTEM_MESSAGE_LENGTH).toBe(protocol.system_message_length);
    expect(SYSTEM_CHECKSUM_COVER_START).toBe(
      protocol.system_checksum_cover_start,
    );
    expect(SYSTEM_CHECKSUM_COVER_END).toBe(protocol.system_checksum_cover_end);
    expect(CHECKSUM_NIBBLE_COUNT).toBe(protocol.checksum_nibble_count);
    expect(CHECKSUM_COVER_START).toBe(protocol.checksum_cover_start);
  });

  it("frame.ts byte sequences match protocol-constants.json", () => {
    expect([...BRICASTI_MFR_ID]).toEqual(protocol.manufacturer_id);
    expect([...PROGRAM_DUMP_HEADER]).toEqual(protocol.program_dump_header);
    expect([...SYSTEM_DUMP_HEADER]).toEqual(protocol.system_dump_header);
    expect([...PROG_CHECKSUM_OFFSETS]).toEqual(protocol.prog_checksum_offsets);
    expect([...SYS_CHECKSUM_OFFSETS]).toEqual(protocol.system_checksum_offsets);
  });

  it("uiState.ts UI offsets match protocol-constants.json", () => {
    expect(UI_OFFSETS.map(Number)).toEqual(protocol.prog_ui_state_offsets);
  });
});
