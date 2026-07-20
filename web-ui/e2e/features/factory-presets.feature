@core
Feature: Factory presets
  Factory programs are organized in banks. Loading one replaces the
  editable parameters, except those the user has locked.

  Background:
    Given the editor is started

  Scenario: Selecting a factory program loads it
    When the user selects factory program "Bright Plate" from bank "Plates v1"
    Then the program name is "Bright Plate"

  Scenario: Loading a preset replaces unlocked parameter values
    When the user sets "predelay" to "40 ms"
    And the user selects factory program "Large Hall" from bank "Halls v1"
    Then "predelay" shows "10 ms"

  Scenario: Locked parameters keep their value when a preset is loaded
    When the user sets "predelay" to "40 ms"
    And the user locks "predelay"
    And the user selects factory program "Large Hall" from bank "Halls v1"
    Then "predelay" shows "40 ms"

  Scenario: Unlocking a parameter lets presets change it again
    When the user sets "predelay" to "40 ms"
    And the user locks "predelay"
    And the user unlocks "predelay"
    And the user selects factory program "Large Hall" from bank "Halls v1"
    Then "predelay" shows "10 ms"

  Scenario: NonLin programs disable parameters that have no effect
    When the user selects factory program "Nonlin A" from bank "NonLin"
    Then parameter "reverb time" is not editable
    And parameter "density" is not editable
    And parameter "size" is editable
    And parameter "predelay" is editable
