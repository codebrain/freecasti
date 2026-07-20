@target-specific
Feature: Pointer and keyboard gestures
  Gesture-level interaction mechanics of this editor's dials and controls.
  Other targets have their own idioms, so these stay out of the core specs.

  Background:
    Given the editor is started

  Scenario: Dragging a dial upward increases the value
    Given the user sets "predelay" to "0 ms"
    When the user drags the "predelay" dial up
    Then "predelay" does not show "0 ms"

  Scenario: The mouse wheel steps a dial
    Given the user sets "predelay" to "0 ms"
    When the user scrolls the mouse wheel up over the "predelay" dial
    Then "predelay" does not show "0 ms"

  Scenario: Double-clicking a dial jumps back to the preset's default value
    # "Large Hall" (the initial program) has a factory predelay of 10 ms.
    Given the user sets "predelay" to "40 ms"
    When the user double-clicks the "predelay" dial
    Then "predelay" shows "10 ms"

  Scenario: Arrow keys step the selected control
    Given the user sets "predelay" to "20 ms"
    When the user clicks the "predelay" dial
    And the user presses the "ArrowUp" key
    Then "predelay" shows "22 ms"

  Scenario: Escape clears the selection so arrow keys do nothing
    Given the user sets "predelay" to "20 ms"
    When the user clicks the "predelay" dial
    And the user presses the "Escape" key
    And the user presses the "ArrowUp" key
    Then "predelay" shows "20 ms"

  Scenario: Typing into a value can be cancelled with Escape
    Given the user sets "predelay" to "20 ms"
    When the user starts typing "999 ms" into "predelay" and presses Escape
    Then "predelay" shows "20 ms"
