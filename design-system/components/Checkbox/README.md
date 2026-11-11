# Checkbox

A choice that is confirmed later, with the form's button. Several may be on at once.

- Markup: `<label class="k-check"><input type="checkbox"><span></span>Label</label>`.
- The mark is a small filled square that pops in; the box fills with the accent.

## In Quickshell (Linux shell and apps)

`import Strix`, then `CheckBox`.

```qml
CheckBox { text: "Wi-Fi"; checked: true }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
