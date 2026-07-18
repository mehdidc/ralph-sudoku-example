# Progress

## Iteration 1

- Created `pyproject.toml` with project metadata, `pygame>=2.0` dependency, `pytest` as dev dependency, pytest config, and `sudoku-gui` entry point.
- Removed `requirements.txt`.
- Ran `uv sync --extra dev` — resolved and installed 6 packages.
- Ran `uv run pytest test_sudoku.py test_gui.py -v` — all 16 tests pass.

## Iteration 2

- Created `gui_tk.py` with a tkinter-based Sudoku GUI (`SudokuGame` class + `SudokuGUI` widget class).
- `SudokuGUI` renders a 9×9 grid of Entry widgets, sidebar with Solve/Reset buttons, keyboard support (1-9, 0/Delete/BackSpace, S, R), and color coding for original/user/solved cells.
- Created `test_tk_gui.py` with 7 tests covering solve, reset, set_cell, is_original, invalid-board rejection, and user-conflict scenarios.
- Updated `pyproject.toml`: added `sudoku-tk` entry point, `gui_tk` to py-modules, updated description.
- Ran `python3 -m pytest test_tk_gui.py test_sudoku.py test_gui.py -v` — all 23 tests pass.

## Iteration 3 (review round 1)

- **Finding 1 (Medium):** Entry widgets accepted direct typing/paste that bypassed the game model. Fixed by keeping all Entry widgets in `"readonly"` state and blocking `<<Paste>>`/`<<Clear>>` virtual events; all input now goes through `_enter_digit`.
- **Finding 2 (Medium):** After solving, root key bindings could still modify solved cells via `_enter_digit`. Fixed by guarding `_enter_digit` with `not self.game.solved` and clearing `selected` after solve.
- Added 5 new tests (12 total in `test_tk_gui.py`): model-level `test_enter_digit_ignored_when_solved`, `test_enter_digit_clears_solved_flag`, and GUI-level `test_gui_entries_are_readonly`, `test_gui_enter_digit_ignored_after_solve`, `test_gui_solve_clears_selection`.
- All 28 tests pass.

## Iteration 4 (review round 2)

- **Finding 1 (Medium):** `readonlybackground` was not set alongside `bg` in `_refresh_grid()`. When Entry widgets are in `readonly` state, Tk uses `readonlybackground` for the background, causing platform-specific defaults to override the intended colors (light blue for selected, gray for given cells). Fixed by setting `readonlybackground` to match `bg` on every config call.
- Added `test_gui_readonlybackground_matches_bg` to verify all 81 entries have matching `bg` and `readonlybackground`, and that selected and original cells get the correct values.
- All 29 tests pass.
