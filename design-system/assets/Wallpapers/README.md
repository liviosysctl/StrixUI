# Wallpapers

The pantheon of the default theme: eight Roman gods, each an engraving printed in two inks of the god's aspect, with one disc in the god's colour. Sources: Art Institute of Chicago, open-access collection, released under CC0; Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `tools/wallpapers.py`.

- `carna.jpg` — Carna, accent `#c8102e` on `#0b0a09`. the default desktop. Head of a vestal, engraved by J. F. Cazenave after Augustin Raymond Aubert, 1780 to 1820. Rijksmuseum RP-P-2017-9060, public domain.
- `janus.jpg` — Janus, accent `#2e9a84` on `#060c0a`. the lock screen. Janus opens the door of the year, engraved by Robert van Audenaerd after Carlo Maratta, 1685 to 1723. Rijksmuseum RP-P-OB-67.432, public domain.
- `apollo.jpg` — Apollo, accent `#d4a21a` on `#0c0a06`. Hendrick Goltzius, The Apollo Belvedere, about 1592. Art Institute of Chicago 1990.498, CC0.
- `mars.jpg` — Mars, accent `#e0641f` on `#0e0907`. Hubert Quellinus after Artus Quellinus, Mars in the west gallery of the Amsterdam town hall, 1655. Rijksmuseum RP-P-AO-22-1Q-1, public domain.
- `minerva.jpg` — Minerva, accent `#8f9b2c` on `#0a0b06`. Jan Saenredam after Hendrick Goltzius, Pallas Athena, from Three Goddesses, about 1595. Art Institute of Chicago 2023.161, CC0.
- `mercurius.jpg` — Mercurius, accent `#448bcd` on `#070b0e`. Hendrick Goltzius after Polidoro da Caravaggio, Mercurius, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.975, CC0.
- `pluto.jpg` — Pluto, accent `#7a4fd1` on `#0a090e`. Hendrick Goltzius after Polidoro da Caravaggio, Pluto, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.970, CC0.
- `bacchus.jpg` — Bacchus, accent `#b23472` on `#0e090a`. Hendrick Goltzius after Polidoro da Caravaggio, Bacchus, from Eight Pagan Gods, 1592. Art Institute of Chicago 2023.974, CC0.
- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

No ancient likeness of Carna survives. Her plate is a veiled vestal, chosen for the veil and the watchful face, and its caption says so.

Treatment of a plate: crop to the head and upper body at 16:9; paper becomes `line` at 46%, ink becomes the aspect's `background`; inside the disc the paper becomes the aspect's `accent`; darken toward the edges, hardest along the top 110px and the bottom 90px; add fine grain.

Add further gods only from collections that state public-domain status, give each an aspect in `tools/pantheon.py`, treat it the same way, and list title, engraver, date, source and licence here.
