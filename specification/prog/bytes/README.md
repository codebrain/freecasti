[Overview](../README.md) | **Bytes** | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Program dump bytes

Documented **program dump** payload fields: the 18 front-panel sound parameters (in menu order), identity/register bytes, and UI/menu bytes such as the LCD cursor. Sound-parameter descriptions are from the owner's manual and V2 addendum (hint only — dumps on your unit are authoritative). Each row links to a page with encoding tables when captures exist.

| Parameter | SysEx (offsets · encoding · confidence) | Description |
|-----------|----------------------------------------|-------------|
| [Reverb Time](reverb-time.md) | `100-101` · `nibble_hilo` · medium | Mid-frequency reverb time. Sets the reverb time of the mid frequencies when the signal stops. |
| [Size](size.md) | `102-103` · `nibble_hilo` · high | Adjusts the apparent size of the late reverberant field. |
| [Pre Delay](predelay.md) | `104-105` · `nibble_hilo` · medium | Sets the amount of time which elapses between the input signal and the onset of reverberation. |
| [Diffusion](diffusion.md) | `107` · `raw_u8` · high | Sets initial diffusion of the reverb. Displayed and controlled as a percentage change from the initial value defined by the preset. |
| [Density](density.md) | `109` · `raw_u8` · high | Sets how the echo density builds up over time. |
| [Modulation](modulation.md) | `111` · `raw_u8` · high | Controls the amount of modulation and pitch variation in the later part of the reverberant field. |
| [Rolloff](rolloff.md) | `112-113` · `nibble_hilo` · medium | Low pass filter applied to the overall output of the reverb. |
| [HF RT Multiply](hf-rt-multiply.md) | `114-115` · `nibble_hilo` · high | Sets the high-frequency reverb time above the crossover frequency set by HF RT Crossover. Displayed and controlled as a scaling of Reverb Time. |
| [HF RT Crossover](hf-rt-crossover.md) | `116-117` · `nibble_hilo` · medium | Sets the crossover frequency used by HF RT Multiply. |
| [LF RT Multiply](lf-rt-multiply.md) | `118-119` · `nibble_hilo` · medium | Sets the low-frequency reverb time below the crossover frequency set by LF RT Crossover. Displayed and controlled as a scaling of Reverb Time. |
| [LF RT Crossover](lf-rt-crossover.md) | `120-121` · `nibble_hilo` · medium | Sets the crossover frequency used by LF RT Multiply. |
| [VLF Cut](vlf-cut.md) | `122-123` · `nibble_hilo` · high | Cuts the very low frequency content of the initial part of both the early and late reverberant fields. |
| [Early/Reverb Mix](early-to-reverb-mix.md) | `124-125` · `nibble_hilo` · high | Sets the balance between the early and later parts of the reverberant fields. |
| [Early Rolloff](early-rolloff.md) | `126-127` · `nibble_hilo` · medium | Sets the rolloff frequency point of the low pass filter for the early part of the reverberant field. |
| [Early Select](early-select.md) | `128-129` · `nibble_hilo` · high | Controls the build up and decay characteristics of the early part of the reverberant field. The V2 addendum expands the selection beyond the printed 0–20 to 0–31 with larger, more spread-out early variants for a slower early reverb build-up (available on both V1 and V2 algorithm presets). |
| [Delay Level](delay-level.md) | `133` · `raw_u8` · high | Level of the delayed input injected into the start of the late reverb (not the early reverb). The delayed sound is the original input signal, delayed, diffused, and band-limited by Rolloff. |
| [Delay Time](delay-time.md) | `134-135` · `nibble_hilo` · high | Delay time for a diffused set of eight voices spread in time (controlled as a single delay). Adds coloration and a late swell to the late reverb. |
| [Delay Modulation](delay-modulation.md) | `139` · `raw_u8` · high | Modulates the delay voices only (not the reverb), similar in character to reverb Modulation: low settings are slower and more shallow; higher settings are more random and deeper. |
| [Display](display.md) | `146-147` · `nibble_hilo` · high | LCD cursor / edit-display position in the program dump (not a sound parameter). Captured under `sysex/prog/menus/`. |
| [Program name](program-name.md) | `8-21` · `ascii_space_padded` · high | 14-character editable ASCII program/register label (manual); space-padded within offsets 8–21. |
| [Program name pad](program-name-pad.md) | `22-23` · `raw_bytes` · high | Trailing space pad (`20 20`) completing the 16-byte wire name window. |
| [Register bank](register-bank.md) | `93` · `raw_u8` · high | User Registers Bank (manual B0–B4) when the dump basis is a register; see `sysex/prog/edit/registers/`. |
| [Register](register.md) | `95` · `raw_u8` · high | User Register number within bank (manual 0–9) when the dump basis is a register. |

_Last exported: 2026-07-19_

Printed ranges and UI labels may differ from this unit's captures (for example Early Select 0–31 vs manual 0–20). See [parameter-catalog.md](../../../docs/parameter-catalog.md) for capture hints, [encoding sources](../../../docs/encoding-sources.md) for witness types, and [../README.md](../README.md) for the program-dump overview.
