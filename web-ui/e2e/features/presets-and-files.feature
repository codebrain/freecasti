@core
Feature: Saved presets and dump files
  The user can snapshot their work as named presets, and exchange programs
  with other machines or the device via SysEx dump files.

  Background:
    Given the editor is started

  Scenario: Saving and loading a user preset restores the program
    When the user sets "predelay" to "20 ms"
    And the user saves the current program as "My Space"
    And the user sets "predelay" to "40 ms"
    And the user loads the saved preset "My Space"
    Then "predelay" shows "20 ms"

  Scenario: Saved presets survive a restart
    When the user saves the current program as "Keeper"
    And the editor is restarted
    Then the saved presets include "Keeper"

  Scenario: Deleting a saved preset removes it
    When the user saves the current program as "Scratch"
    And the user deletes the saved preset "Scratch"
    Then the saved presets do not include "Scratch"

  Scenario: The exported program file is a well-formed program dump
    When the user exports the current program to a file
    Then the exported file is a well-formed program dump

  Scenario: The exported system file is a well-formed system dump
    When the user exports the system settings to a file
    Then the exported file is a well-formed system dump

  Scenario: Importing a program file restores the program
    When the user sets "predelay" to "20 ms"
    And the user exports the current program to a file
    And the user sets "predelay" to "40 ms"
    And the user imports the exported file
    Then the "program" view is active
    And "predelay" shows "20 ms"

  Scenario: Locked parameters keep their value when a file is imported
    When the user sets "predelay" to "20 ms"
    And the user exports the current program to a file
    And the user sets "predelay" to "40 ms"
    And the user locks "predelay"
    And the user imports the exported file
    Then "predelay" shows "40 ms"

  Scenario: Importing a system file opens the System view
    When the user exports the system settings to a file
    And the user imports the exported file
    Then the "system" view is active
