# Sudoku

## What is Sudoku?

Sudoku is a logic-based number puzzle played on a 9x9 grid. The grid is divided into nine 3x3 subgrids (called "boxes" or "regions"). The goal is to fill every empty cell with a digit from 1 to 9 so that:

1. Each **row** contains the digits 1 through 9 exactly once.
2. Each **column** contains the digits 1 through 9 exactly once.
3. Each 3x3 **box** contains the digits 1 through 9 exactly once.

A puzzle begins with some digits already placed (the "givens"). A well-formed Sudoku puzzle has exactly one valid solution.

## How to Play

1. Look at the rows, columns, and boxes that intersect an empty cell.
2. Eliminate digits that already appear in those groups.
3. If only one digit remains possible, write it in.
4. If no cell can be solved immediately, make a logical deduction across the board (e.g., "this digit must go somewhere in this box, so it cannot appear elsewhere in the intersecting row").
5. Repeat until the grid is complete.

## How the Solver Works

This project uses a straightforward **recursive backtracking** algorithm:

1. **Find the next empty cell** (represented by `0`).
2. **Try digits 1-9** in order. For each candidate, check whether it conflicts with the existing digits in the same row, column, or 3x3 box.
3. **Place the digit** and move on to the next empty cell (recurse).
4. **If a dead end is reached** (no valid digit for a cell), undo the last placement (backtrack) and try the next candidate.
5. **If all cells are filled**, a valid solution has been found.

This approach guarantees a solution whenever one exists, though it explores invalid paths before finding the correct one. More advanced solvers use constraint propagation (naked singles, hidden singles, etc.) to reduce the search space before resorting to backtracking.
