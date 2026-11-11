# Motion

Everything that can move, moves. Nothing invents its own timing: every transition uses a duration and a curve from the tokens, and every moving thing is listed in the catalogue below. If it is not in the catalogue, it does not move; if it is in the catalogue, it must not appear or change without its motion.

## Tokens

| Duration | Value | For |
|---|---|---|
| `dur-instant` | 80ms | Press feedback, menu hover |
| `dur-fast` | 140ms | Hover, focus, tooltips, border colour |
| `dur-base` | 220ms | Switch, segmented thumb, tabs, dialogs, list rows, window focus |
| `dur-slow` | 360ms | Panel out of the dock, carousel, windows, workspaces, rolling numbers |
| `dur-reveal` | 640ms | Theme reveal, unlock, ring gauges |
| `dur-loop` | 1400ms | One pass of an indeterminate line |
| `stagger` | 30ms | Delay between neighbours entering |

| Curve | Value | For |
|---|---|---|
| `ease-out` | cubic-bezier(0.2, 0.8, 0.2, 1) | Arriving |
| `ease-in` | cubic-bezier(0.5, 0, 0.9, 0.3) | Leaving |
| `ease-in-out` | cubic-bezier(0.65, 0, 0.35, 1) | Travelling from one place to another |
| `ease-spring` | cubic-bezier(0.3, 1.4, 0.5, 1) | A small overshoot on small parts |

## Rules

- Arriving is slower than leaving. Closing uses the same motion in reverse, one duration step faster, with `ease-in`.
- Animate transform and opacity. Width and height change only where the shape itself is the message (workspace pill, theme card, progress).
- Every motion can be interrupted: a new trigger starts from the current position, never from the start.
- Things grow from where they were triggered: a panel from its dock symbol, a menu from the pointer, the theme reveal from the click.
- Lists enter row by row, `stagger` apart, at most eight rows; later rows appear with the eighth.
- Reduced motion: movement and scaling are removed, and what remains is a fade of at most `dur-fast`. Loops stop. The visualizer stands still.

## Catalogue

