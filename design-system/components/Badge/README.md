# Badge

One or two words of state beside a name, or a count.

- `k-badge` outlined grey for neutral state, `k-badge-accent` filled with the accent for the one thing that wants attention, `k-badge-error` with a symbol for a fault, `k-badge-count` for numbers.
- A badge is words, not a colour code: never rely on its colour alone.
- `k-dot` is the 6px dot in the accent for "live" (recording); `k-dot-live` lets it breathe.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Badge`, `Dot`.

```qml
Badge { text: "3"; kind: "count" }
Dot { live: true }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
