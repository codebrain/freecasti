# GENERATED FILE — do not hand-edit.
# Produced by m7_sysex export from byte_map + parameter analyses.
# Compile with: kaitai-struct-compiler m7_program_dump.ksy
# Spec: https://kaitai.io/

meta:
  id: m7_program_dump
  title: Bricasti M7 program-dump SysEx
  application: Bricasti M7
  file-extension: syx
  endian: be
  ks-version: '0.10'
doc: |
  Reverse-engineered from labeled captures in this repository. Not an official
  Bricasti specification. Dump-derived encodings and offsets are authoritative
  for this corpus.
  
  Fixed length 157 bytes. Checksum: CRC-16/ARC over offsets [8, 152), packed
  as u16_be_high_nibble_first at offsets [152, 153, 154, 155].
  
  Sound-parameter value maps (affine scales / sparse tables) live alongside
  this layout in the companion .spec.json and in specification/prog/bytes/.
seq:
  - id: sysex_start
    doc: |
      SysEx start (F0)
    contents: [0xf0]
  - id: manufacturer_id
    doc: |
      Manufacturer ID (00 62 63)
    contents: [0x00, 0x62, 0x63]
  - id: program_dump_header
    doc: |
      Program-dump header (70 08 01 00)
    contents: [0x70, 0x08, 0x01, 0x00]
  - id: program_name
    doc: |
      Program name (ASCII): 16-byte wire window with 14-character editable
      label (manual); trailing two bytes space-padded - confirmed against
      sysex/_presets/ file...
    type: str
    size: 16
    encoding: ASCII
  - id: register_basis_blob
    doc: |
      Register basis blob (`raw_bytes`): factory dumps space-pad with `0x20`;
      Reg-backed hold-EDIT dumps store a nibble-packed unedited copy of the
      register basis ...
    size: 64
  - id: bank_index
    doc: |
      Bank index (`nibble_hilo`) from sysex/_presets/ [Halls=0, Plates=1,
      Rooms=2, Chambers=3, Ambience=4, Spaces=5, Halls 2=6, Plates 2=7, Rooms
      2=8, Spaces 2=9, ...
      Locked encoding table: 15 known encoded value(s)
    type: bank_index_encoded
  - id: program_slot
    doc: |
      Program slot within bank (`nibble_hilo`) from sysex/_presets/ (not a
      global program number)
    type: nibble_u8_hilo
  - id: edit_generation_counter
    doc: |
      Menu-browse flag: `00` when no parameter menu is open or while editing a
      value; `02` while a parameter menu is highlighted (see
      `sysex/prog/menus/` captures)...
      Secondary/edit-UI field — not a primary sound parameter
    type: u1
  - id: register_bank
    doc: |
      Register bank (`raw_u8`, manual Bank): `B0`–`B4` = `00`–`04` when the
      dump basis is a user register (see `sysex/prog/edit/registers/`); `00`
      on factory/param...
      Locked encoding table: 5 known encoded value(s)
    type: u1
    enum: register_bank_values
  - id: structure_version
    doc: |
      Structure/version constant (`08` in all witnessed program dumps) — not a
      sound parameter
    type: u1
  - id: register
    doc: |
      Register within bank (`raw_u8`, manual Register `0`–`9`) when the dump
      basis is a user register; `00` on factory/parameter-series dumps in this
      corpus
      Locked encoding table: 10 known encoded value(s)
    type: u1
    enum: register_values
  - id: reserved_always_0
    doc: |
      Reserved/unknown (always `00` in witnessed captures)
    type: u1
  - id: algorithm_family_flag
    doc: |
      Algorithm/family flag from corpus presets (Halls all 3; most other
      presets 4, with a few bank-leading exceptions also 3). Mirrored at 145
      as 0 when 97=3 and ...
    type: u1
  - id: selected_menu_index
    doc: |
      Selected front-panel menu index (`nibble_hilo`, 0–17) when a parameter
      menu is open; `00 00` when idle. Hardware menu order matches
      `PROGRAM_PARAMETERS` in c...
      Secondary/edit-UI field — not a primary sound parameter
    type: nibble_u8_hilo
  - id: reverb_time
    doc: |
      Mid-frequency reverb time. Sets the reverb time of the mid frequencies
      when the signal stops.
      Parameter series: sysex/prog/parameters/reverb time/
      Locked encoding table: 137 known encoded value(s)
    type: reverb_time_encoded
  - id: size
    doc: |
      Adjusts the apparent size of the late reverberant field.
      Parameter series: sysex/prog/parameters/size/
      Locked encoding table: 31 known encoded value(s)
    type: size_encoded
  - id: predelay
    doc: |
      Sets the amount of time which elapses between the input signal and the
      onset of reverberation.
      Parameter series: sysex/prog/parameters/predelay/
      Locked encoding table: 86 known encoded value(s)
    type: predelay_encoded
  - id: reserved_padding
    doc: |
      Reserved padding (always 0) between predelay and diffusion
    type: u1
  - id: diffusion
    doc: |
      Sets initial diffusion of the reverb. Displayed and controlled as a
      percentage change from the initial value defined by the preset.
      Parameter series: sysex/prog/parameters/diffusion/
      Locked encoding table: 11 known encoded value(s)
    type: u1
    enum: diffusion_values
  - id: reserved_padding_108
    doc: |
      Reserved padding (always 0) between diffusion and density
    type: u1
  - id: density
    doc: |
      Sets how the echo density builds up over time.
      Parameter series: sysex/prog/parameters/density/
      Locked encoding table: 11 known encoded value(s)
    type: u1
    enum: density_values
  - id: reserved_padding_110
    doc: |
      Reserved padding (always 0) between density and modulation
    type: u1
  - id: modulation
    doc: |
      Controls the amount of modulation and pitch variation in the later part
      of the reverberant field.
      Parameter series: sysex/prog/parameters/modulation/
      Locked encoding table: 12 known encoded value(s)
    type: u1
    enum: modulation_values
  - id: rolloff
    doc: |
      Low pass filter applied to the overall output of the reverb.
      Parameter series: sysex/prog/parameters/rolloff/
      Locked encoding table: 71 known encoded value(s)
    type: rolloff_encoded
  - id: hf_rt_multiply
    doc: |
      Sets the high-frequency reverb time above the crossover frequency set by
      HF RT Crossover. Displayed and controlled as a scaling of Reverb Time.
      Parameter series: sysex/prog/parameters/hf rt multiply/
      Locked encoding table: 17 known encoded value(s)
    type: hf_rt_multiply_encoded
  - id: hf_rt_crossover
    doc: |
      Sets the crossover frequency used by HF RT Multiply.
      Parameter series: sysex/prog/parameters/hf rt crossover/
      Locked encoding table: 37 known encoded value(s)
    type: hf_rt_crossover_encoded
  - id: lf_rt_multiply
    doc: |
      Sets the low-frequency reverb time below the crossover frequency set by
      LF RT Crossover. Displayed and controlled as a scaling of Reverb Time.
      Parameter series: sysex/prog/parameters/lf rt multiply/
      Locked encoding table: 57 known encoded value(s)
    type: lf_rt_multiply_encoded
  - id: lf_rt_crossover
    doc: |
      Sets the crossover frequency used by LF RT Multiply.
      Parameter series: sysex/prog/parameters/lf rt crossover/
      Locked encoding table: 27 known encoded value(s)
    type: lf_rt_crossover_encoded
  - id: vlf_cut
    doc: |
      Cuts the very low frequency content of the initial part of both the
      early and late reverberant fields.
      Parameter series: sysex/prog/parameters/vlf cut/
      Locked encoding table: 21 known encoded value(s)
    type: vlf_cut_encoded
  - id: early_to_reverb_mix
    doc: |
      Sets the balance between the early and later parts of the reverberant
      fields.
      Parameter series: sysex/prog/parameters/early to reverb mix/
      Locked encoding table: 41 known encoded value(s)
    type: early_to_reverb_mix_encoded
  - id: early_rolloff
    doc: |
      Sets the rolloff frequency point of the low pass filter for the early
      part of the reverberant field.
      Parameter series: sysex/prog/parameters/early rolloff/
      Locked encoding table: 71 known encoded value(s)
    type: early_rolloff_encoded
  - id: early_select
    doc: |
      Controls the build up and decay characteristics of the early part of the
      reverberant field. The V2 addendum expands the selection beyond the
      printed 0–20 to 0–31 with larger, more spread-out early variants for a
      slower early reverb build-up (available on both V1 and V2 algorithm
      presets).
      Parameter series: sysex/prog/parameters/early select/
      Locked encoding table: 32 known encoded value(s)
    type: early_select_encoded
  - id: engine_bank_class_flag
    doc: |
      Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on `* 2`
      banks (Halls 2…Spaces 2), 2 on NonLin. Parameter-series dumps also show
      1 because they ...
    type: u1
  - id: fixed_always_02_00
    doc: |
      Fixed companion to offset 130 (always `02 00` in this corpus)
    size: 2
  - id: delay_level
    doc: |
      Level of the delayed input injected into the start of the late reverb
      (not the early reverb). The delayed sound is the original input signal,
      delayed, diffused, and band-limited by Rolloff.
      Parameter series: sysex/prog/parameters/delay level/
      Locked encoding table: 16 known encoded value(s)
    type: u1
    enum: delay_level_values
  - id: delay_time
    doc: |
      Delay time for a diffused set of eight voices spread in time (controlled
      as a single delay). Adds coloration and a late swell to the late reverb.
      Parameter series: sysex/prog/parameters/delay time/
      Locked encoding table: 113 known encoded value(s)
    type: delay_time_encoded
  - id: reserved_always_0_136
    doc: |
      Reserved (always 0) between delay time and bank-index mirror
    type: u1
  - id: bank_index_mirror
    doc: |
      Bank index mirror (equals offset 89) from sysex/_presets/; on hold-EDIT
      dumps this stays the source bank while 88-89 are Edit index 11
    type: u1
  - id: reserved_always_0_138
    doc: |
      Reserved (always 0) between bank-index mirror and delay modulation
    type: u1
  - id: delay_modulation
    doc: |
      Modulates the delay voices only (not the reverb), similar in character
      to reverb Modulation: low settings are slower and more shallow; higher
      settings are more random and deeper.
      Parameter series: sysex/prog/parameters/delay modulation/
      Locked encoding table: 12 known encoded value(s)
    type: u1
    enum: delay_modulation_values
  - id: reserved_always_0_140
    doc: |
      Reserved block (always 0 in this corpus)
    size: 5
  - id: family_flag_mirror
    doc: |
      Mirror of algorithm/family flag at 97 (145=0 when 97=3; 145=1 when 97=4
      in this corpus)
    type: u1
  - id: display
    doc: |
      Display (`nibble_hilo`): high nibble = page/row while browsing (`92=02`)
      or edit anchor while changing a value (`92=00`); low nibble = position
      within the me...
      Capture series: sysex/prog/menus/
      Locked encoding table: 35 known encoded value(s)
    type: display_encoded
  - id: reserved_always_0_148
    doc: |
      Reserved (always 0) immediately before checksum nibbles
    size: 4
  - id: checksum
    doc: |
      Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four
      high-nibble-first SysEx bytes (per-dump; recompute after edits - do not
      copy across ...
      CRC-16/ARC over [8, checksum), four high-nibble-first bytes
    size: 4
  - id: sysex_end
    doc: |
      SysEx end (F7)
    contents: [0xf7]
enums:
  bank_index_values:
    0: halls  # Halls
    1: plates  # Plates
    2: rooms  # Rooms
    3: chambers  # Chambers
    4: ambience  # Ambience
    5: spaces  # Spaces
    6: halls_2  # Halls 2
    7: plates_2  # Plates 2
    8: rooms_2  # Rooms 2
    9: spaces_2  # Spaces 2
    10: nonlin  # NonLin
    11: edit  # Edit
    118: edit_receive  # Edit (receive)
    119: favorites  # Favorites
    120: registers  # Registers
  register_bank_values:
    0: b0  # B0
    1: b1  # B1
    2: b2  # B2
    3: b3  # B3
    4: b4  # B4
  register_values:
    0: reg_0  # 0
    1: reg_1  # 1
    2: reg_2  # 2
    3: reg_3  # 3
    4: reg_4  # 4
    5: reg_5  # 5
    6: reg_6  # 6
    7: reg_7  # 7
    8: reg_8  # 8
    9: reg_9  # 9
  reverb_time_values:
    0: v_0_2  # 0.2
    1: v_0_25  # 0.25
    2: v_0_3  # 0.3
    3: v_0_35  # 0.35
    4: v_0_4  # 0.4
    5: v_0_45  # 0.45
    6: v_0_5  # 0.5
    7: v_0_55  # 0.55
    8: v_0_6  # 0.6
    9: v_0_65  # 0.65
    10: v_0_7  # 0.7
    11: v_0_75  # 0.75
    12: v_0_8  # 0.8
    13: v_0_85  # 0.85
    14: v_0_9  # 0.9
    15: v_0_95  # 0.95
    16: v_1  # 1
    17: v_1_05  # 1.05
    18: v_1_1  # 1.1
    19: v_1_15  # 1.15
    20: v_1_2  # 1.2
    21: v_1_25  # 1.25
    22: v_1_3  # 1.3
    23: v_1_35  # 1.35
    24: v_1_4  # 1.4
    25: v_1_45  # 1.45
    26: v_1_5  # 1.5
    27: v_1_55  # 1.55
    28: v_1_6  # 1.6
    29: v_1_65  # 1.65
    30: v_1_7  # 1.7
    31: v_1_75  # 1.75
    32: v_1_8  # 1.8
    33: v_1_85  # 1.85
    34: v_1_9  # 1.9
    35: v_1_95  # 1.95
    36: v_2  # 2
    37: v_2_05  # 2.05
    38: v_2_1  # 2.1
    39: v_2_15  # 2.15
    40: v_2_2  # 2.2
    41: v_2_25  # 2.25
    42: v_2_3  # 2.3
    43: v_2_35  # 2.35
    44: v_2_4  # 2.4
    45: v_2_45  # 2.45
    46: v_2_5  # 2.5
    47: v_2_55  # 2.55
    48: v_2_6  # 2.6
    49: v_2_65  # 2.65
    50: v_2_7  # 2.7
    51: v_2_75  # 2.75
    52: v_2_8  # 2.8
    53: v_2_85  # 2.85
    54: v_2_9  # 2.9
    55: v_2_95  # 2.95
    56: v_3  # 3
    57: v_3_1  # 3.1
    58: v_3_2  # 3.2
    59: v_3_3  # 3.3
    60: v_3_4  # 3.4
    61: v_3_5  # 3.5
    62: v_3_6  # 3.6
    63: v_3_7  # 3.7
    64: v_3_8  # 3.8
    65: v_3_9  # 3.9
    66: v_4_0  # 4.0
    67: v_4_1  # 4.1
    68: v_4_2  # 4.2
    69: v_4_3  # 4.3
    70: v_4_4  # 4.4
    71: v_4_5  # 4.5
    72: v_4_6  # 4.6
    73: v_4_7  # 4.7
    74: v_4_8  # 4.8
    75: v_4_9  # 4.9
    76: v_5  # 5
    77: v_5_1  # 5.1
    78: v_5_2  # 5.2
    79: v_5_3  # 5.3
    80: v_5_4  # 5.4
    81: v_5_5  # 5.5
    82: v_5_6  # 5.6
    83: v_5_7  # 5.7
    84: v_5_8  # 5.8
    85: v_5_9  # 5.9
    86: v_6  # 6
    87: v_6_2  # 6.2
    88: v_6_4  # 6.4
    89: v_6_6  # 6.6
    90: v_6_8  # 6.8
    91: v_7  # 7
    92: v_7_2  # 7.2
    93: v_7_4  # 7.4
    94: v_7_6  # 7.6
    95: v_7_8  # 7.8
    96: v_8  # 8
    97: v_8_2  # 8.2
    98: v_8_4  # 8.4
    99: v_8_6  # 8.6
    100: v_8_8  # 8.8
    101: v_9  # 9
    102: v_9_2  # 9.2
    103: v_9_4  # 9.4
    104: v_9_6  # 9.6
    105: v_9_8  # 9.8
    106: v_10  # 10
    107: v_10_5  # 10.5
    108: v_11  # 11
    109: v_11_5  # 11.5
    110: v_12  # 12
    111: v_12_5  # 12.5
    112: v_13  # 13
    113: v_13_5  # 13.5
    114: v_14  # 14
    115: v_14_5  # 14.5
    116: v_15  # 15
    117: v_15_5  # 15.5
    118: v_16  # 16
    119: v_16_5  # 16.5
    120: v_17  # 17
    121: v_17_5  # 17.5
    122: v_18  # 18
    123: v_18_5  # 18.5
    124: v_19  # 19
    125: v_19_5  # 19.5
    126: v_20  # 20
    127: v_21  # 21
    128: v_22  # 22
    129: v_23  # 23
    130: v_24  # 24
    131: v_25  # 25
    132: v_26  # 26
    133: v_27  # 27
    134: v_28  # 28
    135: v_29  # 29
    136: v_30  # 30
  size_values:
    0: small  # Small
    1: v_1  # 1
    2: v_2  # 2
    3: v_3  # 3
    4: v_4  # 4
    5: v_5  # 5
    6: v_6  # 6
    7: v_7  # 7
    8: v_8  # 8
    9: v_9  # 9
    10: v_10  # 10
    11: v_11  # 11
    12: v_12  # 12
    13: v_13  # 13
    14: v_14  # 14
    15: v_15  # 15
    16: v_16  # 16
    17: v_17  # 17
    18: v_18  # 18
    19: v_19  # 19
    20: v_20  # 20
    21: v_21  # 21
    22: v_22  # 22
    23: v_23  # 23
    24: v_24  # 24
    25: v_25  # 25
    26: v_26  # 26
    27: v_27  # 27
    28: v_28  # 28
    29: v_29  # 29
    30: large  # Large
  predelay_values:
    0: v_0_ms  # 0 ms
    1: v_2_ms  # 2 ms
    2: v_4_ms  # 4 ms
    3: v_6_ms  # 6 ms
    4: v_8_ms  # 8 ms
    5: v_10_ms  # 10 ms
    6: v_12_ms  # 12 ms
    7: v_14_ms  # 14 ms
    8: v_16_ms  # 16 ms
    9: v_18_ms  # 18 ms
    10: v_20_ms  # 20 ms
    11: v_22_ms  # 22 ms
    12: v_24_ms  # 24 ms
    13: v_26_ms  # 26 ms
    14: v_28_ms  # 28 ms
    15: v_30_ms  # 30 ms
    16: v_32_ms  # 32 ms
    17: v_34_ms  # 34 ms
    18: v_36_ms  # 36 ms
    19: v_38_ms  # 38 ms
    20: v_40_ms  # 40 ms
    21: v_44_ms  # 44 ms
    22: v_48_ms  # 48 ms
    23: v_52_ms  # 52 ms
    24: v_56_ms  # 56 ms
    25: v_60_ms  # 60 ms
    26: v_64_ms  # 64 ms
    27: v_68_ms  # 68 ms
    28: v_72_ms  # 72 ms
    29: v_76_ms  # 76 ms
    30: v_80_ms  # 80 ms
    31: v_84_ms  # 84 ms
    32: v_88_ms  # 88 ms
    33: v_92_ms  # 92 ms
    34: v_96_ms  # 96 ms
    35: v_100_ms  # 100 ms
    36: v_108_ms  # 108 ms
    37: v_116_ms  # 116 ms
    38: v_124_ms  # 124 ms
    39: v_132_ms  # 132 ms
    40: v_140_ms  # 140 ms
    41: v_148_ms  # 148 ms
    42: v_156_ms  # 156 ms
    43: v_164_ms  # 164 ms
    44: v_172_ms  # 172 ms
    45: v_180_ms  # 180 ms
    46: v_188_ms  # 188 ms
    47: v_196_ms  # 196 ms
    48: v_204_ms  # 204 ms
    49: v_212_ms  # 212 ms
    50: v_220_ms  # 220 ms
    51: v_228_ms  # 228 ms
    52: v_236_ms  # 236 ms
    53: v_244_ms  # 244 ms
    54: v_252_ms  # 252 ms
    55: v_260_ms  # 260 ms
    56: v_268_ms  # 268 ms
    57: v_276_ms  # 276 ms
    58: v_284_ms  # 284 ms
    59: v_292_ms  # 292 ms
    60: v_300_ms  # 300 ms
    61: v_308_ms  # 308 ms
    62: v_316_ms  # 316 ms
    63: v_324_ms  # 324 ms
    64: v_332_ms  # 332 ms
    65: v_340_ms  # 340 ms
    66: v_348_ms  # 348 ms
    67: v_356_ms  # 356 ms
    68: v_364_ms  # 364 ms
    69: v_372_ms  # 372 ms
    70: v_380_ms  # 380 ms
    71: v_388_ms  # 388 ms
    72: v_396_ms  # 396 ms
    73: v_404_ms  # 404 ms
    74: v_412_ms  # 412 ms
    75: v_420_ms  # 420 ms
    76: v_428_ms  # 428 ms
    77: v_436_ms  # 436 ms
    78: v_444_ms  # 444 ms
    79: v_452_ms  # 452 ms
    80: v_460_ms  # 460 ms
    81: v_468_ms  # 468 ms
    82: v_476_ms  # 476 ms
    83: v_484_ms  # 484 ms
    84: v_492_ms  # 492 ms
    85: v_500_ms  # 500 ms
  diffusion_values:
    0: low  # Low
    1: v_1  # 1
    2: v_2  # 2
    3: v_3  # 3
    4: v_4  # 4
    5: v_5  # 5
    6: v_6  # 6
    7: v_7  # 7
    8: v_8  # 8
    9: v_9  # 9
    10: high  # High
  density_values:
    0: low  # Low
    1: v_1  # 1
    2: v_2  # 2
    3: v_3  # 3
    4: v_4  # 4
    5: v_5  # 5
    6: v_6  # 6
    7: v_7  # 7
    8: v_8  # 8
    9: v_9  # 9
    10: high  # High
  modulation_values:
    0: off  # off
    1: v_0  # 0
    2: v_1  # 1
    3: v_2  # 2
    4: v_3  # 3
    5: v_4  # 4
    6: v_5  # 5
    7: v_6  # 6
    8: v_7  # 7
    9: v_8  # 8
    10: v_9  # 9
    11: v_10  # 10
  rolloff_values:
    0: v_80_hz  # 80 Hz
    1: v_120_hz  # 120 Hz
    2: v_160_hz  # 160 Hz
    3: v_200_hz  # 200 Hz
    4: v_240_hz  # 240 Hz
    5: v_280_hz  # 280 Hz
    6: v_320_hz  # 320 Hz
    7: v_360_hz  # 360 Hz
    8: v_400_hz  # 400 Hz
    9: v_480_hz  # 480 Hz
    10: v_560_hz  # 560 Hz
    11: v_640_hz  # 640 Hz
    12: v_720_hz  # 720 Hz
    13: v_800_hz  # 800 Hz
    14: v_1000_hz  # 1000 Hz
    15: v_1200_hz  # 1200 Hz
    16: v_1400_hz  # 1400 Hz
    17: v_1600_hz  # 1600 Hz
    18: v_1800_hz  # 1800 Hz
    19: v_2000_hz  # 2000 Hz
    20: v_2400_hz  # 2400 Hz
    21: v_2800_hz  # 2800 Hz
    22: v_3200_hz  # 3200 Hz
    23: v_3600_hz  # 3600 Hz
    24: v_4000_hz  # 4000 Hz
    25: v_4400_hz  # 4400 Hz
    26: v_4800_hz  # 4800 Hz
    27: v_5200_hz  # 5200 Hz
    28: v_5600_hz  # 5600 Hz
    29: v_6000_hz  # 6000 Hz
    30: v_6400_hz  # 6400 Hz
    31: v_6800_hz  # 6800 Hz
    32: v_7200_hz  # 7200 Hz
    33: v_7600_hz  # 7600 Hz
    34: v_8000_hz  # 8000 Hz
    35: v_8400_hz  # 8400 Hz
    36: v_8800_hz  # 8800 Hz
    37: v_9200_hz  # 9200 Hz
    38: v_9600_hz  # 9600 Hz
    39: v_10000_hz  # 10000 Hz
    40: v_10400_hz  # 10400 Hz
    41: v_10800_hz  # 10800 Hz
    42: v_11200_hz  # 11200 Hz
    43: v_11600_hz  # 11600 Hz
    44: v_12000_hz  # 12000 Hz
    45: v_12400_hz  # 12400 Hz
    46: v_12800_hz  # 12800 Hz
    47: v_13200_hz  # 13200 Hz
    48: v_13600_hz  # 13600 Hz
    49: v_14000_hz  # 14000 Hz
    50: v_14400_hz  # 14400 Hz
    51: v_14800_hz  # 14800 Hz
    52: v_15200_hz  # 15200 Hz
    53: v_15600_hz  # 15600 Hz
    54: v_16000_hz  # 16000 Hz
    55: v_16400_hz  # 16400 Hz
    56: v_16800_hz  # 16800 Hz
    57: v_17200_hz  # 17200 Hz
    58: v_17600_hz  # 17600 Hz
    59: v_18000_hz  # 18000 Hz
    60: v_18400_hz  # 18400 Hz
    61: v_18800_hz  # 18800 Hz
    62: v_19200_hz  # 19200 Hz
    63: v_19600_hz  # 19600 Hz
    64: v_20000_hz  # 20000 Hz
    65: v_20400_hz  # 20400 Hz
    66: v_20800_hz  # 20800 Hz
    67: v_21200_hz  # 21200 Hz
    68: v_21600_hz  # 21600 Hz
    69: v_22000_hz  # 22000 Hz
    70: full  # Full
  hf_rt_multiply_values:
    0: v_0_2  # 0.2
    1: v_0_25  # 0.25
    2: v_0_3  # 0.3
    3: v_0_35  # 0.35
    4: v_0_4  # 0.4
    5: v_0_45  # 0.45
    6: v_0_5  # 0.5
    7: v_0_55  # 0.55
    8: v_0_6  # 0.6
    9: v_0_65  # 0.65
    10: v_0_7  # 0.7
    11: v_0_75  # 0.75
    12: v_0_8  # 0.8
    13: v_0_85  # 0.85
    14: v_0_9  # 0.9
    15: v_0_95  # 0.95
    16: v_1  # 1
  hf_rt_crossover_values:
    0: v_200_hz  # 200 Hz
    1: v_240_hz  # 240 Hz
    2: v_280_hz  # 280 Hz
    3: v_320_hz  # 320 Hz
    4: v_360_hz  # 360 Hz
    5: v_400_hz  # 400 Hz
    6: v_480_hz  # 480 Hz
    7: v_560_hz  # 560 Hz
    8: v_640_hz  # 640 Hz
    9: v_720_hz  # 720 Hz
    10: v_800_hz  # 800 Hz
    11: v_1000_hz  # 1000 Hz
    12: v_1200_hz  # 1200 Hz
    13: v_1400_hz  # 1400 Hz
    14: v_1600_hz  # 1600 Hz
    15: v_1800_hz  # 1800 Hz
    16: v_2000_hz  # 2000 Hz
    17: v_2400_hz  # 2400 Hz
    18: v_2800_hz  # 2800 Hz
    19: v_3200_hz  # 3200 Hz
    20: v_3600_hz  # 3600 Hz
    21: v_4000_hz  # 4000 Hz
    22: v_4800_hz  # 4800 Hz
    23: v_5600_hz  # 5600 Hz
    24: v_6400_hz  # 6400 Hz
    25: v_7200_hz  # 7200 Hz
    26: v_8000_hz  # 8000 Hz
    27: v_8800_hz  # 8800 Hz
    28: v_9600_hz  # 9600 Hz
    29: v_10400_hz  # 10400 Hz
    30: v_11200_hz  # 11200 Hz
    31: v_12000_hz  # 12000 Hz
    32: v_12800_hz  # 12800 Hz
    33: v_13600_hz  # 13600 Hz
    34: v_14400_hz  # 14400 Hz
    35: v_15200_hz  # 15200 Hz
    36: v_16000_hz  # 16000 Hz
  lf_rt_multiply_values:
    0: v_0_2  # 0.2
    1: v_0_25  # 0.25
    2: v_0_3  # 0.3
    3: v_0_35  # 0.35
    4: v_0_4  # 0.4
    5: v_0_45  # 0.45
    6: v_0_5  # 0.5
    7: v_0_55  # 0.55
    8: v_0_6  # 0.6
    9: v_0_65  # 0.65
    10: v_0_7  # 0.7
    11: v_0_75  # 0.75
    12: v_0_8  # 0.8
    13: v_0_85  # 0.85
    14: v_0_9  # 0.9
    15: v_0_95  # 0.95
    16: v_1  # 1
    17: v_1_05  # 1.05
    18: v_1_1  # 1.1
    19: v_1_15  # 1.15
    20: v_1_2  # 1.2
    21: v_1_25  # 1.25
    22: v_1_3  # 1.3
    23: v_1_35  # 1.35
    24: v_1_4  # 1.4
    25: v_1_45  # 1.45
    26: v_1_5  # 1.5
    27: v_1_55  # 1.55
    28: v_1_6  # 1.6
    29: v_1_65  # 1.65
    30: v_1_7  # 1.7
    31: v_1_75  # 1.75
    32: v_1_8  # 1.8
    33: v_1_85  # 1.85
    34: v_1_9  # 1.9
    35: v_1_95  # 1.95
    36: v_2  # 2
    37: v_2_1  # 2.1
    38: v_2_2  # 2.2
    39: v_2_3  # 2.3
    40: v_2_4  # 2.4
    41: v_2_5  # 2.5
    42: v_2_6  # 2.6
    43: v_2_7  # 2.7
    44: v_2_8  # 2.8
    45: v_2_9  # 2.9
    46: v_3_0  # 3.0
    47: v_3_1  # 3.1
    48: v_3_2  # 3.2
    49: v_3_3  # 3.3
    50: v_3_4  # 3.4
    51: v_3_5  # 3.5
    52: v_3_6  # 3.6
    53: v_3_7  # 3.7
    54: v_3_8  # 3.8
    55: v_3_9  # 3.9
    56: v_4  # 4
  lf_rt_crossover_values:
    0: v_80_hz  # 80 Hz
    1: v_120_hz  # 120 Hz
    2: v_160_hz  # 160 Hz
    3: v_200_hz  # 200 Hz
    4: v_240_hz  # 240 Hz
    5: v_280_hz  # 280 Hz
    6: v_320_hz  # 320 Hz
    7: v_360_hz  # 360 Hz
    8: v_400_hz  # 400 Hz
    9: v_480_hz  # 480 Hz
    10: v_560_hz  # 560 Hz
    11: v_640_hz  # 640 Hz
    12: v_720_hz  # 720 Hz
    13: v_800_hz  # 800 Hz
    14: v_1000_hz  # 1000 Hz
    15: v_1200_hz  # 1200 Hz
    16: v_1400_hz  # 1400 Hz
    17: v_1600_hz  # 1600 Hz
    18: v_1800_hz  # 1800 Hz
    19: v_2000_hz  # 2000 Hz
    20: v_2400_hz  # 2400 Hz
    21: v_2800_hz  # 2800 Hz
    22: v_3200_hz  # 3200 Hz
    23: v_3600_hz  # 3600 Hz
    24: v_4000_hz  # 4000 Hz
    25: v_4400_hz  # 4400 Hz
    26: v_4800_hz  # 4800 Hz
  vlf_cut_values:
    0: v_20_db  # -20 dB
    1: v_19_db  # -19 dB
    2: v_18_db  # -18 dB
    3: v_17_db  # -17 dB
    4: v_16_db  # -16 dB
    5: v_15_db  # -15 dB
    6: v_14_db  # -14 dB
    7: v_13_db  # -13 dB
    8: v_12_db  # -12 dB
    9: v_11_db  # -11 dB
    10: v_10_db  # -10 dB
    11: v_9_db  # -9 dB
    12: v_8_db  # -8 dB
    13: v_7_db  # -7 dB
    14: v_6_db  # -6 dB
    15: v_5_db  # -5 dB
    16: v_4_db  # -4 dB
    17: v_3_db  # -3 dB
    18: v_2_db  # -2 dB
    19: v_1_db  # -1 dB
    20: v_0_db  # 0 dB
  early_to_reverb_mix_values:
    0: v_0_20  # 0/20
    1: v_1_20  # 1/20
    2: v_2_20  # 2/20
    3: v_3_20  # 3/20
    4: v_4_20  # 4/20
    5: v_5_20  # 5/20
    6: v_6_20  # 6/20
    7: v_7_20  # 7/20
    8: v_8_20  # 8/20
    9: v_9_20  # 9/20
    10: v_10_20  # 10/20
    11: v_11_20  # 11/20
    12: v_12_20  # 12/20
    13: v_13_20  # 13/20
    14: v_14_20  # 14/20
    15: v_15_20  # 15/20
    16: v_16_20  # 16/20
    17: v_17_20  # 17/20
    18: v_18_20  # 18/20
    19: v_19_20  # 19/20
    20: v_20_20  # 20/20
    21: v_20_19  # 20/19
    22: v_20_18  # 20/18
    23: v_20_17  # 20/17
    24: v_20_16  # 20/16
    25: v_20_15  # 20/15
    26: v_20_14  # 20/14
    27: v_20_13  # 20/13
    28: v_20_12  # 20/12
    29: v_20_11  # 20/11
    30: v_20_10  # 20/10
    31: v_20_9  # 20/9
    32: v_20_8  # 20/8
    33: v_20_7  # 20/7
    34: v_20_6  # 20/6
    35: v_20_5  # 20/5
    36: v_20_4  # 20/4
    37: v_20_3  # 20/3
    38: v_20_2  # 20/2
    39: v_20_1  # 20/1
    40: v_20_0  # 20/0
  early_rolloff_values:
    0: v_80_hz  # 80 Hz
    1: v_120_hz  # 120 Hz
    2: v_160_hz  # 160 Hz
    3: v_200_hz  # 200 Hz
    4: v_240_hz  # 240 Hz
    5: v_280_hz  # 280 Hz
    6: v_320_hz  # 320 Hz
    7: v_360_hz  # 360 Hz
    8: v_400_hz  # 400 Hz
    9: v_480_hz  # 480 Hz
    10: v_560_hz  # 560 Hz
    11: v_640_hz  # 640 Hz
    12: v_720_hz  # 720 Hz
    13: v_800_hz  # 800 Hz
    14: v_1000_hz  # 1000 Hz
    15: v_1200_hz  # 1200 Hz
    16: v_1400_hz  # 1400 Hz
    17: v_1600_hz  # 1600 Hz
    18: v_1800_hz  # 1800 Hz
    19: v_2000_hz  # 2000 Hz
    20: v_2400_hz  # 2400 Hz
    21: v_2800_hz  # 2800 Hz
    22: v_3200_hz  # 3200 Hz
    23: v_3600_hz  # 3600 Hz
    24: v_4000_hz  # 4000 Hz
    25: v_4400_hz  # 4400 Hz
    26: v_4800_hz  # 4800 Hz
    27: v_5200_hz  # 5200 Hz
    28: v_5600_hz  # 5600 Hz
    29: v_6000_hz  # 6000 Hz
    30: v_6400_hz  # 6400 Hz
    31: v_6800_hz  # 6800 Hz
    32: v_7200_hz  # 7200 Hz
    33: v_7600_hz  # 7600 Hz
    34: v_8000_hz  # 8000 Hz
    35: v_8400_hz  # 8400 Hz
    36: v_8800_hz  # 8800 Hz
    37: v_9200_hz  # 9200 Hz
    38: v_9600_hz  # 9600 Hz
    39: v_10000_hz  # 10000 Hz
    40: v_10400_hz  # 10400 Hz
    41: v_10800_hz  # 10800 Hz
    42: v_11200_hz  # 11200 Hz
    43: v_11600_hz  # 11600 Hz
    44: v_12000_hz  # 12000 Hz
    45: v_12400_hz  # 12400 Hz
    46: v_12800_hz  # 12800 Hz
    47: v_13200_hz  # 13200 Hz
    48: v_13600_hz  # 13600 Hz
    49: v_14000_hz  # 14000 Hz
    50: v_14400_hz  # 14400 Hz
    51: v_14800_hz  # 14800 Hz
    52: v_15200_hz  # 15200 Hz
    53: v_15600_hz  # 15600 Hz
    54: v_16000_hz  # 16000 Hz
    55: v_16400_hz  # 16400 Hz
    56: v_16800_hz  # 16800 Hz
    57: v_17200_hz  # 17200 Hz
    58: v_17600_hz  # 17600 Hz
    59: v_18000_hz  # 18000 Hz
    60: v_18400_hz  # 18400 Hz
    61: v_18800_hz  # 18800 Hz
    62: v_19200_hz  # 19200 Hz
    63: v_19600_hz  # 19600 Hz
    64: v_20000_hz  # 20000 Hz
    65: v_20400_hz  # 20400 Hz
    66: v_20800_hz  # 20800 Hz
    67: v_21200_hz  # 21200 Hz
    68: v_21600_hz  # 21600 Hz
    69: v_22000_hz  # 22000 Hz
    70: full  # Full
  early_select_values:
    0: v_0  # 0
    1: v_1  # 1
    2: v_2  # 2
    3: v_3  # 3
    4: v_4  # 4
    5: v_5  # 5
    6: v_6  # 6
    7: v_7  # 7
    8: v_8  # 8
    9: v_9  # 9
    10: v_10  # 10
    11: v_11  # 11
    12: v_12  # 12
    13: v_13  # 13
    14: v_14  # 14
    15: v_15  # 15
    16: v_16  # 16
    17: v_17  # 17
    18: v_18  # 18
    19: v_19  # 19
    20: v_20  # 20
    21: v_21  # 21
    22: v_22  # 22
    23: v_23  # 23
    24: v_24  # 24
    25: v_25  # 25
    26: v_26  # 26
    27: v_27  # 27
    28: v_28  # 28
    29: v_29  # 29
    30: v_30  # 30
    31: v_31  # 31
  delay_level_values:
    0: off  # off
    1: v_20_db  # -20 dB
    2: v_19_db  # -19 dB
    3: v_18_db  # -18 dB
    4: v_17_db  # -17 dB
    5: v_16_db  # -16 dB
    6: v_15_db  # -15 dB
    7: v_14_db  # -14 dB
    8: v_13_db  # -13 dB
    9: v_12_db  # -12 dB
    10: v_11_db  # -11 dB
    11: v_10_db  # -10 dB
    12: v_9_db  # -9 dB
    13: v_8_db  # -8 dB
    14: v_7_db  # -7 dB
    15: v_6_db  # -6 dB
  delay_time_values:
    0: v_100_msec  # 100 mSec
    1: v_108_msec  # 108 mSec
    2: v_116_msec  # 116 mSec
    3: v_124_msec  # 124 mSec
    4: v_132_msec  # 132 mSec
    5: v_140_msec  # 140 mSec
    6: v_148_msec  # 148 mSec
    7: v_156_msec  # 156 mSec
    8: v_164_msec  # 164 mSec
    9: v_172_msec  # 172 mSec
    10: v_180_msec  # 180 mSec
    11: v_188_msec  # 188 mSec
    12: v_196_msec  # 196 mSec
    13: v_204_msec  # 204 mSec
    14: v_212_msec  # 212 mSec
    15: v_220_msec  # 220 mSec
    16: v_228_msec  # 228 mSec
    17: v_236_msec  # 236 mSec
    18: v_244_msec  # 244 mSec
    19: v_252_msec  # 252 mSec
    20: v_260_msec  # 260 mSec
    21: v_268_msec  # 268 mSec
    22: v_276_msec  # 276 mSec
    23: v_284_msec  # 284 mSec
    24: v_292_msec  # 292 mSec
    25: v_300_msec  # 300 mSec
    26: v_308_msec  # 308 mSec
    27: v_316_msec  # 316 mSec
    28: v_324_msec  # 324 mSec
    29: v_332_msec  # 332 mSec
    30: v_340_msec  # 340 mSec
    31: v_348_msec  # 348 mSec
    32: v_356_msec  # 356 mSec
    33: v_364_msec  # 364 mSec
    34: v_372_msec  # 372 mSec
    35: v_380_msec  # 380 mSec
    36: v_388_msec  # 388 mSec
    37: v_396_msec  # 396 mSec
    38: v_404_msec  # 404 mSec
    39: v_412_msec  # 412 mSec
    40: v_420_msec  # 420 mSec
    41: v_428_msec  # 428 mSec
    42: v_436_msec  # 436 mSec
    43: v_444_msec  # 444 mSec
    44: v_452_msec  # 452 mSec
    45: v_460_msec  # 460 mSec
    46: v_468_msec  # 468 mSec
    47: v_476_msec  # 476 mSec
    48: v_484_msec  # 484 mSec
    49: v_492_msec  # 492 mSec
    50: v_500_msec  # 500 mSec
    51: v_508_msec  # 508 mSec
    52: v_516_msec  # 516 mSec
    53: v_524_msec  # 524 mSec
    54: v_532_msec  # 532 mSec
    55: v_540_msec  # 540 mSec
    56: v_548_msec  # 548 mSec
    57: v_556_msec  # 556 mSec
    58: v_564_msec  # 564 mSec
    59: v_572_msec  # 572 mSec
    60: v_580_msec  # 580 mSec
    61: v_588_msec  # 588 mSec
    62: v_596_msec  # 596 mSec
    63: v_604_msec  # 604 mSec
    64: v_612_msec  # 612 mSec
    65: v_620_msec  # 620 mSec
    66: v_628_msec  # 628 mSec
    67: v_636_msec  # 636 mSec
    68: v_644_msec  # 644 mSec
    69: v_652_msec  # 652 mSec
    70: v_660_msec  # 660 mSec
    71: v_668_msec  # 668 mSec
    72: v_676_msec  # 676 mSec
    73: v_684_msec  # 684 mSec
    74: v_692_msec  # 692 mSec
    75: v_700_msec  # 700 mSec
    76: v_708_msec  # 708 mSec
    77: v_716_msec  # 716 mSec
    78: v_724_msec  # 724 mSec
    79: v_732_msec  # 732 mSec
    80: v_740_msec  # 740 mSec
    81: v_748_msec  # 748 mSec
    82: v_756_msec  # 756 mSec
    83: v_764_msec  # 764 mSec
    84: v_772_msec  # 772 mSec
    85: v_780_msec  # 780 mSec
    86: v_788_msec  # 788 mSec
    87: v_796_msec  # 796 mSec
    88: v_804_msec  # 804 mSec
    89: v_812_msec  # 812 mSec
    90: v_820_msec  # 820 mSec
    91: v_828_msec  # 828 mSec
    92: v_836_msec  # 836 mSec
    93: v_844_msec  # 844 mSec
    94: v_852_msec  # 852 mSec
    95: v_860_msec  # 860 mSec
    96: v_868_msec  # 868 mSec
    97: v_876_msec  # 876 mSec
    98: v_884_msec  # 884 mSec
    99: v_892_msec  # 892 mSec
    100: v_900_msec  # 900 mSec
    101: v_908_msec  # 908 mSec
    102: v_916_msec  # 916 mSec
    103: v_924_msec  # 924 mSec
    104: v_932_msec  # 932 mSec
    105: v_940_msec  # 940 mSec
    106: v_948_msec  # 948 mSec
    107: v_956_msec  # 956 mSec
    108: v_964_msec  # 964 mSec
    109: v_972_msec  # 972 mSec
    110: v_980_msec  # 980 mSec
    111: v_988_msec  # 988 mSec
    112: v_996_msec  # 996 mSec
  delay_modulation_values:
    0: off  # off
    1: v_0  # 0
    2: v_1  # 1
    3: v_2  # 2
    4: v_3  # 3
    5: v_4  # 4
    6: v_5  # 5
    7: v_6  # 6
    8: v_7  # 7
    9: v_8  # 8
    10: v_9  # 9
    11: v_10  # 10
  display_values:
    28: idle_no_menu  # idle (no menu)
    29: browse_size_1  # browse: size (1)
    30: browse_predelay_2  # browse: predelay (2)
    31: browse_diffusion_3  # browse: diffusion (3)
    32: browse_density_4  # browse: density (4)
    33: browse_modulation_5  # browse: modulation (5)
    34: edit_predelay_2___browse_rolloff_6  # edit: predelay (2) / browse: rolloff (6)
    35: browse_hf_rt_multiply_7  # browse: hf rt multiply (7)
    36: browse_hf_rt_crossover_8  # browse: hf rt crossover (8)
    37: browse_lf_rt_multiply_9  # browse: lf rt multiply (9)
    38: browse_lf_rt_crossover_10  # browse: lf rt crossover (10)
    39: browse_vlf_cut_11  # browse: vlf cut (11)
    40: browse_early_to_reverb_mix_12  # browse: early to reverb mix (12)
    41: edit_diffusion_3___browse_early_rolloff_13  # edit: diffusion (3) / browse: early rolloff (13)
    42: browse_early_select_14  # browse: early select (14)
    43: browse_delay_level_15  # browse: delay level (15)
    44: browse_delay_time_16  # browse: delay time (16)
    45: browse_delay_modulation_17  # browse: delay modulation (17)
    46: browse_reverb_time_0  # browse: reverb time (0)
    55: edit_density_4  # edit: density (4)
    70: edit_modulation_5  # edit: modulation (5)
    78: edit_rolloff_6  # edit: rolloff (6)
    101: edit_hf_rt_multiply_7  # edit: hf rt multiply (7)
    115: edit_hf_rt_crossover_8  # edit: hf rt crossover (8)
    124: edit_vlf_cut_11  # edit: vlf cut (11)
    131: edit_early_to_reverb_mix_12  # edit: early to reverb mix (12)
    146: edit_early_rolloff_13  # edit: early rolloff (13)
    156: edit_early_select_14  # edit: early select (14)
    165: edit_delay_level_15  # edit: delay level (15)
    176: edit_delay_time_16  # edit: delay time (16)
    187: edit_delay_modulation_17  # edit: delay modulation (17)
    191: edit_lf_rt_multiply_9  # edit: lf rt multiply (9)
    196: edit_reverb_time_0  # edit: reverb time (0)
    199: edit_lf_rt_crossover_10  # edit: lf rt crossover (10)
    210: edit_size_1  # edit: size (1)

types:
  bank_index_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of bank_index_values.
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
        enum: bank_index_values

  reverb_time_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of reverb_time_values.
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
        enum: reverb_time_values

  size_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of size_values.
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
        enum: size_values

  predelay_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of predelay_values.
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
        enum: predelay_values

  rolloff_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of rolloff_values.
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
        enum: rolloff_values

  hf_rt_multiply_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of hf_rt_multiply_values.
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
        enum: hf_rt_multiply_values

  hf_rt_crossover_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of hf_rt_crossover_values.
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
        enum: hf_rt_crossover_values

  lf_rt_multiply_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of lf_rt_multiply_values.
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
        enum: lf_rt_multiply_values

  lf_rt_crossover_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of lf_rt_crossover_values.
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
        enum: lf_rt_crossover_values

  vlf_cut_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of vlf_cut_values.
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
        enum: vlf_cut_values

  early_to_reverb_mix_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of early_to_reverb_mix_values.
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
        enum: early_to_reverb_mix_values

  early_rolloff_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of early_rolloff_values.
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
        enum: early_rolloff_values

  early_select_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of early_select_values.
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
        enum: early_select_values

  delay_time_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of delay_time_values.
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
        enum: delay_time_values

  display_encoded:
    doc: |
      Two SysEx data bytes (each 0x00-0x0F); decoded value is a
      member of display_values.
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
        enum: display_values

  nibble_u8_hilo:
    doc: |
      Two SysEx data bytes that each hold a nibble (0x00-0x0F).
      Decoded value = (hi_nibble << 4) | lo_nibble.
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