| Element | Trigger | Property | Duration | Curve | If interrupted |
|---|---|---|---|---|---|
| Button, IconButton | hover, focus | background, border, colour | `dur-fast` | `ease-out` | reverses |
| Button, IconButton | press | scale to 0.985 (0.92 for icons), 1px down | `dur-instant` | `ease-out` | reverses |
| Button | loading | a 28% piece runs along the bottom edge | `dur-loop`, repeating | `ease-in-out` | stops with the state |
| TextField | focus | border colour, ring | `dur-fast` | `ease-out` | reverses |
| TextField | wrong input | shake, 8px, four swings | `dur-slow` | `ease-out` | restarts |
| Switch | toggle | thumb slides 16px, track colour | `dur-base` | `ease-spring`, colour `ease-out` | reverses from position |
| Switch | press | thumb widens to 16px | `dur-fast` | `ease-out` | reverses |
| Checkbox, Radio | toggle | mark scales from 0, box colour | `dur-fast` | `ease-spring` | reverses |
| Segmented | select | thumb glides and resizes; labels stay | `dur-base` | `ease-in-out` | retargets |
| Tabs in a panel | select | old section out, new one slides 16px from the side of travel and fades | `dur-base` | `ease-out` | new section wins |
| Slider | drag, keys | fill follows directly; handle grows 25% while pressed | `dur-fast` | `ease-spring` | follows |
| Progress | value | width | `dur-slow` | `ease-out` | retargets |
| Progress | unknown | an 18% piece runs along the line | `dur-loop`, repeating | `ease-in-out` | stops with the state |
| Ring | value | arc length; digits roll | `dur-reveal` | `ease-out` | retargets |
| Rolling number | value | each digit column slides | `dur-slow` | `ease-in-out` | retargets |
| List row | hover, select | background; the red caret slides in 4px | `dur-fast` | `ease-out` | reverses |
| List row | enter | 6px rise and fade, staggered | `dur-base` + `stagger` | `ease-out` | finishes |
| List row | remove | fade and collapse | `dur-base` | `ease-in` | finishes |
| Card | hover | border colour, 2px lift | `dur-fast` | `ease-out` | reverses |
| Tooltip | hover after `dur-slow`, focus | fade and 4px rise | `dur-fast` | `ease-out` | hides at once |
| ContextMenu | open | pop from its top left corner | `dur-fast` | `ease-out` | closes |
| Dialog | open | scrim fades; dialog rises 8px from 97% | `dur-base` | `ease-out` | closes |
| Dialog | close | reverse | `dur-fast` | `ease-in` | finishes |
| Notification | arrive | slides 32px in from the right, fades | `dur-slow` | `ease-out` | finishes |
| Notification | dismiss, expire | slides out right; the stack closes the gap | `dur-base` | `ease-in`; gap `ease-in-out` | finishes |
| Notification, critical | shown | a line drains over its lifetime | 8s | linear | pauses on hover |
| OSD | key press | line width; number | `dur-fast` | `ease-out` | retargets |
| OSD | show, hide | fade and 8px rise | `dur-base` | `ease-out`, `ease-in` | stays while keys repeat |
| Top bar meter | new value | bar height; digits roll | `dur-slow` | `ease-out` | retargets |
| Workspace dots | switch | active pill moves by changing widths | `dur-base` | `ease-in-out` | retargets |
| Top bar track | new title | old fades out, new fades in | `dur-base` | `ease-out` | new title wins |
| Dock | pointer reaches the bottom edge | rises from `dock-rest` to `dock-height` and widens; content fades in `dur-fast` later | height `dur-base`, width `dur-slow` | `ease-out` | reverses from position |
| Dock | pointer leaves, after 420ms | content fades, then it sinks and narrows | `dur-base`, `dur-slow` | `ease-out` | rises again |
| Dock panel | open | scales up from the symbol that opened it; content fades in `dur-fast` later | `dur-slow` | `ease-out` | reverses from position |
| Dock panel | close | reverse | `dur-base` | `ease-in` | reverses |
| Dock symbol | active | fills red | `dur-fast` | `ease-out` | reverses |
| Search | open (Super Space) | panel drops 8px and fades in; scrim fades | `dur-base` | `ease-out` | closes from position |
| Search | close | reverse | `dur-fast` | `ease-in` | finishes |
| Search | enter a group, go back | the list slides 12px in from the right, going back from the left | `dur-base` | `ease-out` | the newer level wins |
| Cheat sheet | open (Super K) | panel drops 8px and fades in; scrim fades | `dur-base` | `ease-out` | closes from position |
| Cheat sheet | edit a row | the sheet closes, Settings opens at the row; the row is marked in `accent-soft` and fades back | `dur-slow` | `ease-out` | finishes |
| Hotkeys | record keys | the key field turns to the accent and its prompt pulses until keys are pressed | `0.9s` per pulse | `ease-in-out` | Esc cancels |
| Search | typing | results update in place, no motion; the red caret follows the chosen row | none | none | none |
| Carousel | browse | row slides; old middle narrows, new one widens; name rises in | `dur-slow` | `ease-in-out` | retargets |
| Theme card | hover | brightness | `dur-fast` | `ease-out` | reverses |
| Theme | apply | new wallpaper grows as a circle from the click point; then the picker fades | `dur-reveal`, then `dur-base` | `ease-in-out`, `ease-in` | finishes |
| Lock screen | lock | another god's plate and aspect; wallpaper dims and softens; column slides in from the left | `dur-reveal`, `dur-slow` | `ease-out` | finishes |
| Lock screen | unlock | column fades and moves 24px left; wallpaper sharpens | `dur-slow`, `dur-reveal` | `ease-in`, `ease-out` | finishes |
| Lock screen | wrong password | field shakes; message appears | `dur-slow` | `ease-out` | restarts |
| Visualizer | sound | bar heights | `dur-fast` | linear | follows |
| Cursor in a terminal | idle | blink | 1.1s | steps | none |
| Recording dot | recording | breathes between 100% and 35% | `dur-loop` | `ease-in-out` | stops with recording |
| Window | open | pops from 86% and fades in | `dur-slow` | `ease-out` | closes |
| Window | close | shrinks to 86% and fades out | `dur-base` | `ease-in` | finishes |
| Window | move, resize, retile | position and size | `dur-slow` | `ease-in-out` | retargets |
| Window | focus change | border colour, dimming | `dur-base` | `ease-out` | retargets |
| Workspace | switch | windows slide sideways 20% with a fade | `dur-slow` | `ease-in-out` | retargets |
| Special workspace | toggle | slides vertically with a fade | `dur-slow` | `ease-out` | reverses |
| Shell layers | appear, disappear | fade | `dur-fast` | `ease-out` | reverses |
| Boot splash | start, shut down | the red piece runs along the line | `dur-loop`, repeating | `ease-in-out` | none |

