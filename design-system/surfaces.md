# Surfaces

How each surface takes the system. Component names, states and measurements stay the same everywhere; only the technology differs.

| Surface | Technology | Takes |
|---|---|---|
| Desktop shell | Quickshell (QML) | All colour tokens at runtime from the theme engine; type, spacing, radius, line, size, duration and easing tokens; every component under the same name |
| Windows bootstick app | Tauri, HTML | `tokens.css`, `bundle.css`, `bundle.js` as they are; WindowFrame's title bar |
| Store | either of the two | The same components: SearchField, List, Card, Button, Progress, Badge |
| Compositor | Hyprland | Window geometry and the animation block in the Motion section |
| Terminal | Ghostty | `term-` colours, `mono` at 13px with 20px line height, a block cursor in `term-cursor`, the god's plate as `background-image` at `background-image-opacity = 0.06`, the prompt `›` in the accent |
| Boot splash | Plymouth | `background`, `text`, `text-muted`, `line`, `accent`, `error`; the wordmark in `display`; the lozenge rule; the running line |
| Text installer | console | `term-` colours with colour 0 as `background` and colour 7 as `term-foreground`; the accent for the current step and the logo, white only for what the person types |

## Sizes on a 2560 by 1440 screen at scale 1

The Screens previews are drawn on a 1280 by 720 board, which is that screen at half size. Measurements of components do not double: a button is 28px high on the real screen, the bar 26px, the dock 28px once it is out. What grows with the screen is the room between things: the lock screen column sits 128px from the left edge, and the stacked clock is set at twice the `clock` style.

## Console

The installer runs in the Linux console in Terminus (ter-v16n). Neither the serif nor the blackletter is available there: the wordmark is drawn as block characters with a one-cell shadow, and titles are bold mono.
