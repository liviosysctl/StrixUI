# Visualizer

Bars that follow the sound. Grey at rest, the accent at the peaks.

- Markup: `<div class="k-viz" data-bars="56"></div>`. Feed it with `el._k.frame(levels)` (values 0 to 1); without a source it idles on a soft signal.
- Bars above 0.72 switch to `accent` (`chart-1`); the rest are `text-muted`.
- With reduced motion it stands still.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Visualizer`.

```qml
Visualizer { values: cava.bars }  // numbers from 0 to 1, from a cava Process
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
