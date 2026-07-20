# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "size"
  The device supports a fixed table of 31 steps for
  "size". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "size"
    Given the editor is started
    Then the only values available for "size" are:
      | Small |
      | 1 |
      | 2 |
      | 3 |
      | 4 |
      | 5 |
      | 6 |
      | 7 |
      | 8 |
      | 9 |
      | 10 |
      | 11 |
      | 12 |
      | 13 |
      | 14 |
      | 15 |
      | 16 |
      | 17 |
      | 18 |
      | 19 |
      | 20 |
      | 21 |
      | 22 |
      | 23 |
      | 24 |
      | 25 |
      | 26 |
      | 27 |
      | 28 |
      | 29 |
      | Large |
