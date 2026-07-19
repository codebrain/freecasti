# GENERATED FILE — do not hand-edit.
# Produced by m7_sysex export from byte_map + parameter analyses.
# Compile with: kaitai-struct-compiler m7_system_dump.ksy
# Spec: https://kaitai.io/

meta:
  id: m7_system_dump
  title: Bricasti M7 system-dump SysEx
  application: Bricasti M7
  file-extension: syx
  endian: be
  ks-version: '0.10'
doc: |
  Reverse-engineered from labeled system captures in this repository. Not an
  official Bricasti specification.
  
  Fixed length 77 bytes. Checksum: CRC-16/ARC over offsets [8, 72), packed as
  u16_be_high_nibble_first at offsets [72, 73, 74, 75].
  
  System-parameter encodings are documented in specification/system/bytes/.
seq:
  - id: sysex_start
    doc: |
      SysEx start (F0)
      Capture series: sysex/system/
    contents: [0xf0]
  - id: manufacturer_id
    doc: |
      Manufacturer ID (00 62 63)
      Capture series: sysex/system/
    contents: [0x00, 0x62, 0x63]
  - id: system_dump_header
    doc: |
      System-dump header (70 08 02 00)
      Capture series: sysex/system/
    contents: [0x70, 0x08, 0x02, 0x00]
  - id: wet_gain
    doc: |
      Part of the M7’s internal mixing: sets the level of the processed
      (reverb) signal. Off, then −60 dB to 0 dB (Full) in 0.5 dB steps.
      Normally 0 dB (Full) with Dry Gain Off for a full-wet sidechain setup.
      Set Off to bypass processing for I/O test and measurement. Allow
      headroom when balancing with Dry Gain — the mix can add gain and the
      reverb process itself can add up to about 10 dB.
      Parameter series: sysex/system/wet gain/
      Locked encoding table: 122 known encoded value(s)
    type: wet_gain_encoded
  - id: dry_gain
    doc: |
      Part of the M7’s internal mixing: sets the level of the dry (direct)
      source path. Used with Wet Gain to balance dry and processed audio.
      Normally Off when the M7 is used as a full-wet sidechain with an
      external mixer; set to 0 dB (Full) with Wet Gain Off for unity dry
      pass-through (mastering or I/O test). Allow headroom — combining dry and
      wet can increase level. When using an external mixer, keep Dry Off to
      avoid out-of-phase dry from converter and signal-path delay.
      Parameter series: sysex/system/dry gain/
      Locked encoding table: 122 known encoded value(s)
    type: dry_gain_encoded
  - id: fixed_prefix
    doc: |
      Fixed header/prefix block (constant in this corpus)
      Capture series: sysex/system/
    type: u1
  - id: audio_routing
    doc: |
      Sets the routing of the processed (wet) audio. Useful for mono-in,
      stereo-out reverb work where a single input feeds both processing
      channels. This affects the wet path only — the dry path stays stereo
      (use a Y cable for mono internal dry mixing). Choices are Mono L, Mono
      R, or Stereo.
      Parameter series: sysex/system/audio routing/
      Locked encoding table: 3 known encoded value(s)
    type: u1
    enum: audio_routing_values
  - id: fixed_prefix_14
    doc: |
      Fixed header/prefix block (constant in this corpus)
      Capture series: sysex/system/
    type: u1
  - id: audio_format
    doc: |
      Selects whether the M7 uses its analog or AES digital audio I/O. Analog
      mode always routes through the analog converters at the optimal internal
      sample rate for analog performance, regardless of what is connected.
      Digital mode uses a valid AES input when present, locks to the incoming
      sample rate and clock, mutes if the digital stream is lost, and switches
      back seamlessly when it returns.
      Parameter series: sysex/system/audio format/
      Locked encoding table: 2 known encoded value(s)
    type: u1
    enum: audio_format_values
  - id: fixed_prefix_16
    doc: |
      Fixed header/prefix block (constant in this corpus)
      Capture series: sysex/system/
    type: u1
  - id: output_level
    doc: |
      Sets the analog output level trim in three steps (−8 dB, −16 dB, and −24
      dB) to match the input sensitivity of your mixer return or the next
      device in the chain. Return to factory defaults after level-matching
      tests — high settings can distort on hot signals.
      Parameter series: sysex/system/output level/
      Locked encoding table: 3 known encoded value(s)
    type: u1
    enum: output_level_values
  - id: reserved_always_0
    doc: |
      Reserved (always 0 in this corpus)
      Capture series: sysex/system/
    type: u1
  - id: fixed_always_02_00
    doc: |
      Fixed field (always `02 00` in this corpus)
      Capture series: sysex/system/
    size: 2
  - id: display_level
    doc: |
      Sets the brightness of the front-panel display in five steps: Dim, 1, 2,
      3, and Bright.
      Parameter series: sysex/system/display level/
      Locked encoding table: 5 known encoded value(s)
    type: u1
    enum: display_level_values
  - id: midi_channel
    doc: |
      Selects the MIDI channel the M7 listens on for program change and other
      control messages (channels 1–16, or Omni for all channels). SysEx dumps
      are channel-less and are not filtered by this setting.
      Parameter series: sysex/system/midi channel/
      Locked encoding table: 17 known encoded value(s)
    type: midi_channel_encoded
  - id: reserved_padding
    doc: |
      Reserved / padding (constant in this corpus)
      Capture series: sysex/system/
    type: u1
  - id: midi_bank
    doc: |
      Selects which program bank the M7 uses when receiving MIDI program
      changes — factory banks (Halls, Plates, Rooms, and so on), the V2 “2”
      banks, NonLin, and user register/favorite banks.
      Parameter series: sysex/system/midi bank/
      Locked encoding table: 14 known encoded value(s)
    type: u1
    enum: midi_bank_values
  - id: reserved_padding_26
    doc: |
      Reserved / padding (constant in this corpus)
      Capture series: sysex/system/
    size: 46
  - id: checksum
    doc: |
      Checksum: CRC-16/ARC over offsets 8-71, packed as four high-nibble-first
      SysEx bytes
      Capture series: sysex/system/
      CRC-16/ARC over [8, checksum), four high-nibble-first bytes
    size: 4
  - id: sysex_end
    doc: |
      SysEx end (F7)
      Capture series: sysex/system/
    contents: [0xf7]
