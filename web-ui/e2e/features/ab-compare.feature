@core
Feature: A/B program compare
  The editor holds two independent program slots, A and B, so two settings
  of a program can be compared. Edits apply to the active slot only.

  Background:
    Given the editor is started

  Scenario: Slot A is active by default
    Then compare slot "A" is active

  Scenario: Edits apply only to the active slot
    When the user sets "reverb time" to "2.5 s"
    And the user activates compare slot "B"
    Then "reverb time" does not show "2.5 s"
    When the user activates compare slot "A"
    Then "reverb time" shows "2.5 s"

  Scenario: Each slot can hold a different factory program
    When the user selects factory program "Bright Plate" from bank "Plates v1"
    And the user activates compare slot "B"
    And the user selects factory program "Large Hall" from bank "Halls v1"
    Then the program name is "Large Hall"
    When the user activates compare slot "A"
    Then the program name is "Bright Plate"

  Scenario: Swapping exchanges the contents of the two slots
    When the user sets "reverb time" to "2.5 s"
    And the user activates compare slot "B"
    And the user sets "reverb time" to "3 s"
    And the user swaps the compare slots
    Then "reverb time" shows "2.5 s"
    When the user activates compare slot "A"
    Then "reverb time" shows "3 s"

  Scenario: Parameter locks are shared by both slots
    # "Bright Plate" would set predelay to 0 ms; the lock placed while slot A
    # was active also protects slot B.
    When the user locks "predelay"
    And the user activates compare slot "B"
    And the user selects factory program "Bright Plate" from bank "Plates v1"
    Then "predelay" shows "10 ms"

  Scenario: Parameter locks survive a slot swap
    When the user locks "predelay"
    And the user swaps the compare slots
    And the user selects factory program "Bright Plate" from bank "Plates v1"
    Then "predelay" shows "10 ms"
