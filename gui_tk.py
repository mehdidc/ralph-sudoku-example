import tkinter as tk
from sudoku import solve

DEFAULT_PUZZLE = [
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


class SudokuGame:
    def __init__(self, puzzle=None):
        self.original = puzzle or [row[:] for row in DEFAULT_PUZZLE]
        self.board = [row[:] for row in self.original]
        self.solved = False

    def reset(self):
        self.board = [row[:] for row in self.original]
        self.solved = False

    def _is_valid_solution(self, board):
        for row in board:
            if sorted(row) != list(range(1, 10)):
                return False
        for col in range(9):
            vals = [board[row][col] for row in range(9)]
            if sorted(vals) != list(range(1, 10)):
                return False
        for br in range(3):
            for bc in range(3):
                vals = [board[br * 3 + r][bc * 3 + c] for r in range(3) for c in range(3)]
                if sorted(vals) != list(range(1, 10)):
                    return False
        return True

    def solve_puzzle(self):
        temp = [row[:] for row in self.board]
        if solve(temp) and self._is_valid_solution(temp):
            self.board = temp
            self.solved = True
            return True
        return False

    def set_cell(self, row, col, num):
        if self.original[row][col] == 0:
            self.board[row][col] = num
            self.solved = False

    def is_original(self, row, col):
        return self.original[row][col] != 0


class SudokuGUI:
    def __init__(self, root, puzzle=None):
        self.root = root
        self.root.title("Sudoku")

        self.game = SudokuGame(puzzle)
        self.cells = [[None] * 9 for _ in range(9)]
        self.selected = None

        grid_frame = tk.Frame(root)
        grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

        for r in range(9):
            for c in range(9):
                entry = tk.Entry(
                    grid_frame,
                    width=2,
                    font=("Arial", 18, "bold"),
                    justify="center",
                    bd=1,
                    relief="solid",
                )
                padx_right = 4 if c % 3 == 2 and c < 8 else 0
                pady_bottom = 4 if r % 3 == 2 and r < 8 else 0
                entry.grid(row=r, column=c, padx=(0, padx_right), pady=(0, pady_bottom))
                entry.bind("<Button-1>", lambda e, row=r, col=c: self._on_click(row, col))
                self.cells[r][c] = entry

        self._refresh_grid()

        btn_frame = tk.Frame(root)
        btn_frame.pack(side=tk.RIGHT, padx=10, pady=10, anchor="n")

        tk.Label(btn_frame, text="Sudoku", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        tk.Button(btn_frame, text="Solve", width=15, command=self._solve).pack(pady=4)
        tk.Button(btn_frame, text="Reset", width=15, command=self._reset).pack(pady=4)

        hint = "Click a cell, then press 1-9.\n0 or Delete to clear.\nS = solve, R = reset."
        tk.Label(btn_frame, text=hint, font=("Arial", 9), fg="gray", justify="left").pack(pady=(10, 0))

        self.root.bind("s", lambda e: self._solve())
        self.root.bind("r", lambda e: self._reset())
        for key in "123456789":
            self.root.bind(key, lambda e, k=key: self._enter_digit(int(k)))
        self.root.bind("0", lambda e: self._enter_digit(0))
        self.root.bind("<Delete>", lambda e: self._enter_digit(0))
        self.root.bind("<BackSpace>", lambda e: self._enter_digit(0))

    def _refresh_grid(self):
        for r in range(9):
            for c in range(9):
                entry = self.cells[r][c]
                val = self.game.board[r][c]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                if val != 0:
                    entry.insert(0, str(val))

                if self.game.is_original(r, c):
                    entry.config(fg="black", bg="#e0e0e0")
                elif self.game.solved:
                    entry.config(fg="cornflower blue", bg="white")
                else:
                    entry.config(fg="dark green", bg="white")

                if self.selected == (r, c):
                    entry.config(bg="light blue")
                elif self.game.is_original(r, c):
                    entry.config(bg="#e0e0e0")

                if self.game.is_original(r, c) or self.game.solved:
                    entry.config(state="readonly")
                else:
                    entry.config(state="normal")

    def _on_click(self, row, col):
        self.selected = (row, col)
        self._refresh_grid()
        self.cells[row][col].focus_set()

    def _enter_digit(self, num):
        if self.selected:
            row, col = self.selected
            self.game.set_cell(row, col, num)
            self._refresh_grid()

    def _solve(self):
        if self.game.solve_puzzle():
            self._refresh_grid()

    def _reset(self):
        self.game.reset()
        self.selected = None
        self._refresh_grid()


def main():
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
