# Pantheon

The pantheon (Style › Wallpaper, Super Ctrl Space). The default theme has no single wallpaper but eight Roman gods. Each god is a plate and an aspect: the plate is the wallpaper, the aspect recolours the system to match it. Calling a god sets both at once.

- The gods, in order: Saturnus (Strix red, the default), Janus (patina), Apollo (antique gold), Mars (rust), Vulcanus (olive), Neptunus (slate blue), Pluto (heather), Bacchus (claret). All but Saturnus are muted, as in dark academia: deep, warm, never bright. Janus keeps the doors; in Ovid it is his gift that keeps the striges out of the house. The lock screen shows another god at every lock.
- An aspect changes only the accent and its family (`accent`, `accent-hover`, `accent-pressed`, `accent-soft`, `accent-text`, `on-accent`, `focus`, terminal cursor and selection) and tints the grounds (`background`, the surfaces, `border`) a little toward the god's hue. Text, `line`, the status colours and syntax stay the same in every aspect, so readability never depends on the god.
- In code the aspect is a theme: `data-theme="mars"` on the root, or on any element to scope it. Light accents (Janus, Apollo and Vulcanus) put dark text on their fills, the others white; `on-accent` says which.
- Every plate is an engraving printed in two inks of its aspect: dark ink on dim cream, and inside the disc the paper takes the god's colour.
- Browse with the arrow keys, the wheel or a click on a neighbour; the small dot under the name is the god's colour. Enter or a click on the middle card spreads the plate as a growing circle from the click point over `dur-reveal`; then the aspect switches and the picker fades.
- Other themes bring their own wallpapers and keep one accent.
