import pytest
from sudoku import solve, is_valid, find_empty


def is_complete(board):
    for row in board:
        if 0 in row:
            return False
    return True


def rows_valid(board):
    for row in board:
        if sorted(row) != list(range(1, 10)):
            return False
    return True


def cols_valid(board):
    for col in range(9):
        vals = [board[row][col] for row in range(9)]
        if sorted(vals) != list(range(1, 10)):
            return False
    return True


def boxes_valid(board):
    for br in range(3):
        for bc in range(3):
            vals = []
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    vals.append(board[r][c])
            if sorted(vals) != list(range(1, 10)):
                return False
    return True


def assert_valid_solution(board):
    assert is_complete(board)
    assert rows_valid(board)
    assert cols_valid(board)
    assert boxes_valid(board)


easy_puzzle = [
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

hard_puzzle = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

already_solved = [
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


def test_solve_easy():
    board = [row[:] for row in easy_puzzle]
    assert solve(board) is True
    assert_valid_solution(board)


def test_solve_hard():
    board = [row[:] for row in hard_puzzle]
    assert solve(board) is True
    assert_valid_solution(board)


def test_already_solved():
    board = [row[:] for row in already_solved]
    assert solve(board) is True
    assert board == already_solved


def test_find_empty_on_full_board():
    assert find_empty(already_solved) is None


def test_find_empty_on_puzzle():
    board = [row[:] for row in easy_puzzle]
    pos = find_empty(board)
    assert pos is not None
    assert board[pos[0]][pos[1]] == 0


def test_is_valid_correct_placement():
    board = [row[:] for row in easy_puzzle]
    assert is_valid(board, 0, 2, 4) is True


def test_is_invalid_placement_row_conflict():
    board = [row[:] for row in easy_puzzle]
    assert is_valid(board, 0, 2, 5) is False


def test_is_invalid_placement_col_conflict():
    board = [row[:] for row in easy_puzzle]
    assert is_valid(board, 0, 2, 6) is False


def test_is_invalid_placement_box_conflict():
    board = [row[:] for row in easy_puzzle]
    assert is_valid(board, 0, 2, 9) is False
