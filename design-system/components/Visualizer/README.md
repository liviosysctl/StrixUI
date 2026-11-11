# Visualizer

Bars that follow the sound. Grey at rest, red at the peaks.

- Markup: `<div class="k-viz" data-bars="56"></div>`. Feed it with `el._k.frame(levels)` (values 0 to 1); without a source it idles on a soft signal.
- Bars above 0.72 switch to `accent` (`chart-1`); the rest are `text-muted`.
- With reduced motion it stands still.
