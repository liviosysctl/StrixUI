# Progress

How far something is, as a 2px line. With a known amount the red part grows; without one, a short red piece runs along the line.

- Markup: `<div class="k-progress" style="--p:40%"><i></i></div>`; unknown amount: add `data-indeterminate`.
- Say what is happening in words above the line (`k-progress-row`), with the number at the right.
- The boot splash uses the indeterminate form only.
