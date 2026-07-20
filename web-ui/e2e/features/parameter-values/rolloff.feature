# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "rolloff"
  The device supports a fixed table of 71 steps for
  "rolloff". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "rolloff"
    Given the editor is started
    Then the only values available for "rolloff" are:
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
      | 5200 Hz |
      | 5600 Hz |
      | 6000 Hz |
      | 6400 Hz |
      | 6800 Hz |
      | 7200 Hz |
      | 7600 Hz |
      | 8000 Hz |
      | 8400 Hz |
      | 8800 Hz |
      | 9200 Hz |
      | 9600 Hz |
      | 10000 Hz |
      | 10400 Hz |
      | 10800 Hz |
      | 11200 Hz |
      | 11600 Hz |
      | 12000 Hz |
      | 12400 Hz |
      | 12800 Hz |
      | 13200 Hz |
      | 13600 Hz |
      | 14000 Hz |
      | 14400 Hz |
      | 14800 Hz |
      | 15200 Hz |
      | 15600 Hz |
      | 16000 Hz |
      | 16400 Hz |
      | 16800 Hz |
      | 17200 Hz |
      | 17600 Hz |
      | 18000 Hz |
      | 18400 Hz |
      | 18800 Hz |
      | 19200 Hz |
      | 19600 Hz |
      | 20000 Hz |
      | 20400 Hz |
      | 20800 Hz |
      | 21200 Hz |
      | 21600 Hz |
      | 22000 Hz |
      | Full |
