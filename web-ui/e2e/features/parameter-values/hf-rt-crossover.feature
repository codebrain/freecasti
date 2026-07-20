# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "hf rt crossover"
  The device supports a fixed table of 37 steps for
  "hf rt crossover". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "hf rt crossover"
    Given the editor is started
    Then the only values available for "hf rt crossover" are:
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
      | 4800 Hz |
      | 5600 Hz |
      | 6400 Hz |
      | 7200 Hz |
      | 8000 Hz |
      | 8800 Hz |
      | 9600 Hz |
      | 10400 Hz |
      | 11200 Hz |
      | 12000 Hz |
      | 12800 Hz |
      | 13600 Hz |
      | 14400 Hz |
      | 15200 Hz |
      | 16000 Hz |
