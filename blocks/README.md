# cliCHair theme blocks (Shopify Horizon)

Source of truth for custom theme blocks used on clichair.ch. Files here are
copied into the theme's `blocks/` folder. They are new files that the stock
Horizon theme does not ship, so a theme update keeps them; the block
placements live in the JSON templates, which the updater migrates.

| File | Purpose |
| --- | --- |
| `ai_gen_block_8ec6b6a.liquid` | Smart breadcrumb (path Home / Brand / Line / Product, context crumb, function chip, sibling popovers, shade switcher, sticky bar, JSON-LD). |

## Re-upload after a theme update

Only needed if the updated copy is missing the file (check `blocks/` in the
code editor):

```
shopify theme push --theme <THEME_ID> --only blocks/ai_gen_block_8ec6b6a.liquid
```

or paste the file content into a new file with the same name in the theme
code editor. The block keeps working with the settings already saved in the
templates.
