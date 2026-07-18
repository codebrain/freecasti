# Rolloff filter slopes (measured)

Hand-maintained interpretation of the **Rolloff** and **Early Rolloff** low-pass
filters. Bricasti publishes the *frequency ranges* for both controls but not the
filter *order* (dB/octave). This page records what is documented, what an
independent measurement of the response shows, and how to confirm it on your own
unit. See the generated parameter pages for byte encodings:
[Rolloff](../specification/prog/bytes/rolloff.md) ·
[Early Rolloff](../specification/prog/bytes/early-rolloff.md).

## What Bricasti documents

Bricasti defines **Rolloff** as a low-pass filter on the overall **late-reverb
output**, while **Early Rolloff** is a separate low-pass filter for the
**early-reflection** field. These are distinct from the HF decay-time multiplier
and crossover controls (HF RT Multiply / HF RT Crossover). Bricasti gives the
frequency ranges, but not the filter order or dB/octave.

Bricasti explicitly states that:

- The **V2** late-reverb rolloff is **gentler** than V1.
- The **early-reverb engine is the same** for V1 and V2.
- Only the **late-reverb construction** changes between the two algorithm
  versions.

_Sources: [M7 Owner's Manual](https://www.bricasti.com/images/M7.pdf),
[V2 Manual Addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)._

## Independent measurement

Beyond Bricasti's published ranges, an independent measurement of the M7's
frequency profile at every rolloff position — taken separately for early
reflections, V1 late reverb, and V2 late reverb — describes three families:

- **Reflections:** shallow rolloff.
- **V1 late reverb:** very fast rolloff.
- **V2 late reverb:** shallower / lower-order rolloff.

## What the response curve measures as

Fitting the measured response (from the real screenshot rather than a redrawn
comparison graphic):

The thick **V1 late-reverb** curve (Halls 1 family) fits a conventional low-pass
response with:

- filter order ≈ **1.92**, i.e. `1.92 × 6.02 ≈ 11.6 dB/octave`
- a fixed second-order fit gives an effective corner of **≈ 1.82 kHz** with a fit
  error of **≈ 0.63 dB**
- a fourth-order (24 dB/octave) fit is substantially worse, **≈ 2.57 dB** error

Approximate values read from the fitted V1 curve:

| Frequency | Level |
|-----------|-------|
| 900 Hz | −0.3 dB |
| 1.8 kHz | −3.1 dB |
| 3.6 kHz | −12.1 dB |
| 7.2 kHz | −23.4 dB |

That is essentially textbook **12 dB/octave** behaviour: it reaches roughly
−24 dB after about two octaves, whereas a 24 dB/octave filter would reach about
−24 dB only one octave above its corner.

The faint **Early Rolloff** curve fits approximately **5.5 dB/octave**, so it is
very likely intended as a **6 dB/octave, one-pole** response.

Interestingly, the displayed Early Rolloff value of 3.6 kHz does **not** appear to
represent its conventional −3 dB corner. The plotted curve reaches about −3 dB
nearer **7–8 kHz**. That suggests the M7's displayed early-rolloff frequency is a
proprietary parameterisation or nominal onset frequency, not necessarily the
standard electrical cutoff definition.

## Best current model

| M7 path | Most likely response | Confidence |
|---------|----------------------|------------|
| Early reflections | 6 dB/octave | High |
| V1 late reverb — Halls 1, Rooms 1, etc. | 12 dB/octave | High |
| V2 late reverb — Halls 2, Rooms 2, etc. | Probably 6 dB/octave or another one-pole-like curve | Moderate |
| NonLin algorithm | Unknown | Low |

The **V2 = 6 dB/octave** conclusion is still an inference rather than a published
specification. It is consistent with Bricasti calling V2 *gentler*, the
independent measurement calling it *lower-order*, and the shared early curve
appearing to be one-pole.

## How to establish it definitively on your M7

Because Bricasti says the Rolloff filter is applied to the reverb output, it
should be measurable very accurately by division:

1. Use AES input and output and set the M7 to **wet-only**.
2. Set HF and LF RT multipliers to **1.0**, VLF **off**, delay **off**, and
   modulation **off** where possible.
3. Isolate late reverb with the **Early/Reverb** balance.
4. Record 30–60 seconds of white noise with Rolloff set to **Full**.
5. Repeat at a chosen rolloff frequency.
6. Average the power spectra and **divide** the filtered capture by the Full
   capture.
7. Repeat with a Halls 1 preset, a Halls 2 preset, and early reflections
   isolated.

That will cancel most of the reverb's inherent spectrum and expose the actual
static filter response. It would also reveal whether the curves are Butterworth,
critically damped, cascaded one-poles, or a custom shape.
