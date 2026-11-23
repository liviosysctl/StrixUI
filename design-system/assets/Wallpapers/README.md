# Wallpapers

The plates of the eight god themes: Roman gods, each an engraving in neutral ink and paper with one ring in the god's colour on his head. Every god has two plates: `<god>.jpg` for the dark variant and `<god>-light.jpg` for the light one. Seven are one series, the Gods in Niches engraved by Jacob Binck after Giovanni Jacopo Caraglio and Rosso Fiorentino; Janus is not part of that series and keeps his own sheet. Sources: Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `cargo strixui wallpapers` from the scan at its full resolution.

- `saturnus.jpg` — Saturnus: accent `#c8102e` on `#080707`. The default desktop. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Saturnus, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178A, public domain.
- `janus.jpg` — Janus: accent `#678d7e` on `#040807`. Janus opens the door of the year, engraved by Robert van Audenaerd after Carlo Maratta, 1685 to 1723. Rijksmuseum RP-P-OB-67.432, public domain.
- `apollo.jpg` — Apollo: accent `#b5925a` on `#090704`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Apollo, from the Gods in Niches, 1510 to 1569. Rijksmuseum RP-P-H-H-91, public domain.
- `mars.jpg` — Mars: accent `#9f5836` on `#0b0605`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Mars, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178I, public domain.
- `vulcanus.jpg` — Vulcanus: accent `#85895b` on `#070804`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Vulcanus, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178S, public domain.
- `neptunus.jpg` — Neptunus: accent `#546d85` on `#05080b`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Neptunus, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178E, public domain.
- `pluto.jpg` — Pluto: accent `#746388` on `#08060a`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Pluto, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178G, public domain.
- `bacchus.jpg` — Bacchus: accent `#93535e` on `#0b0607`. Jacob Binck after Giovanni Jacopo Caraglio after Rosso Fiorentino, Bacchus, from the Gods in Niches, 1530. Rijksmuseum RP-P-1951-178Q, public domain.
- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

Treatment of a plate: crop at 16:9 so the sheet fills the screen and its edge never shows; ink is near black and paper a neutral grey, so the only colour is the theme's. Dark: the plate is almost black, with a neutral glow around a fine ring in the `accent` on the head. Light: the plate is lit from the middle and falls off to black at the edges, and the paper inside the ring takes the `accent`. No grain, no second crop pasted in: the ring is a lens over the one picture.

Add further gods only from collections that state public-domain status, give each a theme in `src/design/gods.json` and a plate in `src/design/plates.json`, treat it the same way, and list title, engraver, date, source and licence here.
