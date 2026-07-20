# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "lf rt multiply"
  The device supports a fixed table of 57 steps for
  "lf rt multiply". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "lf rt multiply"
    Given the editor is started
    Then the only values available for "lf rt multiply" are:
      | 0.2x |
      | 0.25x |
      | 0.3x |
      | 0.35x |
      | 0.4x |
      | 0.45x |
      | 0.5x |
      | 0.55x |
      | 0.6x |
      | 0.65x |
      | 0.7x |
      | 0.75x |
      | 0.8x |
      | 0.85x |
      | 0.9x |
      | 0.95x |
      | 1x |
      | 1.05x |
      | 1.1x |
      | 1.15x |
      | 1.2x |
      | 1.25x |
      | 1.3x |
      | 1.35x |
      | 1.4x |
      | 1.45x |
      | 1.5x |
      | 1.55x |
      | 1.6x |
      | 1.65x |
      | 1.7x |
      | 1.75x |
      | 1.8x |
      | 1.85x |
      | 1.9x |
      | 1.95x |
      | 2x |
      | 2.1x |
      | 2.2x |
      | 2.3x |
      | 2.4x |
      | 2.5x |
      | 2.6x |
      | 2.7x |
      | 2.8x |
      | 2.9x |
      | 3.0x |
      | 3.1x |
      | 3.2x |
      | 3.3x |
      | 3.4x |
      | 3.5x |
      | 3.6x |
      | 3.7x |
      | 3.8x |
      | 3.9x |
      | 4x |
