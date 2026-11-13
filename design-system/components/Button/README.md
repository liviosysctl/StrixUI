# Button

The one way to trigger an action. `k-btn-primary` (filled with the accent) appears at most once per view, for the thing the view is for. Plain `k-btn` is the secondary action, `k-btn-quiet` is for cancel and dismiss, `k-btn-danger` for actions that destroy data.

- Markup: `<button class="k-btn k-btn-primary"><span>Install</span></button>`. Put the label in a `span` so long text truncates.
- Labels: sentence case, a verb first. "Install", "Check", "Erase disk".
- Loading: set `data-loading`; a short piece runs along the bottom edge. Keep the label, change its wording ("Checking").
- Disabled: the `disabled` attribute. Never hide a button that will come back.
- Do not put two primary buttons side by side, and do not use the accent for anything that is not the main action.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Button`.

```qml
Button { text: "Install"; variant: "primary"; onClicked: backend.call("install") }
Button { text: "Checking"; loading: true }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
