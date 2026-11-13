# Radio

One of several, when all options should stay visible and there are more than four, or the labels are long. For two to four short options use Segmented.

- Markup: the Checkbox markup with `type="radio"` and a shared `name`.
- Arrow keys move the choice inside the group.

## In Quickshell (Linux shell and apps)

`import Strix`, then `RadioButton`, `ButtonGroup`.

```qml
ButtonGroup { id: look }
RadioButton { text: "Dark"; checked: true; ButtonGroup.group: look }
RadioButton { text: "Light"; ButtonGroup.group: look }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
