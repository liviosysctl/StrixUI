# BootSplash

The boot splash (Plymouth): the blackletter wordmark on plain `background`, a lozenge rule, the motto, and one hair line.

- Start and shut down: no percentage. A short piece in the accent runs along the line (Progress, indeterminate).
- Disk passphrase: the line becomes the line field; typed characters show as dots.
- Wrong passphrase: the field shakes once and the text under it reads "Wrong passphrase. Try again." in `error`.
- Colours used: `background`, `text`, `text-muted`, `line`, `accent`, `error`. Nothing else, so the splash can be built per variant from six values.
- Switch the states with the control under the preview.

## In Quickshell

Not Quickshell: Plymouth, rendered by the theme engine from the theme; see surfaces.md.
