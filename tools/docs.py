README = r'''Strix is a NixOS-based system with its own desktop. Its default look is a dark study: near-black surfaces, old engravings of Roman gods as the ground, one accent colour that belongs to the god on the wallpaper, type from an old printing house beside a quiet monospace. It should feel like a terminal kept in a library. Everything is small, thin and exact; nothing is chunky.

This system is the single source for that look on every surface: the desktop shell (bar, dock, lock screen, greeter, theme picker, settings, notifications), the terminal, the boot splash, the text installer, the store and the Windows bootstick app.

## Principles

- Old and exact. The mood comes from engravings, blackletter, an old-style serif and small ornaments. The work is done in a fine monospace. Never mix the roles: nothing you operate is set in the serif, and nothing that sets the mood is set in mono.
- One accent. `accent` marks the single most important thing in a view: the main action, the selected segment, the active workspace, the active window, running progress, the cursor, and the disc on the wallpaper. Its colour belongs to the god of the moment (Strix red under Saturnus, the default), but there is only ever one. If two things carry it, one of them is wrong.
- Fine, not heavy. Text is 12px, controls are 28px high, lines are one pixel, corners are 2 to 4px. When in doubt, make it thinner and leave more room around it.
- Flat and dark. Surfaces are one step lighter than the ground and carry a hair border. No glass, no blur behind panels.
- Lines, not fills. State is shown with a line, a border, a caret or a word before it is shown with a filled box.
- Everything that can move, moves, and every motion uses the tokens in the Motion section.

## Content

- Write all interface text in English, in sentence case: "Shut down", "Lock screen", "You are up to date".
- Be plain and short. Say what happened, then what to do: "Wrong password", "Wrong passphrase. Try again.", "No network. The store needs a connection to load the app list."
- Buttons are verbs: "Install", "Check", "Erase disk". A dialog's button repeats the verb of its title, never "OK".
- Address the person as "you". The system does not say "I" or "we".
- Pair a label with its value using `::` with a space on each side: `Kernel :: 6.18.2`. The label is bold (`label`), the value regular (`value`), the `::` is `text-faint`.
- Numbers carry their unit with a space, in binary units for storage: `7.4 GiB`, `162 GiB of 952 GiB`. Percent has no space: `17%`. Time is 24-hour by default: `21:04`.
- Dates read "Tuesday, 10 November"; short form "Tue 10 Nov".
- Greetings and the motto are lowercase: "good evening, livio", "nocte vigilat".
- Plate captions name the god or the work, then the engraver, the place and the date: "Pluto in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592". Where a likeness is a stand-in, the caption says so.
- Never use emoji, anywhere, including sample text, notifications and terminal output.
- Never set labels in capitals with letter-spacing, never separate items with a middle dot, never draw a coloured box around a statement, never stripe table rows, and never use green, yellow and red together as a status code.
- The system's name appears only where a person reads it. Component and class names are neutral (`k-`, `Kit`), so the name can change in one place.

## Colour

- Ground: `background` for the desktop, splash and installer; `surface` for windows, panels, cards and the dock; `surface-raised` for hover and selected rows; `surface-sunken` for wells (fields, tracks).
- Text: `text` for what must be read, `text-muted` for secondary text and resting symbols, `text-faint` only for placeholders, line numbers, timestamps and the `::` separator.
- The accent as a fill is `accent`, with `on-accent` on top (white on the dark accents, near-black on the light ones). The accent as text or as a symbol is `accent-text`; `accent` itself is not meant to be read as text. Hover and press of a red fill are `accent-hover` and `accent-pressed`.
- Lines: `border` for decorative lines and inactive windows, `border-strong` for anything that carries meaning (control outlines), `line` for the cream line work of the wallpaper, bracket frames and the edge of the chosen theme card.
- Status is always a word or a symbol first. `error`, `warning`, `success` and `info` are muted and are used as text or a 1px border, never as a filled area.
- Focus is `focus-ring` on every control: a 2px gap in `background`, then 2px of `focus`. Never the browser's blue.
- Code uses the `syntax-` tokens; charts use `chart-1` to `chart-5` in order, and `chart-1` is the series that matters.
- The terminal uses the `term-` tokens. They are quieter than usual on purpose, so the cursor in the accent and a red error stay the loudest things in a window.

### The theme engine

The ten required colours of `theme.toml` have the same names here: `background`, `surface`, `border`, `text`, `text-muted`, `accent`, `on-accent`, `focus`, `error`, `warning`. Every other colour token is an extra colour under the same name. `term-background`, `term-foreground`, `term-cursor`, `term-selection` and the sixteen `term-` colours map to the keys of the `terminal` table without the prefix. All contrast rules of the engine hold: text 4.5:1 on background and surface, focus 3:1, terminal text 4.5:1.

### The pantheon: one aspect per god

The default theme has eight aspects, one for each god of its wallpapers. Choosing a god in the pantheon (Style › Wallpaper) sets the plate and its aspect together. In the tokens the aspects are the colour themes: `saturnus` is the first and the default, and `data-theme="<god>"` on the root (or on any element) switches the rest.

__GODS_TABLE__

- An aspect sets only `background`, `surface`, `surface-raised`, `surface-sunken`, `border`, the accent family (`accent`, `accent-hover`, `accent-pressed`, `accent-soft`, `accent-text`, `on-accent`, `focus`) and `term-background`, `term-cursor`, `term-selection`. Grounds keep the default's lightness and take only a faint tint of the god's hue. Everything else is shared, so text, status and syntax read the same under every god.
- The colours follow dark academia: deep, muted and warm, like leather, brass, ink and old bindings. Every accent but the default's has an OKLCH chroma between 0.05 and 0.11, so none is pure or bright; only the Strix red stays at full strength, as the colour of the brand.
- The accent of each god is chosen by hand; the rest is derived in OKLCH by `tools/pantheon.py`, which also checks every pair: text 4.5:1 on all grounds, `accent-text` 4.5:1 on grounds and `accent-soft`, `on-accent` 4.5:1 on all three fills, `focus` and the accent fill 3:1.
- Light accents (__LIGHT__) carry near-black text; dark ones (__DARK__) carry white. Use `on-accent`, never a fixed white.
- `error` stays red under every god. Under Saturnus the error and the accent are both red; that is why status is always a word first.

## Type

- Three families, three jobs. `mono` (JetBrains Mono) is the interface: data, labels, controls, the terminal. `serif` (IM Fell English, cut from the Fell types of the 17th century) is the voice: titles, dates, italic asides, the motto, plate captions. `fraktur` (Grenze Gotisch, a light blackletter that stays readable) is for names only: the wordmark and theme names.
- All three are licensed under the SIL Open Font License and are shipped with every surface, so Linux and Windows render the same.
- Use the styles by name. Blackletter: `display` (wordmark on lock screen and splash), `emblem` (theme names, the name in About). Serif: `title-lg`, `title`, `subtitle`, `aside`, `motto`. Mono: `clock`, `heading`, `body`, `label`, `value`, `caption`, `micro`.
- Blackletter is for one or two words that are a name. Never a sentence, never a label, never below 36px.
- The serif has one weight. Emphasis in the serif is italic; emphasis in mono is weight 600. Do not underline and do not colour text for emphasis.
- Never set the serif below 12px, and never use it for controls, values or list rows.
- The serif has old-style figures only. Set dates and anything with digits in its italic, where the figures read clearly, and keep bare numbers (the clock, values, versions) in mono.
- The wordmark is the name in `display` or as `.k-wordmark`. There is no logo symbol and no monogram; do not draw one.
- The motto "nocte vigilat" sits under the wordmark in `motto`: lowercase, italic, widely spaced. It appears on the lock screen, the greeter, the splash, About and system info, nowhere else.

## Ornament

- `.k-rule` is a hair line with a small open lozenge in the middle, as between the parts of an old title page. Use it once in a view to part the mood from the matter: under the wordmark, between the date and the weather, above the update card.
- `.k-plate` is a plate caption: one line of serif italic naming a picture, in the form "Pluto in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592". Every engraving shown full screen carries one.
- InfoBlock's double-line brackets are the only frame. Use them for system facts, once per view.
- `.k-grain` lays a fine grain over a full-screen picture. Use it on wallpapers only, never on surfaces.
- That is the whole stock of ornament. No flourishes, corner pieces, drop caps or borders made of pattern.

## Space, shape and depth

- Spacing steps are 4, 8, 12, 16, 24, 32, 48 and 64 (`space-1` to `space-8`). Panels and windows pad by `space-3` to `space-4`, dialogs by `space-5` at the sides.
- Windows sit `space-3` apart and `space-3` from the screen edge. Keep the gaps even; the engraving should show between windows.
- Corners are barely rounded: `radius-xs` (1px) for the smallest parts, `radius-sm` (2px) for controls, `radius-md` (4px) for windows, panels and the dock. `radius-pill` is only for the switch, radios, count badges, the search field and the active workspace.
- Every border and track is `line-hair` (1px). Only the filled part of a progress line or ring is `line-bold` (2px).
- Shadows are soft and dark: `shadow-pop` under toolbars and tooltips, `shadow-window` under windows, `shadow-panel` under panels, dialogs and menus. A surface gets a shadow or nothing; never a glow.
- Sizes: controls are `control-md` (28px) and `control-sm` (22px); the top bar is `bar-height` (26px); symbols are 14px, 12px in the bar and the dock.

## Wallpaper and imagery

- Wallpapers are engravings of Roman gods, printed in two inks of the god's aspect: dim cream for the paper and the aspect's `background` for the ink. Inside one flat disc behind the head the paper takes the god's `accent`, dulled a little as ink on old paper, so the head is drawn in dark lines on the colour. Around the disc sit a few hair lines: two circles, a graduated ring and a meridian. The picture is darkened hard toward the edges so it reads as texture, not as a poster.
- Eight plates are in the Wallpapers asset group, one per god: Saturnus (the default desktop), Janus, Apollo, Mars, Vulcanus, Neptunus, Pluto and Bacchus. The desktop shows the god chosen in the pantheon; the lock screen shows another god at every lock, in that god's aspect, never the same twice in a row. They come from the open-access collections of the Art Institute of Chicago (CC0) and the Rijksmuseum (public domain). The group's README gives title, engraver, date, source and licence for each.
- Crop to the upper body: head, shoulders, arms. Keep the top 110px and the bottom 90px of a wallpaper dark so the bar and the dock stay readable.
- Under the lock screen, the theme picker and the pantheon the wallpaper is dimmed to `dim-wallpaper` and softened slightly.
- Add further gods only as engravings or etchings in the public domain from a collection that says so, with an aspect of their own whose accent is far enough in hue from the others, treated the same way, with source and licence written into the README. No photographs, no paintings in colour, no characters, no artwork of other projects.
- `Kit.wallpaper()` still returns the plain star chart drawn with the tokens (cream lines and the disc, no picture). It is the fallback where a picture cannot be shipped: the boot splash and the installer.

## Symbols

- Symbols are Lucide (ISC licence), bundled in the script: 24px grid, drawn thin at a 1.25 stroke, round caps, in the current text colour. Use `<i class="k-icon" data-icon="wifi"></i>`; `Kit.icons` lists the names.
- Sizes: 14px in controls and lists, 12px in the top bar, the dock and small buttons, 10px in badges and title bars.
- A symbol stands alone only where its meaning is certain (power, search, close, Wi-Fi, sound). Otherwise it sits beside a word, or carries a Tooltip.
- No emoji, no coloured symbols, no symbols as decoration.

## Layout of the shell

- The top bar is for reading. It has no surface; small grey text and symbols sit on the engraving. Left: search and the clock, then CPU, memory, temperature. Middle: workspaces and the playing track in serif italic. Right: recording, the bell with its count, power.
- The dock is for doing, and it is part of the bottom edge of the screen. At rest it is a tab `dock-rest` (5px) high with a short red line. When the pointer reaches the bottom edge it rises to `dock-height` (28px) and widens to show settings, the date with the weather, media, Wi-Fi, Bluetooth, sound and about. Each symbol lets its panel grow out of it. It never floats above the edge.
- Search (Super Space) is the one way in to everything else: a single field over the dimmed desktop that finds apps, the actions of the system menu, settings down to a single row, and commands. With an empty field it is the system menu itself. There is no separate app launcher or system menu.
- The clock, the bell and power exist only in the bar. Network, sound and updates exist only in the dock.
- Notifications arrive top right under the bar. The OSD appears bottom centre.
- The lock screen puts everything in one narrow column on the left, the wordmark bottom right, the plate caption bottom centre. The greeter uses the same parts, centred.

## Using the files

- Load `tokens.css`, then `components/bundle.css`, then `components/bundle.js`. Components are plain HTML with `k-` classes; `Kit.hydrate(root)` wires behaviour and is safe to call again after adding markup.
- Read a component's README before using it. Do not restyle a component from outside and do not add colours, radii, durations or curves that are not tokens.
- For a surface that is not HTML (the Quickshell shell, Hyprland, Ghostty, the splash, the installer), take the values from `tokens.json` and keep the component names, states and measurements from here.
- To reduce motion for one view, set `data-motion="reduced"` on the root element; the system setting is respected without it.
'''

