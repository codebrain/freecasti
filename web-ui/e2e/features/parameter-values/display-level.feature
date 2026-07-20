# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "display level"
  The device supports a fixed table of 5 steps for
  "display level". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "display level"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "display level" are:
      | Dim |
      | 1 |
      | 2 |
      | 3 |
      | Bright |
