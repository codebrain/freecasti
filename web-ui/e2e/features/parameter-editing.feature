@core
Feature: Parameter editing
  Parameters accept human-readable values in device units. Input that the
  device cannot represent is either snapped to the nearest step or ignored.

  Background:
    Given the editor is started

  Scenario: Setting a time parameter to an exact device step
    When the user sets "predelay" to "20 ms"
    Then "predelay" shows "20 ms"

  Scenario: Values snap to the nearest device step
    When the user sets "predelay" to "23 ms"
    Then "predelay" shows "22 ms"

  Scenario: Seconds are accepted for reverb time
    When the user sets "reverb time" to "2.5 s"
    Then "reverb time" shows "2.5 s"

  Scenario: Invalid input is ignored
    When the user sets "predelay" to "20 ms"
    And the user sets "predelay" to "banana"
    Then "predelay" shows "20 ms"

  Scenario: Named steps can be chosen by name
    When the user sets "diffusion" to "High"
    Then "diffusion" shows "High"

  Scenario: Enumerated parameters offer a fixed set of choices
    Given the user opens the "system" view
    When the user sets "audio routing" to "Mono L"
    Then "audio routing" shows "Mono L"

  Scenario: System levels are edited in dB
    Given the user opens the "system" view
    When the user sets "wet gain" to "-12 dB"
    Then "wet gain" shows "-12 dB"