MOTION = r'''# Motion

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
'''

SURFACES = r'''# Surfaces

How each surface takes the system. Component names, states and measurements stay the same everywhere; only the technology differs.

| Surface | Technology | Takes |
|---|---|---|
| Desktop shell | Quickshell (QML) | All colour tokens at runtime from the theme engine; type, spacing, radius, line, size, duration and easing tokens; every component under the same name |
| Windows bootstick app | Tauri, HTML | `tokens.css`, `bundle.css`, `bundle.js` as they are; WindowFrame's title bar |
| Store | either of the two | The same components: SearchField, List, Card, Button, Progress, Badge |
| Compositor | Hyprland | Window geometry and the animation block in the Motion section |
| Terminal | Ghostty | `term-` colours, `mono` at 13px with 20px line height, a block cursor in `term-cursor` |
| Boot splash | Plymouth | `background`, `text`, `text-muted`, `line`, `accent`, `error`; the wordmark in `display`; the lozenge rule; the running line |
| Text installer | console | `term-` colours with colour 0 as `background` and colour 7 as `term-foreground`; red for the current step and the logo, white only for what the person types |

## Sizes on a 2560 by 1440 screen at scale 1

The Screens previews are drawn on a 1280 by 720 board, which is that screen at half size. Measurements of components do not double: a button is 28px high on the real screen, the bar 26px, the dock 28px once it is out. What grows with the screen is the room between things: the lock screen column sits 128px from the left edge, and the stacked clock is set at twice the `clock` style.

## Console

The installer runs in the Linux console in Terminus (ter-v16n). Neither the serif nor the blackletter is available there: the wordmark is drawn as block characters with a one-cell shadow, and titles are bold mono.
'''

