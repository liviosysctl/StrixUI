# Slider

A value on a range: volume, brightness, blur, timeouts.

- Markup: `<label class="k-slider"><i class="k-icon" data-icon="volume-2"></i><input type="range"><output></output></label>`.
- A 2px line, in the accent up to the value, with a narrow cream handle. The number at the end follows the handle; `data-unit` adds the unit.
- Arrow keys step by one.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Slider`.

```qml
Slider { iconName: "volume-2"; value: 0.62; onMoved: audio.volume = value }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
