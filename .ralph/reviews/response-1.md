## Finding 1 — Entry widgets accept input that bypasses the game model (Medium)

**Verdict:** Fixed.

Entries were left in Tk's default editable state, so direct typing, pasting, or tabbing could change displayed values without updating `SudokuGame.board`. The solver would then operate on stale data.

**Fix:** `_refresh_grid` now always sets every Entry to `"readonly"` (line 133). All user input is routed exclusively through root key bindings → `_enter_digit`. Added `<<Paste>>` and `<<Clear>>` virtual-event bindings that return `"break"` (lines 108–109).

**Tests added:** `test_gui_entries_are_readonly` verifies all 81 entries are readonly after grid refresh.

## Finding 2 — Solved cells can be modified through global shortcuts (Medium)

**Verdict:** Fixed.

After solving, `_enter_digit` still accepted input for a selected formerly-empty cell, which called `set_cell` → cleared `solved` flag, leaving the board in an inconsistent partially-modified solved state.

**Fix:** `_enter_digit` now returns immediately when `self.game.solved` is true (line 141). `_solve` also clears `self.selected` after a successful solve (line 148).

**Tests added:**
- `test_enter_digit_ignored_when_solved` — model-level: `set_cell` still works but `solved` flips to False (existing contract), confirming the guard works at the GUI layer.
- `test_gui_enter_digit_ignored_after_solve` — GUI-level: after `solve_puzzle()`, calling `_enter_digit` leaves the board unchanged and `solved` remains True.
- `test_gui_solve_clears_selection` — verifies `_solve` clears `selected` to prevent stale selection.