SECTIONS = {'motion.md': MOTION, 'surfaces.md': SURFACES}

WALL_README = r'''# Wallpapers

The pantheon of the default theme: eight Roman gods, each an engraving printed in two inks of the god's aspect, with one disc in the god's colour. Sources: Art Institute of Chicago, open-access collection, released under CC0; Rijksmuseum, open data, Public Domain Mark. Each file is 2560 by 1440 and made by `tools/wallpapers.py`.

'''

def _plates():
    import pantheon, wallpapers
    role = {'saturnus': ' The default desktop.'}
    rows = []
    for g in pantheon.GODS:
        credit = wallpapers.PLATES[g[0]][3]
        t = pantheon.aspect(g[0])
        rows.append('- `%s.jpg` — %s: accent `%s` on `%s`.%s %s.' % (g[0], g[1], t['accent'], t['background'], role.get(g[0], ''), credit.rstrip('.')))
    return '\n'.join(rows) + '\n'

WALL_README += _plates() + r'''- `star-chart.svg` — the plain fallback without a picture: cream lines and the disc. Own drawing. Colours are fixed in the file; `Kit.wallpaper()` gives the version that follows the tokens.

Treatment of a plate: crop to the head and upper body at 16:9; paper becomes `line` at 46%, ink becomes the aspect's `background`; inside the disc the paper becomes the aspect's `accent` at 90% with a little of the cream under it; darken toward the edges, hardest along the top 110px and the bottom 90px; add fine grain.

Add further gods only from collections that state public-domain status, give each an aspect in `tools/pantheon.py`, treat it the same way, and list title, engraver, date, source and licence here.
'''

