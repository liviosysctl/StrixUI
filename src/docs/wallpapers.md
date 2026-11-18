# Wallpapers

The plates of the eight god themes: Roman gods, each an engraving printed in two inks of the theme, with one disc in the god's colour. Sources: Art Institute of Chicago, open-access collection, released under CC0; Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `cargo strixui wallpapers`.

{{PLATES}}
- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

Treatment of a plate: crop to the head and upper body at 16:9; paper becomes `line` at 46%, ink becomes the theme's `background`; inside the disc the paper becomes the theme's `accent` at 90% with a little of the cream under it; darken toward the edges, hardest along the top 110px and the bottom 90px; add fine grain.

Add further gods only from collections that state public-domain status, give each a theme in `src/design/gods.json` and a plate in `src/design/plates.json`, treat it the same way, and list title, engraver, date, source and licence here.
