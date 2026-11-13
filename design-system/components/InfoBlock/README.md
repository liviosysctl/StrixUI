# InfoBlock

Facts as label and value, framed by double-line brackets with open corners. The signature frame of the system.

- Markup: `<dl class="k-info">` with `dt` label, `<i>::</i>`, `dd` value per row; an optional serif `h4` on top.
- Labels are bold, values regular and muted, `::` between them is faint.
- The brackets are `line` at reduced strength. Use the frame for system facts only (system info, About, the installer summary, `strix-info` in the terminal), at most once per view.

## In Quickshell (Linux shell and apps)

`import Strix`, then `InfoBlock`.

```qml
InfoBlock { title: "strix"; model: [["OS", "Strix 0.1"], ["Theme", Theme.about.name + ", dark"]] }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
