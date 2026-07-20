# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "predelay"
  The device supports a fixed table of 86 steps for
  "predelay". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "predelay"
    Given the editor is started
    Then the only values available for "predelay" are:
      | 0 ms |
      | 2 ms |
      | 4 ms |
      | 6 ms |
      | 8 ms |
      | 10 ms |
      | 12 ms |
      | 14 ms |
      | 16 ms |
      | 18 ms |
      | 20 ms |
      | 22 ms |
      | 24 ms |
      | 26 ms |
      | 28 ms |
      | 30 ms |
      | 32 ms |
      | 34 ms |
      | 36 ms |
      | 38 ms |
      | 40 ms |
      | 44 ms |
      | 48 ms |
      | 52 ms |
      | 56 ms |
      | 60 ms |
      | 64 ms |
      | 68 ms |
      | 72 ms |
      | 76 ms |
      | 80 ms |
      | 84 ms |
      | 88 ms |
      | 92 ms |
      | 96 ms |
      | 100 ms |
      | 108 ms |
      | 116 ms |
      | 124 ms |
      | 132 ms |
      | 140 ms |
      | 148 ms |
      | 156 ms |
      | 164 ms |
      | 172 ms |
      | 180 ms |
      | 188 ms |
      | 196 ms |
      | 204 ms |
      | 212 ms |
      | 220 ms |
      | 228 ms |
      | 236 ms |
      | 244 ms |
      | 252 ms |
      | 260 ms |
      | 268 ms |
      | 276 ms |
      | 284 ms |
      | 292 ms |
      | 300 ms |
      | 308 ms |
      | 316 ms |
      | 324 ms |
      | 332 ms |
      | 340 ms |
      | 348 ms |
      | 356 ms |
      | 364 ms |
      | 372 ms |
      | 380 ms |
      | 388 ms |
      | 396 ms |
      | 404 ms |
      | 412 ms |
      | 420 ms |
      | 428 ms |
      | 436 ms |
      | 444 ms |
      | 452 ms |
      | 460 ms |
      | 468 ms |
      | 476 ms |
      | 484 ms |
      | 492 ms |
      | 500 ms |
