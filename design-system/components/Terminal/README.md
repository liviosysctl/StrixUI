# Terminal

Ghostty in the Strix theme, tiled on the desktop under the bar: `strix-info`, `git log`, a compiler error and a warning, and `ls`.

- Colours: the 16 `term-` colours are muted like the rest of the system, brick, olive, brass, slate, heather, patina and old paper, each 4.5:1 or more on the ground of every god. The ground (`term-background`), the cursor and the selection follow the god's aspect; the cursor is a block in the accent.
- The plate of the god on the desktop lies in the ground of the terminal at 6%, desaturated and anchored bottom right (Ghostty `background-image` with `background-image-opacity`), so the terminal belongs to the desktop without losing contrast.
- Prompt: path, branch, and a single `›` in the accent. One line, no symbols that need a patched font, no colour blocks.
- `strix-info` prints the facts as `label :: value` between the same double corner marks as InfoBlock, with the 16 colours as a strip. The motto and the wordmark stay out of the terminal.
- Errors are `term-bright-red` and bold, warnings `term-bright-yellow`; that is the loudest the terminal gets. Font `mono` at 13px with 20px line height; padding 16px by 20px; no title bar under Hyprland.
