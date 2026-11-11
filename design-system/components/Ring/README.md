# Ring

A share of a whole at a glance: load, memory, battery. Three side by side in the System panel.

- Markup: `<div class="k-ring" data-value="38"></div>`; update with `Kit.ring(el, value)`.
- The arc fills over `dur-reveal`; the number rolls digit by digit.
- Always put the name under it. The ring alone says nothing.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Ring`.

```qml
Ring { value: 0.24; label: "RAM" }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
