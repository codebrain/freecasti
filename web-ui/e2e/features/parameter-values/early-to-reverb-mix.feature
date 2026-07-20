# GENERATED FILE — do not edit by hand.
# Regenerate with: npm run gen:value-features (web-ui)
# @slow: walking a whole value table needs more than the default timeout.
@core @parameter-values @slow
Feature: Allowable values for "early to reverb mix"
  The device supports a fixed table of 41 steps for
  "early to reverb mix". The editor must offer exactly these values, in this
  order, and nothing else.

  Scenario: Every value the editor may offer for "early to reverb mix"
    Given the editor is started
    Then the only values available for "early to reverb mix" are:
      | 0% / 100% |
      | 5% / 95% |
      | 9% / 91% |
      | 13% / 87% |
      | 17% / 83% |
      | 20% / 80% |
      | 23% / 77% |
      | 26% / 74% |
      | 29% / 71% |
      | 31% / 69% |
      | 33% / 67% |
      | 35% / 65% |
      | 38% / 63% |
      | 39% / 61% |
      | 41% / 59% |
      | 43% / 57% |
      | 44% / 56% |
      | 46% / 54% |
      | 47% / 53% |
      | 49% / 51% |
      | 50% / 50% |
      | 51% / 49% |
      | 53% / 47% |
      | 54% / 46% |
      | 56% / 44% |
      | 57% / 43% |
      | 59% / 41% |
      | 61% / 39% |
      | 63% / 38% |
      | 65% / 35% |
      | 67% / 33% |
      | 69% / 31% |
      | 71% / 29% |
      | 74% / 26% |
      | 77% / 23% |
      | 80% / 20% |
      | 83% / 17% |
      | 87% / 13% |
      | 91% / 9% |
      | 95% / 5% |
      | 100% / 0% |
