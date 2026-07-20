@core
Feature: Device display follows the editor selection
  Program dumps embed the M7's front-panel state. When a parameter's control
  is selected in the editor, the transmitted dump makes the device highlight
  that same parameter on its own display, so the hardware follows along.

  Background:
    Given the editor is started
    And a MIDI connection to the device
    And send on change is enabled

  Scenario Outline: Selecting a control highlights its parameter on the device
    When the user selects the "<parameter>" control
    Then the device receives a program dump
    And the device display highlights "<parameter>"

    Examples:
      | parameter   |
      | reverb time |
      | predelay    |
      | delay time  |

  Scenario: Moving the selection moves the device's highlight
    When the user selects the "predelay" control
    Then the device display highlights "predelay"
    When the user selects the "size" control
    Then the device display highlights "size"

  Scenario: Deselecting returns the device display to idle
    When the user selects the "predelay" control
    Then the device display highlights "predelay"
    When the user deselects the control
    Then the device display returns to idle