enums:
  wet_gain_values:
    0: off  # off
    1: v_60_db  # -60 dB
    2: v_59_5_db  # -59.5 dB
    3: v_59_db  # -59 dB
    4: v_58_5_db  # -58.5 dB
    5: v_58_db  # -58 dB
    6: v_57_5_db  # -57.5 dB
    7: v_57_db  # -57 dB
    8: v_56_5_db  # -56.5 dB
    9: v_56_db  # -56 dB
    10: v_55_5_db  # -55.5 dB
    11: v_55_db  # -55 dB
    12: v_54_5_db  # -54.5 dB
    13: v_54_db  # -54 dB
    14: v_53_5_db  # -53.5 dB
    15: v_53_db  # -53 dB
    16: v_52_5_db  # -52.5 dB
    17: v_52_db  # -52 dB
    18: v_51_5_db  # -51.5 dB
    19: v_51_db  # -51 dB
    20: v_50_5_db  # -50.5 dB
    21: v_50_db  # -50 dB
    22: v_49_5_db  # -49.5 dB
    23: v_49_db  # -49 dB
    24: v_48_5_db  # -48.5 dB
    25: v_48_db  # -48 dB
    26: v_47_5_db  # -47.5 dB
    27: v_47_db  # -47 dB
    28: v_46_5_db  # -46.5 dB
    29: v_46_db  # -46 dB
    30: v_45_5_db  # -45.5 dB
    31: v_45_db  # -45 dB
    32: v_44_5_db  # -44.5 dB
    33: v_44_db  # -44 dB
    34: v_43_5_db  # -43.5 dB
    35: v_43_db  # -43 dB
    36: v_42_5_db  # -42.5 dB
    37: v_42_db  # -42 dB
    38: v_41_5_db  # -41.5 dB
    39: v_41_db  # -41 dB
    40: v_40_5_db  # -40.5 dB
    41: v_40_db  # -40 dB
    42: v_39_5_db  # -39.5 dB
    43: v_39_db  # -39 dB
    44: v_38_5_db  # -38.5 dB
    45: v_38_db  # -38 dB
    46: v_37_5_db  # -37.5 dB
    47: v_37_db  # -37 dB
    48: v_36_5_db  # -36.5 dB
    49: v_36_db  # -36 dB
    50: v_35_5_db  # -35.5 dB
    51: v_35_db  # -35 dB
    52: v_34_5_db  # -34.5 dB
    53: v_34_db  # -34 dB
    54: v_33_5_db  # -33.5 dB
    55: v_33_db  # -33 dB
    56: v_32_5_db  # -32.5 dB
    57: v_32_db  # -32 dB
    58: v_31_5_db  # -31.5 dB
    59: v_31_db  # -31 dB
    60: v_30_5_db  # -30.5 dB
    61: v_30_db  # -30 dB
    62: v_29_5_db  # -29.5 dB
    63: v_29_db  # -29 dB
    64: v_28_5_db  # -28.5 dB
    65: v_28_db  # -28 dB
    66: v_27_5_db  # -27.5 dB
    67: v_27_db  # -27 dB
    68: v_26_5_db  # -26.5 dB
    69: v_26_db  # -26 dB
    70: v_25_5_db  # -25.5 dB
    71: v_25_db  # -25 dB
    72: v_24_5_db  # -24.5 dB
    73: v_24_db  # -24 dB
    74: v_23_5_db  # -23.5 dB
    75: v_23_db  # -23 dB
    76: v_22_5_db  # -22.5 dB
    77: v_22_db  # -22 dB
    78: v_21_5_db  # -21.5 dB
    79: v_21_db  # -21 dB
    80: v_20_5_db  # -20.5 dB
    81: v_20_db  # -20 dB
    82: v_19_5_db  # -19.5 dB
    83: v_19_db  # -19 dB
    84: v_18_5_db  # -18.5 dB
    85: v_18_db  # -18 dB
    86: v_17_5_db  # -17.5 dB
    87: v_17_db  # -17 dB
    88: v_16_5_db  # -16.5 dB
    89: v_16_db  # -16 dB
    90: v_15_5_db  # -15.5 dB
    91: v_15_db  # -15 dB
    92: v_14_5_db  # -14.5 dB
    93: v_14_db  # -14 dB
    94: v_13_5_db  # -13.5 dB
    95: v_13_db  # -13 dB
    96: v_12_5_db  # -12.5 dB
    97: v_12_db  # -12 dB
    98: v_11_5_db  # -11.5 dB
    99: v_11_db  # -11 dB
    100: v_10_5_db  # -10.5 dB
    101: v_10_db  # -10 dB
    102: v_9_5_db  # -9.5 dB
    103: v_9_db  # -9 dB
    104: v_8_5_db  # -8.5 dB
    105: v_8_db  # -8 dB
    106: v_7_5_db  # -7.5 dB
    107: v_7_db  # -7 dB
    108: v_6_5_db  # -6.5 dB
    109: v_6_db  # -6 dB
    110: v_5_5_db  # -5.5 dB
    111: v_5_db  # -5 dB
    112: v_4_5_db  # -4.5 dB
    113: v_4_db  # -4 dB
    114: v_3_5_db  # -3.5 dB
    115: v_3_db  # -3 dB
    116: v_2_5_db  # -2.5 dB
    117: v_2_db  # -2 dB
    118: v_1_5_db  # -1.5 dB
    119: v_1_db  # -1 dB
    120: v_0_5_db  # -0.5 dB
    121: full  # full
  dry_gain_values:
    0: off  # off
    1: v_60_db  # -60 dB
    2: v_59_5_db  # -59.5 dB
    3: v_59_db  # -59 dB
    4: v_58_5_db  # -58.5 dB
    5: v_58_db  # -58 dB
    6: v_57_5_db  # -57.5 dB
    7: v_57_db  # -57 dB
    8: v_56_5_db  # -56.5 dB
    9: v_56_db  # -56 dB
    10: v_55_5_db  # -55.5 dB
    11: v_55_db  # -55 dB
    12: v_54_5_db  # -54.5 dB
    13: v_54_db  # -54 dB
    14: v_53_5_db  # -53.5 dB
    15: v_53_db  # -53 dB
    16: v_52_5_db  # -52.5 dB
    17: v_52_db  # -52 dB
    18: v_51_5_db  # -51.5 dB
    19: v_51_db  # -51 dB
    20: v_50_5_db  # -50.5 dB
    21: v_50_db  # -50 dB
    22: v_49_5_db  # -49.5 dB
    23: v_49_db  # -49 dB
    24: v_48_5_db  # -48.5 dB
    25: v_48_db  # -48 dB
    26: v_47_5_db  # -47.5 dB
    27: v_47_db  # -47 dB
    28: v_46_5_db  # -46.5 dB
    29: v_46_db  # -46 dB
    30: v_45_5_db  # -45.5 dB
    31: v_45_db  # -45 dB
    32: v_44_5_db  # -44.5 dB
    33: v_44_db  # -44 dB
    34: v_43_5_db  # -43.5 dB
    35: v_43_db  # -43 dB
    36: v_42_5_db  # -42.5 dB
    37: v_42_db  # -42 dB
    38: v_41_5_db  # -41.5 dB
    39: v_41_db  # -41 dB
    40: v_40_5_db  # -40.5 dB
    41: v_40_db  # -40 dB
    42: v_39_5_db  # -39.5 dB
    43: v_39_db  # -39 dB
    44: v_38_5_db  # -38.5 dB
    45: v_38_db  # -38 dB
    46: v_37_5_db  # -37.5 dB
    47: v_37_db  # -37 dB
    48: v_36_5_db  # -36.5 dB
    49: v_36_db  # -36 dB
    50: v_35_5_db  # -35.5 dB
    51: v_35_db  # -35 dB
    52: v_34_5_db  # -34.5 dB
    53: v_34_db  # -34 dB
    54: v_33_5_db  # -33.5 dB
    55: v_33_db  # -33 dB
    56: v_32_5_db  # -32.5 dB
    57: v_32_db  # -32 dB
    58: v_31_5_db  # -31.5 dB
    59: v_31_db  # -31 dB
    60: v_30_5_db  # -30.5 dB
    61: v_30_db  # -30 dB
    62: v_29_5_db  # -29.5 dB
    63: v_29_db  # -29 dB
    64: v_28_5_db  # -28.5 dB
    65: v_28_db  # -28 dB
    66: v_27_5_db  # -27.5 dB
    67: v_27_db  # -27 dB
    68: v_26_5_db  # -26.5 dB
    69: v_26_db  # -26 dB
    70: v_25_5_db  # -25.5 dB
    71: v_25_db  # -25 dB
    72: v_24_5_db  # -24.5 dB
    73: v_24_db  # -24 dB
    74: v_23_5_db  # -23.5 dB
    75: v_23_db  # -23 dB
    76: v_22_5_db  # -22.5 dB
    77: v_22_db  # -22 dB
    78: v_21_5_db  # -21.5 dB
    79: v_21_db  # -21 dB
    80: v_20_5_db  # -20.5 dB
    81: v_20_db  # -20 dB
    82: v_19_5_db  # -19.5 dB
    83: v_19_db  # -19 dB
    84: v_18_5_db  # -18.5 dB
    85: v_18_db  # -18 dB
    86: v_17_5_db  # -17.5 dB
    87: v_17_db  # -17 dB
    88: v_16_5_db  # -16.5 dB
    89: v_16_db  # -16 dB
    90: v_15_5_db  # -15.5 dB
    91: v_15_db  # -15 dB
    92: v_14_5_db  # -14.5 dB
    93: v_14_db  # -14 dB
    94: v_13_5_db  # -13.5 dB
    95: v_13_db  # -13 dB
    96: v_12_5_db  # -12.5 dB
    97: v_12_db  # -12 dB
    98: v_11_5_db  # -11.5 dB
    99: v_11_db  # -11 dB
    100: v_10_5_db  # -10.5 dB
    101: v_10_db  # -10 dB
    102: v_9_5_db  # -9.5 dB
    103: v_9_db  # -9 dB
    104: v_8_5_db  # -8.5 dB
    105: v_8_db  # -8 dB
    106: v_7_5_db  # -7.5 dB
    107: v_7_db  # -7 dB
    108: v_6_5_db  # -6.5 dB
    109: v_6_db  # -6 dB
    110: v_5_5_db  # -5.5 dB
    111: v_5_db  # -5 dB
    112: v_4_5_db  # -4.5 dB
    113: v_4_db  # -4 dB
    114: v_3_5_db  # -3.5 dB
    115: v_3_db  # -3 dB
    116: v_2_5_db  # -2.5 dB
    117: v_2_db  # -2 dB
    118: v_1_5_db  # -1.5 dB
    119: v_1_db  # -1 dB
    120: v_0_5_db  # -0.5 dB
    121: full  # full
  audio_routing_values:
    0: stereo  # stereo
    1: mono_l  # mono l
    2: mono_r  # mono r
  audio_format_values:
    0: analog  # analog
    1: digital  # digital
  output_level_values:
    0: v_8_db  # -8 dB
    1: v_16_db  # -16 dB
    2: v_24_db  # -24 dB
  display_level_values:
    0: dim  # dim
    1: v_1  # 1
    2: v_2  # 2
    3: v_3  # 3
    4: bright  # bright
  midi_channel_values:
    0: v_1  # 1
    1: v_2  # 2
    2: v_3  # 3
    3: v_4  # 4
    4: v_5  # 5
    5: v_6  # 6
    6: v_7  # 7
    7: v_8  # 8
    8: v_9  # 9
    9: v_10  # 10
    10: v_11  # 11
    11: v_12  # 12
    12: v_13  # 13
    13: v_14  # 14
    14: v_15  # 15
    15: v_16  # 16
    16: omni  # omni
  midi_bank_values:
    0: halls  # halls
    1: plates  # plates
    2: rooms  # rooms
    3: chambers  # chambers
    4: ambience  # ambience
    5: spaces  # spaces
    6: halls_2  # halls 2
    7: plates_2  # plates 2
    8: rooms_2  # rooms 2
    9: spaces_2  # spaces 2
    10: nonlin  # nonlin
    11: edit  # edit
    12: regs  # regs
    13: favs  # favs

types:
  wet_gain_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of wet_gain_values.
    seq:
      - id: hi_nibble
        type: u1
        valid:
          max: 15
      - id: lo_nibble
        type: u1
        valid:
          max: 15
    instances:
      value:
        value: (hi_nibble << 4) | lo_nibble
        enum: wet_gain_values

  dry_gain_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of dry_gain_values.
    seq:
      - id: hi_nibble
        type: u1
        valid:
          max: 15
      - id: lo_nibble
        type: u1
        valid:
          max: 15
    instances:
      value:
        value: (hi_nibble << 4) | lo_nibble
        enum: dry_gain_values

  midi_channel_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of midi_channel_values.
    seq:
      - id: hi_nibble
        type: u1
        valid:
          max: 15
      - id: lo_nibble
        type: u1
        valid:
          max: 15
    instances:
      value:
        value: (hi_nibble << 4) | lo_nibble
        enum: midi_channel_values
