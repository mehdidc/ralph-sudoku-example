## Finding 1 — Read-only state suppresses configured cell backgrounds (Medium)

**Verdict:** Fixed.

Tk Entry widgets in `readonly` state use `readonlybackground` instead of `bg` for the displayed background. Without setting `readonlybackground`, platform defaults (e.g., macOS system background) override the intended light-blue selection and gray given-cell shading.

**Fix:** `_refresh_grid()` now sets `readonlybackground` to match `bg` on every `entry.config()` call (lines 122–131 in `gui_tk.py`).

**Test added:** `test_gui_readonlybackground_matches_bg` — verifies all 81 entries have matching `bg` and `readonlybackground` after a click, and checks that the selected cell gets `"light blue"` and original cells get `"#e0e0e0"`.
