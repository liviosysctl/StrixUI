# SearchField

A pill field with the search symbol in front. Used by the app finder, the clipboard history, the store and settings.

- Results update while typing; there is no search button.
- Show the key that closes or clears it as a `k-kbd` hint at the end.
- Give the input an `aria-label`; there is no visible label.

## In Quickshell (Linux shell and apps)

`import Strix`, then `SearchField`.

```qml
SearchField { width: 300; onAccepted: search.call("query", { text: text }) }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
