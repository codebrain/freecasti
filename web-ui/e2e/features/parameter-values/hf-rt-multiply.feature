# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "hf rt multiply"
  The device supports a fixed table of 17 steps for
  "hf rt multiply". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "hf rt multiply"
    Given the editor is started
    Then the only values available for "hf rt multiply" are:
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
