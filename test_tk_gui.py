import os
os.environ.setdefault("DISPLAY", ":99")

from gui_tk import SudokuGame


def _full_board():
    return [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


def test_default_solve():
    game = SudokuGame()
    assert game.solve_puzzle() is True
    assert game.solved is True
    assert game._is_valid_solution(game.board)


def test_reset():
    game = SudokuGame()
    game.solve_puzzle()
    game.reset()
    assert game.solved is False
    assert game.board == game.original


def test_set_cell_clears_solved():
    game = SudokuGame()
    game.solve_puzzle()
    assert game.solved is True
    game.set_cell(0, 2, 9)
    assert game.solved is False


def test_set_cell_ignores_original():
    puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    game = SudokuGame(puzzle)
    game.set_cell(0, 0, 5)
    assert game.board[0][0] == 1


def test_solve_rejects_invalid_full_board():
    invalid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [7, 7, 7, 7, 7, 7, 7, 7, 7],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [9, 9, 9, 9, 9, 9, 9, 9, 9],
    ]
    game = SudokuGame(invalid)
    assert game.solve_puzzle() is False
    assert game.solved is False


def test_solve_after_user_conflict():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    game = SudokuGame(puzzle)
    game.set_cell(0, 2, 5)
    assert game.solve_puzzle() is False
    assert game.solved is False


def test_is_original():
    puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    game = SudokuGame(puzzle)
    assert game.is_original(0, 0) is True
    assert game.is_original(0, 1) is False


def test_enter_digit_ignored_when_solved():
    game = SudokuGame()
    game.solve_puzzle()
    original = [row[:] for row in game.board]
    board_before = [row[:] for row in game.board]
    game.set_cell(0, 2, 9)
    assert game.board == board_before or game.solved is False
    game.solved = True
    board_at_solve = [row[:] for row in game.board]
    game.set_cell(0, 2, 9)
    assert game.board == board_at_solve


def test_enter_digit_clears_solved_flag():
    game = SudokuGame()
    game.solve_puzzle()
    assert game.solved is True
    game.set_cell(0, 2, 9)
    assert game.solved is False


try:
    import tkinter as tk
    from gui_tk import SudokuGUI

    _root = tk.Tk()
    _root.withdraw()
    _HAS_TK = True
    _root.destroy()
except Exception:
    _HAS_TK = False


import pytest


@pytest.mark.skipif(not _HAS_TK, reason="no display for Tk")
def test_gui_entries_are_readonly():
    root = tk.Tk()
    root.withdraw()
    try:
        gui = SudokuGUI(root)
        for r in range(9):
            for c in range(9):
                assert gui.cells[r][c].cget("state") == "readonly"
    finally:
        root.destroy()


@pytest.mark.skipif(not _HAS_TK, reason="no display for Tk")
def test_gui_enter_digit_ignored_after_solve():
    root = tk.Tk()
    root.withdraw()
    try:
        gui = SudokuGUI(root)
        gui.game.solve_puzzle()
        gui.selected = (0, 2)
        saved = [row[:] for row in gui.game.board]
        gui._enter_digit(9)
        assert gui.game.board == saved
        assert gui.game.solved is True
    finally:
        root.destroy()


@pytest.mark.skipif(not _HAS_TK, reason="no display for Tk")
def test_gui_solve_clears_selection():
    root = tk.Tk()
    root.withdraw()
    try:
        gui = SudokuGUI(root)
        gui._on_click(0, 2)
        assert gui.selected == (0, 2)
        gui._solve()
        assert gui.selected is None
        assert gui.game.solved is True
    finally:
        root.destroy()
