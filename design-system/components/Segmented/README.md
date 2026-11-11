# Segmented

Two to four short options, one always chosen. Also the tab switch at the top of a panel.

- Markup: `<div class="k-seg"><button aria-selected="true">Dark</button><button>Light</button></div>`. `Kit.hydrate()` adds the thumb.
- The labels never move: every label has the same weight in both states. Only the thumb in the accent glides (`dur-base`, `ease-in-out`).
- As tabs: `data-for="#id"` points at a `.k-tabs` container; its sections switch with a short slide in the direction of travel.
- Listens to `change` with `detail.index` and `detail.value`. Left and right arrows move the choice.
