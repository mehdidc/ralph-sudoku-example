import copy
import sys
import pygame
from sudoku import solve, is_valid, find_empty

CELL_SIZE = 60
GRID_SIZE = 9 * CELL_SIZE
SIDEBAR_WIDTH = 200
WIDTH = GRID_SIZE + SIDEBAR_WIDTH
HEIGHT = GRID_SIZE
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
BLUE = (100, 149, 237)
GREEN = (144, 238, 144)
RED = (255, 180, 180)

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
        self.selected = None
        self.solved = False

    def reset(self):
        self.board = [row[:] for row in self.original]
        self.solved = False

    def solve_puzzle(self):
        temp = [row[:] for row in self.board]
        if solve(temp):
            self.board = temp
            self.solved = True
            return True
        return False

    def set_cell(self, row, col, num):
        if self.original[row][col] == 0:
            self.board[row][col] = num

    def is_original(self, row, col):
        return self.original[row][col] != 0


def draw_grid(surface, game):
    for row in range(9):
        for col in range(9):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            bg = WHITE
            if game.selected == (row, col):
                bg = LIGHT_BLUE
            elif game.is_original(row, col):
                bg = GRAY
            pygame.draw.rect(surface, bg, rect)

            val = game.board[row][col]
            if val != 0:
                font = pygame.font.SysFont("Arial", 28, bold=True)
                if game.is_original(row, col):
                    color = BLACK
                elif game.solved:
                    color = BLUE
                else:
                    color = (0, 100, 0)
                text = font.render(str(val), True, color)
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(surface, BLACK, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE), width)
        pygame.draw.line(surface, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE), width)


def draw_sidebar(surface, game, buttons):
    sidebar_x = GRID_SIZE
    font = pygame.font.SysFont("Arial", 20)
    title = font.render("Sudoku", True, BLACK)
    surface.blit(title, (sidebar_x + 15, 15))

    small_font = pygame.font.SysFont("Arial", 14)
    hint_lines = [
        "Click a cell to select",
        "Press 1-9 to enter a number",
        "Press 0/Delete to clear",
        "Press S to auto-solve",
        "Press R to reset",
    ]
    for i, line in enumerate(hint_lines):
        text = small_font.render(line, True, DARK_GRAY)
        surface.blit(text, (sidebar_x + 10, 55 + i * 22))

    for btn in buttons:
        btn.draw(surface)


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=5)
        font = pygame.font.SysFont("Arial", 16, bold=True)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()
            return True
        return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    game = SudokuGame()

    buttons = [
        Button(GRID_SIZE + 15, 200, 170, 35, "Solve", game.solve_puzzle),
        Button(GRID_SIZE + 15, 245, 170, 35, "Reset", game.reset),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mx < GRID_SIZE:
                    col = mx // CELL_SIZE
                    row = my // CELL_SIZE
                    if 0 <= row < 9 and 0 <= col < 9:
                        game.selected = (row, col)
                else:
                    for btn in buttons:
                        btn.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if game.selected:
                    row, col = game.selected
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        game.set_cell(row, col, 1)
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        game.set_cell(row, col, 2)
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        game.set_cell(row, col, 3)
                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        game.set_cell(row, col, 4)
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        game.set_cell(row, col, 5)
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        game.set_cell(row, col, 6)
                    elif event.key in (pygame.K_7, pygame.K_KP7):
                        game.set_cell(row, col, 7)
                    elif event.key in (pygame.K_8, pygame.K_KP8):
                        game.set_cell(row, col, 8)
                    elif event.key in (pygame.K_9, pygame.K_KP9):
                        game.set_cell(row, col, 9)
                    elif event.key in (pygame.K_0, pygame.K_DELETE, pygame.K_BACKSPACE):
                        game.set_cell(row, col, 0)

                if event.key == pygame.K_s:
                    game.solve_puzzle()
                elif event.key == pygame.K_r:
                    game.reset()

        screen.fill(WHITE)
        draw_grid(screen, game)
        draw_sidebar(screen, game, buttons)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
