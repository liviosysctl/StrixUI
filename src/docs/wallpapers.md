# Wallpapers

The plates of the eight god themes: Roman gods, each an engraving in neutral ink and paper with one ring in the god's colour on his head. Every god has two plates: `<god>.jpg` for the dark variant and `<god>-light.jpg` for the light one. Seven are one series, the Gods in Niches engraved by Jacob Binck after Giovanni Jacopo Caraglio and Rosso Fiorentino; Janus is not part of that series and keeps his own sheet. Sources: Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `cargo strixui wallpapers` from the scan at its full resolution.

{{PLATES}}
- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

Treatment of a plate: crop at 16:9 so the sheet fills the screen and its edge never shows; ink is near black and paper a neutral grey, so the only colour is the theme's. Dark: the plate is almost black, with a neutral glow around a fine ring in the `accent` on the head. Light: the plate is lit from the middle and falls off to black at the edges, and the paper inside the ring takes the `accent`. No grain, no second crop pasted in: the ring is a lens over the one picture.

Add further gods only from collections that state public-domain status, give each a theme in `src/design/gods.json` and a plate in `src/design/plates.json`, treat it the same way, and list title, engraver, date, source and licence here.
