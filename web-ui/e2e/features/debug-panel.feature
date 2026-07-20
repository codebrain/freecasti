@target-specific
Feature: Debug panel
  A side drawer showing the last change, the MIDI SysEx traffic log, and
  tempo timing discrepancies.

  Background:
    Given the editor is started

  Scenario: The debug panel opens and stays open between sessions
    When the user opens the debug panel
    Then the debug panel is shown
    When the editor is restarted
    Then the debug panel is shown

  Scenario: The last change is summarized
    When the user sets "predelay" to "20 ms"
    And the user opens the debug panel
    Then the last change shows "predelay" changing to "20 ms"

  Scenario: Transmitted SysEx appears in the MIDI log
    Given a MIDI connection to the device
    And send on change is disabled
    When the user sends the current settings to the device
    And the device receives a program dump
    And the user opens the debug panel
    Then the MIDI log shows a transmitted program dump

  Scenario: The MIDI log can be cleared
    Given a MIDI connection to the device
    And send on change is disabled
    When the user sends the current settings to the device
    And the device receives a program dump
    And the user opens the debug panel
    And the user clears the MIDI log
    Then the MIDI log is empty
