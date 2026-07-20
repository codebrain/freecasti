# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "vlf cut"
  The device supports a fixed table of 21 steps for
  "vlf cut". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "vlf cut"
    Given the editor is started
    Then the only values available for "vlf cut" are:
      | -20 dB |
      | -19 dB |
      | -18 dB |
      | -17 dB |
      | -16 dB |
      | -15 dB |
      | -14 dB |
      | -13 dB |
      | -12 dB |
      | -11 dB |
      | -10 dB |
      | -9 dB |
      | -8 dB |
      | -7 dB |
      | -6 dB |
      | -5 dB |
      | -4 dB |
      | -3 dB |
      | -2 dB |
      | -1 dB |
      | 0 dB |
