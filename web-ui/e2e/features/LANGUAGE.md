# Feature language rules

These feature files describe the behavior of an abstract **M7 editor** — not
of a web page. The same specs are meant to verify any future target (VST
plugin, Max4Live patch, …) by re-implementing the two driver interfaces in
`../drivers/editorDriver.ts` and `../drivers/midiDriver.ts`. Keep them
portable by following these rules.

## Vocabulary

| Say                                    | Never say                          |
| -------------------------------------- | ---------------------------------- |
| the editor / the editor is started      | the page, the app loads, the browser |
| the Program / System **view**           | tab, screen, panel                 |
| the user **sets** "predelay" to "20 ms" | drags, clicks, types, scrolls      |
| "predelay" **shows** "20 ms"            | the element/readout displays       |
| **between sessions** / restarted        | localStorage, reload, refresh      |
| **exports/imports a file**              | downloads, uploads                 |
| **the device**                          | the MIDI port, Web MIDI, the fake  |
| a **program dump** / **system dump**    | SysEx frame details, byte offsets  |
| factory program "Large Hall" from bank "Halls v1" | list indices, slots      |

Values are always the human-readable form the editor shows: `"20 ms"`,
`"-12 dB"`, `"Mono L"`, `"2.5 s"`, `"1/4"` (note division in tempo mode).

## Tags

- `@core` — must hold on **every** target. Steps may only use the
  `EditorDriver` and `MidiDriver` interfaces.
- `@target-specific` — behavior specific to the current implementation:
  pointer/keyboard gestures, the help dialog, the debug drawer, rendering
  modes, and the missing-assets error page. Other targets skip these
  (`npx bddgen --tags "@core"` on a different harness) or replace them with
  their own target-specific features.

## Generated value tables

`parameter-values/` holds one generated feature per parameter, exhaustively
listing every value the editor may offer (`npm run gen:value-features`
rebuilds them from the runtime spec). Edit the generator, not the files.

## Writing new steps

- Portable step definitions live in `../steps/` and receive the `editor` and
  `midi` fixtures. They must never touch Playwright's `page`.
- Target-specific step definitions may use the concrete `webEditor` /
  `webMidi` fixtures (and through them the page). Keep them in
  `web-*.steps.ts` files and use them only from `@target-specific` features.
- Interaction mechanics (how a value gets set) belong in drivers, not in
  Gherkin. If a scenario needs to mention a gesture, it is `@target-specific`.
