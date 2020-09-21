import pygame
import math
from queue import PriorityQueue
from ast import literal_eval

WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path finding visualized")

RED = (255, 0, 0)
ORANGE = (255, 165 ,0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
TURQUOISE = (64, 224, 208)
BLUE = (0, 255, 0)
PURPLE = (128, 0, 128)

WHITE = (255, 255, 255)
LIGHT_GREY = (192, 192, 192)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
DARKER_GREY = (16, 16, 16)
BLACK = (0, 0, 0)

map_file = "maps/main_maze.txt"
cell_graph=literal_eval(open(map_file, "r").read())

def load_graph(graph):
    cell_dict = {}
    for cell in graph:
        cell_dict[cell] = graph[cell][0]
    
    scale = 0
    for k, v in cell_dict.items():
        if v[0] > scale:
            scale = v[0]
        if v[1] > scale:
            scale = v[1]

    print(scale)
    return cell_dict
    """
    num_rooms = len(room_graph)
    rooms = [None] * num_rooms
    grid_size = 1
    for i in range(0, num_rooms):
        x = room_graph[i][0][0]
        grid_size = max(grid_size, room_graph[i][0][0], room_graph[i][0][1])
        self.rooms[i] = Room(f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})",i, room_graph[i][0][0], room_graph[i][0][1])
    self.room_grid = []
    grid_size += 1
    self.grid_size = grid_size
    for i in range(0, grid_size):
        self.room_grid.append([None] * grid_size)
    for room_id in room_graph:
        room = self.rooms[room_id]
        self.room_grid[room.x][room.y] = room
        if 'n' in room_graph[room_id][1]:
            self.rooms[room_id].connect_rooms('n', self.rooms[room_graph[room_id][1]['n']])
        if 's' in room_graph[room_id][1]:
            self.rooms[room_id].connect_rooms('s', self.rooms[room_graph[room_id][1]['s']])
        if 'e' in room_graph[room_id][1]:
            self.rooms[room_id].connect_rooms('e', self.rooms[room_graph[room_id][1]['e']])
        if 'w' in room_graph[room_id][1]:
            self.rooms[room_id].connect_rooms('w', self.rooms[room_graph[room_id][1]['w']])
    self.starting_room = self.rooms[0]
    """



class Cell:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = BLACK
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	#def is_closed(self): return self.color == GREY
	#def is_open(self): return self.color == LIGHT_GREY
	def is_barrier(self): return self.color == BLACK
	def is_start(self): return self.color == ORANGE
	def is_target(self): return self.color == TURQUOISE

	def set_none(self): self.color = DARKER_GREY
	def set_barrier(self): self.color = BLACK
	def set_start(self): self.color = ORANGE
	def set_closed(self):
            if self.color[0] <= 240: self.color = (self.color[0]+16, self.color[1], self.color[2])
            if self.color[1] <= 240: self.color = (self.color[0], self.color[1]+16, self.color[2])
            if self.color[2] <= 240: self.color = (self.color[0], self.color[1], self.color[2]+16)
	def set_open(self):
            if self.color[0] <= 240: self.color = (self.color[0]+16, self.color[1], self.color[2])
            if self.color[1] <= 240: self.color = (self.color[0], self.color[1]+16, self.color[2])
            if self.color[2] <= 240: self.color = (self.color[0], self.color[1], self.color[2]+16)
	def set_target(self): self.color = TURQUOISE
	def set_path(self): self.color = PURPLE

	def get_pos(self): return self.row, self.col
	def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.set_path()
		draw()


def algorithm(draw, grid, start, target):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {cell: float("inf") for row in grid for cell in row}
	g_score[start] = 0
	f_score = {cell: float("inf") for row in grid for cell in row}
	f_score[start] = h(start.get_pos(), target.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == target:
			reconstruct_path(came_from, target, draw)
			target.set_target()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), target.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.set_open()

		draw()

		if current != start:
			current.set_closed()

	return False


def set_grid(rows, width, preset=None):
    grid = []
    gap = width // rows
    for i in range(rows):
	    grid.append([])
	    for j in range(rows):
             print(i, j)
             cell = Cell(i, j, gap, rows)
             grid[i].append(cell)

    
    if preset:
        for k, v in preset.items():
            x = v[0][0] * 2 - 1
            y = v[0][1] * 2 - 1
            print(x,y)
            grid[x][y].set_none()
            #if k == 0 : grid[x][y].set_start()
            if 'n' in v[1].keys(): grid[x][y+1].set_none()
            if 's' in v[1].keys(): grid[x][y-1].set_none()
            if 'e' in v[1].keys(): grid[x+1][y].set_none()
            if 'w' in v[1].keys(): grid[x-1][y].set_none()
    
    return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(BLACK)

	for row in grid:
		for cell in row:
			cell.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width, preset = None, scale = 60):
    ROWS = scale
    grid = set_grid(ROWS, width, preset)
    start = None
    target = None

    run = True
    while run:
	    draw(win, grid, ROWS, width)

	    for event in pygame.event.get():
		    if event.type == pygame.QUIT:
			    run = False

		    if pygame.mouse.get_pressed()[0]: # LEFT
			    pos = pygame.mouse.get_pos()
			    row, col = get_clicked_pos(pos, ROWS, width)
			    cell = grid[row][col]
			    print(f'[{cell.x}, {cell.y}]')
			    if not start and cell != target:
				    start = cell
				    start.set_start()

			    elif not target and cell != start:
				    target = cell
				    target.set_target()

			    elif cell != target and cell != start:
				    cell.set_none()

		    elif pygame.mouse.get_pressed()[2]: # RIGHT
			    pos = pygame.mouse.get_pos()
			    row, col = get_clicked_pos(pos, ROWS, width)
			    cell = grid[row][col]
			    cell.set_barrier()
			    if cell == start:
				    start = None
			    elif cell == target:
				    target = None

		    if event.type == pygame.KEYDOWN:
			    if event.key == pygame.K_SPACE and start and target:
				    for row in grid:
					    for cell in row:
						    cell.update_neighbors(grid)

				    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, target)

			    if event.key == pygame.K_c:
				    start = None
				    target = None
				    grid = set_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH, cell_graph)