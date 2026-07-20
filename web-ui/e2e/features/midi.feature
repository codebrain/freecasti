@core
Feature: MIDI communication with the device
  With a MIDI connection, the editor can push its state to the M7 and adopt
  dumps the device sends back. The editor recognizes echoes of its own
  transmissions so they are not treated as external changes.

  Background:
    Given the editor is started

  Scenario: Sending the current program transmits it byte-for-byte
    Given a MIDI connection to the device
    And send on change is disabled
    When the user exports the current program to a file
    And the user sends the current settings to the device
    Then the device receives a program dump
    And the last message the device received equals the exported file

  Scenario: Sending from the System view transmits a system dump
    Given a MIDI connection to the device
    And send on change is disabled
    When the user exports the system settings to a file
    And the user opens the "system" view
    And the user sends the current settings to the device
    Then the device receives a system dump
    And the last message the device received equals the exported file

  Scenario: Send on change transmits edits automatically
    Given a MIDI connection to the device
    And send on change is enabled
    When the user sets "predelay" to "20 ms"
    Then the device receives a program dump

  Scenario: Rapid edits are coalesced into one throttled transmission
    Given a MIDI connection to the device
    And send on change is enabled
    And the send on change throttle is 8000 ms
    When the user sets "predelay" to "20 ms"
    And the user sets "predelay" to "30 ms"
    And the user sets "predelay" to "40 ms"
    Then the device receives exactly 1 message
    And the last message the device received is a program dump

  Scenario: An incoming program dump replaces the editor state
    Given a MIDI connection to the device
    And send on change is disabled
    When the user selects factory program "Large Hall" from bank "Halls v1"
    And the user sends the current settings to the device
    And the device receives a program dump
    And the user selects factory program "Bright Plate" from bank "Plates v1"
    And the echo window has passed
    And the device sends back the last message it received
    Then the "program" view is active
    And the program name is "Large Hall"

  Scenario: An incoming system dump opens the System view
    Given a MIDI connection to the device
    And send on change is disabled
    When the user opens the "system" view
    And the user sends the current settings to the device
    And the device receives a system dump
    And the user opens the "program" view
    And the echo window has passed
    And the device sends back the last message it received
    Then the "system" view is active

  Scenario: A device echo of the editor's own transmission is not an external change
    Given a MIDI connection to the device
    And send on change is enabled
    When the user sets "predelay" to "20 ms"
    And the device receives a program dump
    And the device sends back the last message it received
    Then the editor records the message as an echo of its own transmission

  Scenario: The editor reports when no MIDI transport is available
    Given the MIDI transport is unavailable
    When the editor is restarted
    Then the editor reports that MIDI is unavailable
