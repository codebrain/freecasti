# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "midi bank"
  The device supports a fixed table of 14 steps for
  "midi bank". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "midi bank"
    Given the editor is started
    And the user opens the "system" view
    Then the only values available for "midi bank" are:
      | Halls |
      | Plates |
      | Rooms |
      | Chambers |
      | Ambience |
      | Spaces |
      | Halls 2 |
      | Plates 2 |
      | Rooms 2 |
      | Spaces 2 |
      | Nonlin |
      | Edit |
      | Regs |
      | Favs |
