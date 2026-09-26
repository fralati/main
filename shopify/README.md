# cliCHair Hair Quiz (Shopify, Horizon theme)

Hair quiz for the clichair.ch home page. The visitor answers 7 questions and
the quiz builds a request, in the visitor's language (EN, IT, DE, FR), that
is copied and pasted into clichAIr (the Zipchat AI assistant). The quiz never
names products: clichAIr analyses the INCI and picks the routine.

## Files

- `snippets/clichair-hair-quiz.liquid`: the paste-ready block (about 34 KB,
  one single Custom Liquid block). This is the only file to paste.
- `src/clichair-hair-quiz.src.liquid`: readable source of the same block.
- `src/build.js`: minifies the source into the paste-ready file
  (`npm install terser csso`, then
  `node src/build.js src/clichair-hair-quiz.src.liquid snippets/clichair-hair-quiz.liquid`).

## Install

Paste the whole paste-ready file into the "Liquid Quiz" Custom Liquid block
on the home page (theme editor > Custom Liquid > Liquid code) and save.
The block content is stored in the template settings, so it survives theme
version updates. Do not add it as a snippet: code files are not carried
over when the theme is updated.

The Shopify editor rejected a 43 KB version while a 34.9 KB version was
accepted, so keep the paste-ready file under about 34 KB.

## Notes

- Language comes from `request.locale.iso_code`; unknown locales fall back to English.
- Answers are kept in `localStorage` (key `cq_state_v3`), so a reload keeps progress.
- "Copy and open clichAIr" copies the request and clicks the Zipchat launcher
  (`[data-zipchat="bubble-icon"],#bubble-icon`). The chat input is in a
  cross-origin iframe, so the visitor pastes and sends the request.
- Colours and fonts use the Horizon CSS variables, so the block follows the
  section colour scheme.
