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
