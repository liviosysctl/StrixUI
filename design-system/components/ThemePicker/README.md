# ThemePicker

The theme picker (Super Ctrl Space) over the dimmed desktop. Strix has one theme per Roman god, and Saturnus is the default. Each theme is a plate and its colours: the plate is the wallpaper, the colours tint the whole system to match it. Choosing a theme sets both at once.

- The themes, in order: Saturnus (Strix red, the default), Janus (patina), Apollo (antique gold), Mars (rust), Vulcanus (olive), Neptunus (slate blue), Pluto (heather), Bacchus (claret). All gods but Saturnus are muted, as in dark academia: deep, warm, never bright.
- The middle card names the theme in blackletter, with a dot in its accent and its variant under it; the plate caption stands below the carousel. Light is greyed out until the light variant exists.
- A theme changes only the accent and its family (`accent`, `accent-hover`, `accent-pressed`, `accent-soft`, `accent-text`, `on-accent`, `focus`, `border-active`, terminal cursor and selection) and tints the grounds (`background`, the surfaces, `border`) a little toward the god's hue. Text, `line`, the status colours and syntax stay the same in every theme, so readability never depends on the god. In code: `data-theme="mars"` on the root, or on any element to scope it.
- The theme changes by itself every 10 minutes (`theme-cycle`): another god at random, never the same one, spreading from the middle of the screen with the same reveal. A theme chosen by hand starts a new cycle.
- "Keep this theme" stops the change; K turns it on and off while the picker is open. The cycle keeps counting while it is on, and a change that falls due is skipped. Turned off again, nothing happens at once: the next theme comes at the next turn of the running cycle. Under the switch the time to the next theme is shown, or, while kept, the time to the next turn.
- The lock screen keeps its own rule: another god theme at every lock, whatever the desktop shows.
- Browse with the arrow keys, the wheel or a click on a neighbour; Enter or a click on the middle card spreads the plate as a growing circle from the click point over `dur-reveal`, then the colours switch and the picker fades.
