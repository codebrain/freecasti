# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "density"
  The device supports a fixed table of 11 steps for
  "density". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "density"
    Given the editor is started
    Then the only values available for "density" are:
      | Low |
      | 1 |
      | 2 |
      | 3 |
      | 4 |
      | 5 |
      | 6 |
      | 7 |
      | 8 |
      | 9 |
      | High |
