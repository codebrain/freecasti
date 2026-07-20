# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "audio routing"
  The device supports a fixed table of 3 steps for
  "audio routing". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "audio routing"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "audio routing" are:
      | Stereo |
      | Mono L |
      | Mono R |
