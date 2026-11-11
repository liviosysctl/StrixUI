# Progress

How far something is, as a 2px line. With a known amount the part in the accent grows; without one, a short piece in the accent runs along the line.

- Markup: `<div class="k-progress" style="--p:40%"><i></i></div>`; unknown amount: add `data-indeterminate`.
- Say what is happening in words above the line (`k-progress-row`), with the number at the right.
- The boot splash uses the indeterminate form only.

## In Quickshell (Linux shell and apps)

`import Strix`, then `ProgressBar`.

```qml
ProgressBar { value: 0.62; label: "Downloading"; valueText: "62%" }
ProgressBar { indeterminate: true }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
