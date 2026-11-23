# IconButton

A square button that carries one symbol. Always give it an `aria-label`, and a Tooltip when the symbol alone could be misread.

- Size: `control` (30px), like every control; the symbol is `icon` (16px).
- Toggle: set `aria-pressed`; pressed turns the symbol to `accent-text`. Swap the symbol too (play and pause).
- `k-iconbtn-danger` is reserved for power.

## In Quickshell (Linux shell and apps)

`import Strix`, then `IconButton`, `ToolTip`.

```qml
IconButton {
    id: off
    iconName: "power"
    danger: true
    ToolTip { text: "Shut down"; visible: off.hovered }
}
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
