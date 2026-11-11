# Wallpapers

The pantheon of the default theme: eight Roman gods, each an engraving printed in two inks of the god's aspect, with one disc in the god's colour. Sources: Art Institute of Chicago, open-access collection, released under CC0; Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `tools/wallpapers.py`.

- `saturnus.jpg` — Saturnus: accent `#c8102e` on `#0b0a09`. The default desktop. Hendrick Goltzius after Polidoro da Caravaggio, Saturnus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.968, CC0.
- `janus.jpg` — Janus: accent `#688f7f` on `#070c09`. Janus opens the door of the year, engraved by Robert van Audenaerd after Carlo Maratta, 1685 to 1723. Rijksmuseum RP-P-OB-67.432, public domain.
- `apollo.jpg` — Apollo: accent `#b5925a` on `#0d0a06`. Hendrick Goltzius after Polidoro da Caravaggio, Sol, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.972, CC0.
- `mars.jpg` — Mars: accent `#9f5836` on `#0e0907`. Hubert Quellinus after Artus Quellinus, Mars in the west gallery of the Amsterdam town hall, 1655. Rijksmuseum RP-P-AO-22-1Q-1, public domain.
- `vulcanus.jpg` — Vulcanus: accent `#878a5d` on `#0a0b06`. Hendrick Goltzius after Polidoro da Caravaggio, Vulcanus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.971, CC0.
- `neptunus.jpg` — Neptunus: accent `#546d85` on `#070b0e`. Hendrick Goltzius after Polidoro da Caravaggio, Neptunus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.969, CC0.
- `pluto.jpg` — Pluto: accent `#746388` on `#0b090e`. Hendrick Goltzius after Polidoro da Caravaggio, Pluto, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.970, CC0.
- `bacchus.jpg` — Bacchus: accent `#93535e` on `#0e0909`. Hendrick Goltzius after Polidoro da Caravaggio, Bacchus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.974, CC0.
- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

Treatment of a plate: crop to the head and upper body at 16:9; paper becomes `line` at 46%, ink becomes the aspect's `background`; inside the disc the paper becomes the aspect's `accent` at 90% with a little of the cream under it; darken toward the edges, hardest along the top 110px and the bottom 90px; add fine grain.

Add further gods only from collections that state public-domain status, give each an aspect in `tools/pantheon.py`, treat it the same way, and list title, engraver, date, source and licence here.
