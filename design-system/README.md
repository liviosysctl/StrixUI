Strix is a NixOS-based system with its own desktop. Its default look is a dark study: near-black surfaces, old engravings of Roman gods as the ground, one accent colour that belongs to the god on the wallpaper, type from an old printing house beside a quiet monospace. It should feel like a terminal kept in a library. Everything is small, thin and exact; nothing is chunky.

This system is the single source for that look on every surface: the desktop shell (bar, dock, lock screen, greeter, theme picker, search, notifications), the Linux apps (settings, the store, the graphical installer), the terminal, the boot splash and the text installer. Every own program has its back end in Rust and its front end in Quickshell (QML). The HTML bundle exists for the bootstick app of the M245 proof of concept (Tauri), the one program outside Linux. Surfaces lists what each one takes.

## Principles

- Old and exact. The mood comes from engravings, blackletter, an old-style serif and small ornaments. The work is done in a fine monospace. Never mix the roles: nothing you operate is set in the serif, and nothing that sets the mood is set in mono.
- One accent. `accent` marks the single most important thing in a view: the main action, the selected segment, the active workspace, running progress, the cursor, and the disc on the wallpaper; the focused window shows it only quietened, as `border-active`. Its colour belongs to the god of the moment (Strix red under Saturnus, the default), but there is only ever one. If two things carry it, one of them is wrong.
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
- Lines: `border` for decorative lines and inactive windows, `border-active` for the focused window (the accent quietened, never the full accent), `border-strong` for anything that carries meaning (control outlines), `line` for the cream line work of the wallpaper, bracket frames and the edge of the chosen theme card.
- Status is always a word or a symbol first. `error`, `warning`, `success` and `info` are muted and are used as text or a 1px border, never as a filled area.
- Focus is `focus-ring` on every control: a 2px gap in `background`, then 2px of `focus`. Never the browser's blue.
- Code uses the `syntax-` tokens; charts use `chart-1` to `chart-5` in order, and `chart-1` is the series that matters.
- The terminal uses the `term-` tokens. They are quieter than usual on purpose, so the cursor in the accent and a red error stay the loudest things in a window.

### The theme engine

The ten required colours of `theme.toml` have the same names here: `background`, `surface`, `border`, `text`, `text-muted`, `accent`, `on-accent`, `focus`, `error`, `warning`. Every other colour token is an extra colour under the same name. `term-background`, `term-foreground`, `term-cursor`, `term-selection` and the sixteen `term-` colours map to the keys of the `terminal` table without the prefix. All contrast rules of the engine hold: text 4.5:1 on background and surface, focus 3:1, terminal text 4.5:1.

### Themes: one per god

Strix has a theme for each of eight Roman gods; Saturnus is the default. A theme is a plate and a set of colours; choosing it in the theme picker (Super Ctrl Space) sets both. In the tokens the god themes are the colour themes: `saturnus` is the first and the default, and `data-theme="<god>"` on the root (or on any element) switches to another. The theme changes by itself to another god every 10 minutes (`theme-cycle`) unless it is kept in the theme picker.

| God | `accent` | `background` | Colour |
| --- | --- | --- | --- |
| Saturnus | `#c8102e` | `#0b0a09` | Strix red. Saturn, lord of time and of the night hours; the default. |
| Janus | `#688f7f` | `#070c09` | Patina, the green of old bronze doors and keys. |
| Apollo | `#b5925a` | `#0d0a06` | Antique gold, worn brass. |
| Mars | `#9f5836` | `#0e0907` | Rust, iron and burnt sienna. |
| Vulcanus | `#878a5d` | `#0a0b06` | Olive, the patina on old bronze from the forge. |
| Neptunus | `#546d85` | `#070b0e` | Deep water, slate and ink blue. |
| Pluto | `#746388` | `#0b090e` | Heather, faded plum. |
| Bacchus | `#93535e` | `#0e0909` | Claret, old wine. |

- A god theme sets only `background`, `surface`, `surface-raised`, `surface-sunken`, `border`, the accent family (`accent`, `accent-hover`, `accent-pressed`, `accent-soft`, `accent-text`, `on-accent`, `focus`, `border-active`) and `term-background`, `term-cursor`, `term-selection`. Grounds keep the default's lightness and take only a faint tint of the god's hue. Everything else is shared, so text, status and syntax read the same under every god.
- The colours follow dark academia: deep, muted and warm, like leather, brass, ink and old bindings. Every accent but the default's has an OKLCH chroma between 0.05 and 0.11, so none is pure or bright; only the Strix red stays at full strength, as the colour of the brand.
- The accent of each god is chosen by hand; the rest is derived in OKLCH by `tools/themes.py`, which also checks every pair: text 4.5:1 on all grounds, `accent-text` 4.5:1 on grounds and `accent-soft`, `on-accent` 4.5:1 on all three fills, `focus` and the accent fill 3:1.
- Light accents (Janus, Apollo and Vulcanus) carry near-black text; dark ones (Saturnus, Mars, Neptunus, Pluto and Bacchus) carry white. Use `on-accent`, never a fixed white.
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

