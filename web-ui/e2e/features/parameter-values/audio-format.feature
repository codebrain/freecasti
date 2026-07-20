# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "audio format"
  The device supports a fixed table of 2 steps for
  "audio format". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "audio format"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "audio format" are:
      | Analog |
      | Digital |
