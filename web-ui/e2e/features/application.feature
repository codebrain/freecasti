@target-specific
Feature: Application shell
  Behavior specific to this editor implementation: asset loading errors,
  the help dialog, the legal footer, and the rendering compatibility mode.

  Scenario: A helpful error is shown when runtime assets are missing
    Given the runtime assets are unavailable
    When the editor is opened anyway
    Then a load error explains how to sync the assets

  Scenario: The help dialog opens and closes with Escape
    Given the editor is started
    When the user opens the help dialog
    Then the help dialog is shown
    When the user presses the "Escape" key
    Then the help dialog is closed

  Scenario: The help dialog closes via its Close button
    Given the editor is started
    When the user opens the help dialog
    And the user clicks the help Close button
    Then the help dialog is closed

  Scenario: The legal disclaimer is always visible in the footer
    Given the editor is started
    Then the footer shows the legal disclaimer

  Scenario: Simple rendering mode is remembered between sessions
    Given the editor is started
    When the user opens the debug panel
    And the user switches rendering to "simple"
    And the editor is restarted
    Then the rendering mode is "simple"
