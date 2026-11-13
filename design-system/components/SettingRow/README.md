# SettingRow

One setting per row: a bold title, one line that says what it does, and the control at the right.

- Markup: `.k-setting` > `div` (`b` title, `p` description) + one control (Switch, Segmented, Slider or a small Button).
- The description says what changes, in one line. If it needs two, the setting is two settings.
- Rows are separated by a hair line; there are no boxes around them.

## In Quickshell (Linux shell and apps)

`import Strix`, then `SettingRow`.

```qml
SettingRow { title: "Change theme"; text: "Another god every 10 minutes"; Switch { checked: true } }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
