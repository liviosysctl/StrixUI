# Switch

On or off, applied at once. Use it for settings that take effect immediately; use Checkbox inside forms that are confirmed with a button.

- Markup: `<label class="k-switch"><input type="checkbox"><span></span>Label</label>`.
- The thumb slides with `ease-spring` and stretches slightly while pressed. On is the accent.
- Space toggles it; the ring sits on the track.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Switch`.

```qml
Switch { text: "Keep this theme"; checked: theme.kept; onToggled: theme.call("keep", { kept: checked }) }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
