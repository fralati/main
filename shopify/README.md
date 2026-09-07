# cliCHair Hair Quiz (Shopify, Horizon theme)

Interactive hair quiz for the clichair.ch home page. While the visitor answers,
an SVG avatar (head of hair) and a magnified single strand are rebuilt from the
answers. At the end the quiz generates a prompt, in the visitor's language
(EN, IT, DE, FR), to paste into clichAIr (the Zipchat AI assistant).

File: `snippets/clichair-hair-quiz.liquid` (about 39 KB, under the 50 KB
limit of a single Liquid setting).

## Install

Option A, snippet + Custom Liquid block (recommended):

1. Online Store > Themes > Horizon > Edit code > Snippets > Add a new snippet
   named `clichair-hair-quiz` and paste the content of the file.
2. In the theme editor, in the Custom Liquid block on the home page, enter:

   ```liquid
   {% render 'clichair-hair-quiz' %}
   ```

Option B, paste the whole file directly into the Custom Liquid block.

## Zipchat launcher

The "Open clichAIr" button copies the prompt, then tries to open the Zipchat
widget through common JavaScript globals and launcher selectors. If the widget
does not open automatically, set `ZIPCHAT_SELECTOR` at the top of the script
to the CSS selector of the Zipchat launcher button (inspect it in the browser).
The visitor is always told to paste the prompt into the chat at the bottom
right, so the flow works even without the automatic opening.

## Notes

- Language is taken from `request.locale.iso_code`; unknown locales fall back to English.
- Answers are kept in `localStorage` (key `cq_state_v1`) so a reload keeps progress.
- No external assets: the avatar and the strand are inline SVG generated in JavaScript.
- Colours and fonts use the Horizon CSS variables with fallbacks (Inter, black, Swiss red accent).