COVER = r'''<!-- @dsCard height=288 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Strix</title>
<style>
  html, body { margin: 0; height: 100%; }
  body { background: var(--background); color: var(--text); overflow: hidden; }
  .cover { position: relative; height: 288px; overflow: hidden; }
  .art { position: absolute; top: 0; left: 480px; width: 480px; height: 288px; overflow: hidden; }
  .art svg { display: block; width: 480px; height: 288px; }
  .red { fill: var(--accent); }
  .cream { fill: var(--line); }
  .deep { fill: var(--surface-raised); }
  .soft { fill: var(--accent-soft); }
  .blk { rx: var(--radius-md); }
  .arc { fill: none; stroke: var(--line); stroke-width: var(--line-hair); opacity: 0.6; }
  .words { position: absolute; left: var(--space-6); bottom: var(--space-6); max-width: 440px; }
  .name { margin: 0; font-family: var(--font-fraktur); font-weight: 300; font-size: 120px; line-height: 0.95; color: var(--text); }
  .tag { margin: var(--space-2) 0 0 4px; font-family: var(--font-serif); font-style: italic; font-size: 14px; line-height: 20px; letter-spacing: 0.04em; color: var(--text-muted); }
</style>
</head>
<body>
<div class="cover">
<div class="art" aria-hidden="true">
<svg viewBox="0 0 480 288" width="480" height="288">
<!--
  blocks      accent disc, 176 across (rx = half the side), the one hue the system is known by · line (cream) slab 96×208 bled off the top · surface-raised 168×200 bleeding off the right edge · accent-soft 96×48 once, for relief — about a third of 960×288
  arrangement one disc between two slabs, bottoms on a line space-5 above the edge, space-5 gutters; the disc sits high, as on the wallpaper
  pattern     the literal motif: "a star chart drawn in a few fine line strokes" — three concentric arcs and a meridian in line at line-hair, centred under the disc, crossing the blocks
  scales      sides in space-2 multiples; gutters space-5; arcs space-7 apart; corners radius-md; disc rx 88
-->
<rect class="cream blk" x="24" y="-16" width="96" height="208" rx="4"/>
<rect class="soft blk" x="24" y="216" width="96" height="48" rx="4"/>
<rect class="deep blk" x="336" y="64" width="168" height="200" rx="4"/>
<circle class="red" cx="232" cy="124" r="88"/>
<circle class="arc" cx="232" cy="264" r="96"/>
<circle class="arc" cx="232" cy="264" r="144"/>
<circle class="arc" cx="232" cy="264" r="192"/>
<path class="arc" d="M232 0V288"/>
</svg>
</div>
<div class="words">
<h1 class="name">Strix</h1>
<p class="tag">Old engravings, fine lines, one colour per god.</p>
</div>
</div>
</body>
</html>
'''


def _fill():
    import pantheon
    global README
    rows = ['| God | `accent` | `background` | Colour |', '| --- | --- | --- | --- |']
    for g in pantheon.GODS:
        t = pantheon.aspect(g[0])
        rows.append('| %s | `%s` | `%s` | %s |' % (g[1], t['accent'], t['background'], g[3]))
    light = [g[1] for g in pantheon.GODS if pantheon.aspect(g[0])['on-accent'] != '#ffffff']
    dark = [g[1] for g in pantheon.GODS if pantheon.aspect(g[0])['on-accent'] == '#ffffff']
    both = lambda x: ', '.join(x[:-1]) + ' and ' + x[-1] if len(x) > 1 else x[0]
    README = README.replace('__GODS_TABLE__', '\n'.join(rows)).replace('__LIGHT__', both(light)).replace('__DARK__', both(dark))
_fill()
