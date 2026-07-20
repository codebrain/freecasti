@core
Feature: Editor lifecycle and persistence
  The M7 editor opens on the Program view with a factory program loaded,
  and preserves the user's work between sessions.

  Background:
    Given the editor is started

  Scenario: A fresh editor opens on the Program view with a program loaded
    Then the "program" view is active
    And a program name is shown

  Scenario: The active view is remembered between sessions
    When the user opens the "system" view
    And the editor is restarted
    Then the "system" view is active

  Scenario: Edits and the tempo survive a restart
    When the user sets "predelay" to "20 ms"
    And the user sets the tempo to 140 BPM
    And the editor is restarted
    Then "predelay" shows "20 ms"
    And the tempo shows 140 BPM

  Scenario: Parameter locks survive a restart
    When the user locks "predelay"
    And the editor is restarted
    And the user selects factory program "Medium Hall" from bank "Halls v1"
    Then "predelay" shows "10 ms"