- Wallpapers are engravings of Roman gods, printed in two inks of the god's theme: dim cream for the paper and the theme's `background` for the ink. Inside one flat disc behind the head the paper takes the god's `accent`, dulled a little as ink on old paper, so the head is drawn in dark lines on the colour. Around the disc sit a few hair lines: two circles, a graduated ring and a meridian. The picture is darkened hard toward the edges so it reads as texture, not as a poster.
- Eight plates are in the Wallpapers asset group, one per god: Saturnus (the default desktop), Janus, Apollo, Mars, Vulcanus, Neptunus, Pluto and Bacchus. The desktop changes to another god theme every 10 minutes (`theme-cycle`) unless the theme is kept in the theme picker; the lock screen shows another god theme at every lock, never the same twice in a row. They come from the open-access collections of the Art Institute of Chicago (CC0) and the Rijksmuseum (public domain). The group's README gives title, engraver, date, source and licence for each.
- Crop to the upper body: head, shoulders, arms. Keep the top 110px and the bottom 90px of a wallpaper dark so the bar and the dock stay readable.
- Under the lock screen and the theme picker the wallpaper is dimmed to `dim-wallpaper` and softened slightly.
- Add further gods only as engravings or etchings in the public domain from a collection that says so, as a theme of their own whose accent is far enough in hue from the others (at most eight god themes), treated the same way, with source and licence written into the README. No photographs, no paintings in colour, no characters, no artwork of other projects.
- `Kit.wallpaper()` still returns the plain star chart drawn with the tokens (cream lines and the disc, no picture). It is the fallback where a picture cannot be shipped: the boot splash and the installer.

## Help and hotkeys

- The interface does not explain itself in sentences. No component carries a line such as "Enter applies, Esc closes" or "drag to move".
- The cheat sheet explains the keys, all in one place: Super K opens it over the desktop, with every hotkey in groups, a filter, and a direct way into Settings › Hotkeys, where every binding can be changed and new ones added.
- A single key chip (`.k-kbd`) may stand next to a control where one key matters and is not obvious: Esc in Search, K for "Keep this theme" in the theme picker. Never more than one or two in a view, and never with a sentence around them.
- In the design system's own previews, a note that only exists to try the preview (a demo password, a faster clock) starts with "Preview only" and sits small and faint in a corner. It is not part of the design.

## Symbols

- Symbols are Lucide (ISC licence), bundled with the system: 24px grid, drawn thin at a 1.25 stroke, round caps, in the current text colour. In QML `Icon { name: "wifi" }` (the `Icons` singleton lists the names), in HTML `<i class="k-icon" data-icon="wifi"></i>` (`Kit.icons` lists them).
- Sizes: 14px in controls and lists, 12px in the top bar, the dock and small buttons, 10px in badges and title bars.
- A symbol stands alone only where its meaning is certain (power, search, close, Wi-Fi, sound). Otherwise it sits beside a word, or carries a Tooltip.
- No emoji, no coloured symbols, no symbols as decoration.

## Layout of the shell

- The top bar is for reading. It has no surface; small grey text and symbols sit on the engraving. Left: search and the clock, then CPU, memory, temperature. Middle: workspaces and the playing track in serif italic. Right: recording, the bell with its count, power.
- The dock is for doing, and it is part of the bottom edge of the screen. At rest it is a tab `dock-rest` (5px) high with a short line in the accent. When the pointer reaches the bottom edge it rises to `dock-height` (28px) and widens to show settings, the date with the weather, media, Wi-Fi, Bluetooth, sound and about. Each symbol lets its panel grow out of it. It never floats above the edge.
- Search (Super Space) is the one way in to everything else: a single field over the dimmed desktop that finds apps, the actions of the system menu, settings down to a single row, and commands. With an empty field it is the system menu itself. There is no separate app launcher or system menu.
- The clock, the bell and power exist only in the bar. Network, sound and updates exist only in the dock.
- Notifications arrive top right under the bar. The OSD appears bottom centre.
- The lock screen puts everything in one narrow column on the left, the wordmark bottom right, the plate caption bottom centre. The greeter uses the same parts, centred.

## Using the system in code

- Linux, the shell and every app: Quickshell. Add the `qml/` folder of the repository to the import path and `import Strix`. Every component has a QML type of the same purpose (its README says which), every token is a property of the `Theme` singleton in camelCase (`Theme.textMuted`, `Theme.space3`, `Theme.durBase` with `Theme.easeOut` as `easing.bezierCurve`), and `Label { textStyle: "caption" }` sets a type style. One `ThemeFile {}` from `Strix.Shell` keeps `Theme` on the theme the engine applied.
- The bootstick app of the proof of concept: Tauri. Load `tokens.css`, then `components/bundle.css`, then `components/bundle.js`. Components are plain HTML with `k-` classes; `Kit.hydrate(root)` wires behaviour and is safe to call again after adding markup. `Kit.theme()` is the theme on `<html data-theme>`, `Kit.onTheme(fn)` follows it, `Kit.god(id)` gives a god's name, plate caption and wallpaper; a `.k-wall[data-follow]` shows the wallpaper of the theme in use.
- Every back end: Rust, with the crate `strix-design` (`rust/strix-design/` in the repository): the tokens, the eight themes, the theme cycle, the lock screen rotation and the default hotkeys, without dependencies.
- The theme engine of StrixOS takes the themes as `themes/<god>/theme.toml`. Themes from outside the eight gods live in their own repositories (layout 1, see `strix-theme-template`), made with `tools/pack.py` from one accent and one public domain engraving; the QML `Theme` shows them with their own wallpaper.
- Read a component's README before using it. Do not restyle a component from outside and do not add colours, radii, durations or curves that are not tokens.
- Hyprland, Ghostty, the splash and the installer take their values from `tokens.json` or from the theme engine; Surfaces says which.
- To reduce motion, set `Theme.reducedMotion` in QML or `data-motion="reduced"` on the root element in HTML; in HTML the system setting is respected without it.
