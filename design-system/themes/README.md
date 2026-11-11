# Themes for the theme engine

One folder per god, each with a `theme.toml` in format 1 of the StrixOS theme engine (`themes/README.md` in the strixos repository). Copy the folders into `themes/` there; `saturnus` is the default.

| Id | Name | Colour |
|---|---|---|
| `saturnus` | Saturnus | Strix red. Saturn, lord of time and of the night hours; the default. |
| `janus` | Janus | Patina, the green of old bronze doors and keys. |
| `apollo` | Apollo | Antique gold, worn brass. |
| `mars` | Mars | Rust, iron and burnt sienna. |
| `vulcanus` | Vulcanus | Olive, the patina on old bronze from the forge. |
| `neptunus` | Neptunus | Deep water, slate and ink blue. |
| `pluto` | Pluto | Heather, faded plum. |
| `bacchus` | Bacchus | Claret, old wine. |

- One variant each, `dark`. A light variant follows with the light theme of the design system.
- The ten required colours (`background`, `surface`, `border`, `text`, `text-muted`, `accent`, `on-accent`, `focus`, `error`, `warning`) have the same names in the design system. Every other colour token follows as an extra colour under its own name, so the engine passes all of them on in `/run/strix/theme/tokens.json`, where the QML module reads them.
- `terminal` holds the `term-` colours without the prefix.
- The wallpaper is not part of format 1 yet. Until it is, the shell takes `assets/Wallpapers/<id>.jpg`.
