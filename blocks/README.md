# cliCHair theme blocks (Shopify Horizon)

Source of truth for custom theme blocks used on clichair.ch. Files here are
copied into the theme's `blocks/` folder. They are new files that the stock
Horizon theme does not ship, so a theme update keeps them; the block
placements live in the JSON templates, which the updater migrates.

| File | Purpose |
| --- | --- |
| `ai_gen_block_8ec6b6a.liquid` | Smart breadcrumb (path Home / Brand / Line / Product, context crumb, function chip, sibling popovers, shade switcher, sticky bar, JSON-LD). |

## Taxonomy (metafield `custom.breadcrumb_parent` on collections)

The path is built from a collection metafield, so it works in every
language (translated titles drop the brand prefix, so titles cannot be
trusted). Every collection carries `custom.breadcrumb_parent`:

| Value | Meaning |
| --- | --- |
| `root` | brand collection (Code Zero, Edelstein, Nika) |
| `<handle>` | parent collection, e.g. `edelstein`, `xflex`, `bio-collection` |
| `clichair` | functional collection, feeds the "For" chip (Care, Colouring, Hair Gel, Men) |
| `hidden` | marketing showcase, never part of the path (Trending, Outlet, Sale, BFCM, Marketing) |

A new collection without the metafield falls back to English title
prefixes ("Edelstein Xflex Gel" is read as a child of Edelstein), which
only works on English pages. Set the metafield in the collection admin
page to make it language independent.

## Re-upload after a theme update

Only needed if the updated copy is missing the file (check `blocks/` in the
code editor):

```
shopify theme push --theme <THEME_ID> --only blocks/ai_gen_block_8ec6b6a.liquid
```

or paste the file content into a new file with the same name in the theme
code editor. The block keeps working with the settings already saved in the
templates.
