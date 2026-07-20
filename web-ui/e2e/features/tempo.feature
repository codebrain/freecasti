@core
Feature: Tempo and note-division editing
  A master tempo lets time parameters be edited as musical note divisions
  instead of raw device times.

  Background:
    Given the editor is started

  Scenario: The tempo defaults to 120 BPM
    Then the tempo shows 120 BPM

  Scenario Outline: The tempo is clamped to the supported range
    When the user sets the tempo to <typed> BPM
    Then the tempo shows <shown> BPM

    Examples:
      | typed | shown |
      | 500   | 300   |
      | 5     | 20    |

  Scenario: The tempo is remembered between sessions
    When the user sets the tempo to 97 BPM
    And the editor is restarted
    Then the tempo shows 97 BPM

  Scenario Outline: Tempo mode offers straight, triplet and dotted note divisions
    When the user sets the tempo to 120 BPM
    And the user enables tempo mode for "predelay"
    And the user sets "predelay" to "<division>"
    Then "predelay" shows "<division>"
    When the user disables tempo mode for "predelay"
    Then "predelay" shows "<device time>"

    # At 120 BPM a quarter note lasts 500 ms. "T" marks triplets (2/3 of the
    # straight note) and "D" dotted notes (1.5x). Each division snaps to the
    # nearest time step the device supports, shown when tempo mode is off.
    Examples:
      | division | device time |
      | 1/32     | 64 ms       |
      | 1/16T    | 84 ms       |
      | 1/16     | 124 ms      |
      | 1/8T     | 164 ms      |
      | 1/16D    | 188 ms      |
      | 1/8      | 252 ms      |
      | 1/4T     | 332 ms      |
      | 1/8D     | 372 ms      |
      | 1/4      | 500 ms      |

  Scenario Outline: Divisions the device cannot hit exactly report their timing error
    When the user sets the tempo to <tempo> BPM
    And the user enables tempo mode for "predelay"
    And the user sets "predelay" to "<division>"
    Then "predelay" reports a timing error of <error> ms

    # An eighth note at 120 BPM is ideally 250 ms, but the closest predelay
    # step is 252 ms; at 97 BPM the ideal 309.3 ms lands on the 308 ms step.
    Examples:
      | tempo | division | error |
      | 120   | 1/8      | 2     |
      | 97    | 1/8      | -1.3  |

  Scenario: Divisions that land exactly on a device step report no timing error
    When the user sets the tempo to 120 BPM
    And the user enables tempo mode for "predelay"
    And the user sets "predelay" to "1/4"
    Then "predelay" reports no timing error
