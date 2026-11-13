# WindowFrame

How a window looks. Under Hyprland the compositor draws it: 1px border, 4px corners (`radius-md`), `shadow-window`, 12px (`space-3`) between windows and to the screen edge. The focused window has a quiet border in the accent (`border-active`, the accent quietened toward `border`), all others the grey one and are a touch dimmer. The border eases over `dur-slow`; focus never flashes.

- Tiled windows have no title bar. The border colour fades over `dur-base` when focus moves.
- Apps that draw their own frame (outside Hyprland, in the previews) use `k-titlebar`: serif app name, a muted subtitle, then minimise, maximise, close as 40px wide targets; close fills with the accent on hover.
- Click a window in the preview to move focus.

## In Quickshell (Linux shell and apps)

`import Strix`, then `WindowFrame`.

```qml
WindowFrame { title: "Store"; subtitle: "Apps from nixpkgs"; active: true; Label { text: "Firefox is installed." } }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
