# Card

A bordered box for one self-contained thing: an app in the store, a state with its own action.

- Parts: serif title, a short muted text, optional action.
- `data-interactive` makes the whole card a target: the border brightens and it lifts by 2px on hover.
- Cards do not nest, and a list of plain facts is not a card: use List or InfoBlock.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Card`.

```qml
Card { title: "Firefox"; text: "Web browser"; interactive: true; onClicked: ... }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
