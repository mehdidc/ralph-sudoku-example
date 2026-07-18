# Progress

## Iteration 1

- Created `pyproject.toml` with project metadata, `pygame>=2.0` dependency, `pytest` as dev dependency, pytest config, and `sudoku-gui` entry point.
- Removed `requirements.txt`.
- Ran `uv sync --extra dev` — resolved and installed 6 packages.
- Ran `uv run pytest test_sudoku.py test_gui.py -v` — all 16 tests pass.
