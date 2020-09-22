import pygame
from .constants import RGB

def draw_grid(win, rows, width):
	gap = width // rows
    
	for i in range(rows):
		pygame.draw.line(win, RGB.BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, RGB.BLACK, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    # paint over everything
	win.fill(RGB.BLACK)
    # draw each cell in grid
	for row in grid:
		for cell in row:
			cell.draw(win)
    # draw grid lines
	draw_grid(win, rows, width)
    # render whats drawn
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap

	return row, col

