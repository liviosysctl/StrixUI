# ContextMenu

Actions for the thing under the pointer.

- Rows: symbol, verb, the key at the far right. Destructive actions sit last, after a divider, in `error`.
- Opens at the pointer with a quick pop from its top left corner; Escape or a click elsewhere closes it.
- At most eight rows. No sub-menus.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Menu`, `MenuItem`, `MenuSeparator`.

```qml
Menu {
    id: menu
    MenuItem { text: "Copy"; iconName: "copy"; shortcut: "Ctrl C" }
    MenuSeparator {}
    MenuItem { text: "Delete"; iconName: "trash-2"; danger: true }
}
// menu.popup()
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
