# Search

One field finds everything: apps, the actions of the system menu, settings down to a single row, and commands. It replaces a separate app launcher and system menu. Opens with Super Space, centred near the top over the dimmed desktop; Super Alt Space opens it with the Apps filter set.

- With an empty field it is the system menu: Apps, Style, Capture, Clipboard, Settings, Update, System, Learn, Commands. Enter on a group opens it, the group shows as a crumb in the field, Backspace on an empty field goes back up. Typing searches inside the open group.
- Typing searches every level at once. Each result shows where it lives under its name, in the serif italic: "Style › Theme", "Settings › Lock screen". The same word can appear more than once with different places; the place tells them apart.
- Kinds, named at the right of each row: App, Action, Setting, Command, Menu. Actions show their keybinding, settings show their current value.
- Enter: an app starts, an action runs, a setting opens Settings scrolled to that row with the row marked, a command runs in a terminal. Text that matches nothing runs as a command in a terminal.
- Matching is fuzzy: the letters in order, word starts count most, so "nl" finds Night light and "rs" finds Region screenshot. Titles count more than places and extra words; results far below the best one are left out; frequently used entries rise.
- Tab and Shift Tab cycle the filter (All, Apps, Actions, Settings, Commands). Up and Down move, Esc clears the field, a second Esc closes.
- Rows: 40px, symbol, title in mono with the matched letters in `text` and semibold, the place in `aside` style, kind in `micro`. The chosen row has the raised ground and the red caret, as in List.
- Motion: the panel drops 8px into place over `dur-base`; entering a group slides the list in from the right, going back from the left; results update in place without animation while typing.
- Markup: `.k-search.k-surface` > `.k-search-head` (symbol, `.k-crumb`, `input`, the Esc chip), `.k-search-filter` (a Segmented), `ul.k-hits` > `li.k-hit[data-kind]`, `.k-search-foot` (only the result line, hidden while empty; the keys are on the cheat sheet). `Kit.fuzzy(query, text)` and `Kit.mark(text, hits)` do the matching and the highlighting.
