# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "dry gain"
  The device supports a fixed table of 122 steps for
  "dry gain". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "dry gain"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "dry gain" are:
      | Off |
      | -60 dB |
      | -59.5 dB |
      | -59 dB |
      | -58.5 dB |
      | -58 dB |
      | -57.5 dB |
      | -57 dB |
      | -56.5 dB |
      | -56 dB |
      | -55.5 dB |
      | -55 dB |
      | -54.5 dB |
      | -54 dB |
      | -53.5 dB |
      | -53 dB |
      | -52.5 dB |
      | -52 dB |
      | -51.5 dB |
      | -51 dB |
      | -50.5 dB |
      | -50 dB |
      | -49.5 dB |
      | -49 dB |
      | -48.5 dB |
      | -48 dB |
      | -47.5 dB |
      | -47 dB |
      | -46.5 dB |
      | -46 dB |
      | -45.5 dB |
      | -45 dB |
      | -44.5 dB |
      | -44 dB |
      | -43.5 dB |
      | -43 dB |
      | -42.5 dB |
      | -42 dB |
      | -41.5 dB |
      | -41 dB |
      | -40.5 dB |
      | -40 dB |
      | -39.5 dB |
      | -39 dB |
      | -38.5 dB |
      | -38 dB |
      | -37.5 dB |
      | -37 dB |
      | -36.5 dB |
      | -36 dB |
      | -35.5 dB |
      | -35 dB |
      | -34.5 dB |
      | -34 dB |
      | -33.5 dB |
      | -33 dB |
      | -32.5 dB |
      | -32 dB |
      | -31.5 dB |
      | -31 dB |
      | -30.5 dB |
      | -30 dB |
      | -29.5 dB |
      | -29 dB |
      | -28.5 dB |
      | -28 dB |
      | -27.5 dB |
      | -27 dB |
      | -26.5 dB |
      | -26 dB |
      | -25.5 dB |
      | -25 dB |
      | -24.5 dB |
      | -24 dB |
      | -23.5 dB |
      | -23 dB |
      | -22.5 dB |
      | -22 dB |
      | -21.5 dB |
      | -21 dB |
      | -20.5 dB |
      | -20 dB |
      | -19.5 dB |
      | -19 dB |
      | -18.5 dB |
      | -18 dB |
      | -17.5 dB |
      | -17 dB |
      | -16.5 dB |
      | -16 dB |
      | -15.5 dB |
      | -15 dB |
      | -14.5 dB |
      | -14 dB |
      | -13.5 dB |
      | -13 dB |
      | -12.5 dB |
      | -12 dB |
      | -11.5 dB |
      | -11 dB |
      | -10.5 dB |
      | -10 dB |
      | -9.5 dB |
      | -9 dB |
      | -8.5 dB |
      | -8 dB |
      | -7.5 dB |
      | -7 dB |
      | -6.5 dB |
      | -6 dB |
      | -5.5 dB |
      | -5 dB |
      | -4.5 dB |
      | -4 dB |
      | -3.5 dB |
      | -3 dB |
      | -2.5 dB |
      | -2 dB |
      | -1.5 dB |
      | -1 dB |
      | -0.5 dB |
      | Full |
