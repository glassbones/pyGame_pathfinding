import pygame
from logic.grid import Grid
from logic.pathing import Pathing
from graphics.display import canvas
from graphics.constants import RENDER, WIN
from ast import literal_eval

def main(render, canvas, preset, rows = 60):
    win = WIN
    width = render.WIDTH
    canvas.width = width
    grid = Grid(width)
    grid.set_grid(rows, width, preset)
    all_cells = grid.get_all_non_inactive_cells()
    p = Pathing(grid)

    # might want to wait until p.start input for this if menu is implemented
    grid.find_branches()

    run = True
    while run:
        
        canvas.draw(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = canvas.get_clicked_pos(grid, pos)
                cell = grid.cells[row][col]
                if not p.start and cell != p.target:
	                p.start = cell
	                p.start.set_start()

                elif not p.target and cell != p.start:
	                p.target = cell
	                p.target.set_target()

                elif cell != p.target and cell != p.start: cell.set_active()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
	            pos = pygame.mouse.get_pos()
	            row, col = canvas.get_clicked_pos(grid, pos)
	            cell = grid.cells[row][col]
	            cell.set_inactive()
	            if cell == p.start: p.start = None
	            elif cell == p.target: p.target = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and p.start:
                    p.reset_flags()

                    while len(grid.seen) != len(all_cells): p.navigate(grid, canvas)
                
                print(f'step count = {p.counter}')
                print(len(all_cells))
                print(len(grid.seen))

                if event.key == pygame.K_c:
                    p.start = None
                    p.target = None
                    grid.set_grid(rows, width)

    pygame.quit()

# hard coded map import
map_file = "logic/data/maps/main_maze.txt"


main(RENDER, canvas, 1)