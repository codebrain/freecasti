[Overview](../README.md) | **Parameters** | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Program parameters

All **program sound parameters** on the Bricasti M7, in front-panel menu order. Descriptions are from the owner's manual and V2 addendum (hint only — dumps on your unit are authoritative). Each row links to a capture-series page with full encoding tables when available.

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

_Last exported: 2026-07-18_

Printed ranges and UI labels may differ from this unit's captures (for example Early Select 0–31 vs manual 0–20). See [parameter-catalog.md](../../../docs/parameter-catalog.md) for capture hints, [encoding sources](../../../docs/encoding-sources.md) for witness types, and [../README.md](../README.md) for the program-dump overview.
