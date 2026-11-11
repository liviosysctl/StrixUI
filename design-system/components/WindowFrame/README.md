# WindowFrame

How a window looks. Under Hyprland the compositor draws it: 1px border, 4px corners (`radius-md`), `shadow-window`, 12px (`space-3`) between windows and to the screen edge. The focused window has a quiet border in the accent (`border-active`, the accent quietened toward `border`), all others the grey one and are a touch dimmer. The border eases over `dur-slow`; focus never flashes.

- Tiled windows have no title bar. The border colour fades over `dur-base` when focus moves.
- Apps that run outside Hyprland (the Windows bootstick app) draw `k-titlebar`: serif app name, a muted subtitle, then minimise, maximise, close as 40px wide targets; close fills with the accent on hover.
- Click a window in the preview to move focus.
