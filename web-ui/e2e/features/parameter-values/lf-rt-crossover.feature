# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "lf rt crossover"
  The device supports a fixed table of 27 steps for
  "lf rt crossover". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "lf rt crossover"
    Given the editor is started
    Then the only values available for "lf rt crossover" are:
      | 80 Hz |
      | 120 Hz |
      | 160 Hz |
      | 200 Hz |
      | 240 Hz |
      | 280 Hz |
      | 320 Hz |
      | 360 Hz |
      | 400 Hz |
      | 480 Hz |
      | 560 Hz |
      | 640 Hz |
      | 720 Hz |
      | 800 Hz |
      | 1000 Hz |
      | 1200 Hz |
      | 1400 Hz |
      | 1600 Hz |
      | 1800 Hz |
      | 2000 Hz |
      | 2400 Hz |
      | 2800 Hz |
      | 3200 Hz |
      | 3600 Hz |
      | 4000 Hz |
      | 4400 Hz |
      | 4800 Hz |
