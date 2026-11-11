# Calendar

One month, Monday first, today marked in the accent. Lives in the Today panel.

- Markup: `<div class="k-cal" data-date="2026-11-10"></div>`; without `data-date` it shows the current day.
- The arrows step by month. Days of the neighbouring months are faint.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Calendar`.

```qml
Calendar { onPicked: day => ... }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
