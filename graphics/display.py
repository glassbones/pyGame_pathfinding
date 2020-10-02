import pygame
from graphics.constants import RGB, WIN

class Canvas:
    def __init__(self, win):
        self.win = win
        self.width = 0

    def draw_grid(self, grid):
        for i in range(grid.row_num):
            pygame.draw.line(self.win, RGB.BLACK, (0, i * grid.gap), (self.width, i * grid.gap))
            for j in range(grid.row_num):
                pygame.draw.line(self.win, RGB.BLACK, (j * grid.gap, 0), (j * grid.gap, self.width))

    def draw(self, grid):
        # paint over everything
        self.win.fill(RGB.BLACK)
        # draw each cell in grid
        for row in grid.cells:
            for cell in row:
                cell.draw(self.win)
        # draw grid lines
        self.draw_grid(grid)
        # render whats drawn
        pygame.display.update()

    def get_clicked_pos(self, grid, pos):
        y, x = pos
        row = y // grid.gap
        col = x // grid.gap
        return row, col

    def draw_circuit(self, grid, forks, branches):
        for cell in forks: cell.color = RGB.DARKER_GREY
        for cell in branches:
            self.draw(grid)
            cell.color = RGB.DARKEST_GREY
            cell.set_is_branch()

canvas = Canvas(WIN)