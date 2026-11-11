# TextField

One line of text. Three shapes share one behaviour: `k-input` (box, the default in apps), `k-input-pill` (search and the greeter), `k-input-line` (the lock screen: only a bottom line).

- Structure: `.k-field` > `label`, `.k-input` > `input`, `.k-help`. The help line keeps its height so the layout does not jump when an error appears.
- Error: `data-state="error"` on the field and `aria-invalid` on the input. The help text says what is wrong and how to fix it.
- Passwords: `type="password"`; dots are spaced. A wrong password adds the class `k-shake` to the `.k-input` once.
- Focus turns the border to `focus` and adds the ring.
