# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "midi channel"
  The device supports a fixed table of 17 steps for
  "midi channel". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "midi channel"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "midi channel" are:
      | 1 |
      | 2 |
      | 3 |
      | 4 |
      | 5 |
      | 6 |
      | 7 |
      | 8 |
      | 9 |
      | 10 |
      | 11 |
      | 12 |
      | 13 |
      | 14 |
      | 15 |
      | 16 |
      | Omni |
