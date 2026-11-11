# Terminal

Ghostty with the theme's terminal colours: a prompt, `git log`, a compiler error and a warning, and `ls` with file-type colours. The strip at the bottom is the 16 ANSI colours, normal above bright.

- Ground `term-background`, text `term-foreground`, a red block cursor (`term-cursor`), selection `term-selection`.
- Red is reserved for errors and remote refs; the hash is sand, the branch sage, paths steel. Every colour holds 4.5:1 on the ground, including bright black.
- Prompt: `user@host path branch >` with a single `>`; no symbols that need a patched font.
- The colours are muted on purpose so the red cursor and the red of an error stay the loudest things in the window.