## Compositor

The same tokens as a Hyprland configuration. Speeds are in tenths of a second, so 360ms is 3.6.

```lua
hl.curve("ease-out",    { type = "bezier", points = { {0.2, 0.8}, {0.2, 1} } })
hl.curve("ease-in",     { type = "bezier", points = { {0.5, 0}, {0.9, 0.3} } })
hl.curve("ease-in-out", { type = "bezier", points = { {0.65, 0}, {0.35, 1} } })
hl.curve("ease-spring", { type = "bezier", points = { {0.3, 1.4}, {0.5, 1} } })

hl.animation({ leaf = "windowsIn",        enabled = true, speed = 3.6, bezier = "ease-out",    style = "popin 86%" })
hl.animation({ leaf = "windowsOut",       enabled = true, speed = 2.2, bezier = "ease-in",     style = "popin 86%" })
hl.animation({ leaf = "windowsMove",      enabled = true, speed = 3.6, bezier = "ease-in-out" })
hl.animation({ leaf = "fadeIn",           enabled = true, speed = 3.6, bezier = "ease-out" })
hl.animation({ leaf = "fadeOut",          enabled = true, speed = 2.2, bezier = "ease-in" })
hl.animation({ leaf = "fadeSwitch",       enabled = true, speed = 2.2, bezier = "ease-out" })
hl.animation({ leaf = "fadeShadow",       enabled = true, speed = 2.2, bezier = "ease-out" })
hl.animation({ leaf = "fadeDim",          enabled = true, speed = 2.2, bezier = "ease-out" })
hl.animation({ leaf = "border",           enabled = true, speed = 2.2, bezier = "ease-out" })
hl.animation({ leaf = "layersIn",         enabled = true, speed = 1.4, bezier = "ease-out",    style = "fade" })
hl.animation({ leaf = "layersOut",        enabled = true, speed = 1.4, bezier = "ease-in",     style = "fade" })
hl.animation({ leaf = "fadeLayersIn",     enabled = true, speed = 1.4, bezier = "ease-out" })
hl.animation({ leaf = "fadeLayersOut",    enabled = true, speed = 1.4, bezier = "ease-in" })
hl.animation({ leaf = "fadePopupsIn",     enabled = true, speed = 1.4, bezier = "ease-out" })
hl.animation({ leaf = "fadePopupsOut",    enabled = true, speed = 1.4, bezier = "ease-in" })
hl.animation({ leaf = "workspaces",       enabled = true, speed = 3.6, bezier = "ease-in-out", style = "slidefade 20%" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 3.6, bezier = "ease-out",    style = "slidefadevert 20%" })
```

Shell layers only fade at the compositor level, because the shell animates its own surfaces (a panel growing out of the dock is drawn by the shell, not by Hyprland). Window geometry to match: border 1px, rounding 4, gaps in 6 and out 12, active border `accent`, inactive border `border`, shadow range 22 with the colour of `shadow-window`, inactive opacity `dim-inactive`.
