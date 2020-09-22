import uuid
import pygame
import math
import random
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
DARKER_GREY = (32, 32, 32)
DARKEST_GREY = (16, 16, 16)
BLACK = (0, 0, 0)

map_file = "logic/data/maps/main_maze.txt"
cell_graph=literal_eval(open(map_file, "r").read())


def circuit_walk(path):
    print('circuit walk')
    seen = set(path)
    next_circuit_cell = []

    for neighbor in path[-1].neighbors:
        if not neighbor.is_branch:
            if neighbor not in seen:
                next_circuit_cell.append(neighbor)

    if next_circuit_cell == []: return path[-1]
    if len(next_circuit_cell) == 3: return circuit_compare(next_circuit_cell[0], next_circuit_cell[1], next_circuit_cell[2])
    if len(next_circuit_cell) == 2: return circuit_compare(next_circuit_cell[0], next_circuit_cell[1])
    if len(next_circuit_cell) == 1: return next_circuit_cell[0]

def circuit_compare(a, b, c = None):
    print('circuit_compare')
    lst = [a,b]
    if c: lst = [a,b,c]
    return random.choice(lst)
    """
    a_path = [a]
    b_path = [b]
    i = 0

    while len(a_path) != i and len(b_path) != i:
        a_next_circuit_cell = circuit_walk(a_path)
        b_next_circuit_cell = circuit_walk(b_path)

        if a_next_circuit_cell == a_path -1: 
            if c != None: return circuit_compare(a, c)
            else: return a
        if b_next_circuit_cell == b_path -1: 
            if c != None: return circuit_compare(b, c)
            else: return b
        
        a_path = a_path.append(a_next_circuit_cell)
        b_path = b_path.append(b_next_circuit_cell)
        i += 1
    """


def all_cells_of(graph):
    [cell.set_id() for row in graph for cell in row]
    return [cell.id for row in graph for cell in row if cell.color != BLACK]

def get_rooms_with_neighbor_count_of(graph, num):
    lst = []
    for row in graph:
        for cell in row:
            cell.update_neighbors(graph)
            if (cell.color != BLACK):
                if (len(cell.neighbors) == num):
                    lst.append(cell)
                    
    return lst
    #return [cell for row in graph for cell in row if len(cell.neighbors) == num]

def find_branches(win, graph, ROWS, width):
    quads = get_rooms_with_neighbor_count_of(graph, 4)
    tris = get_rooms_with_neighbor_count_of(graph, 3)
    duos = get_rooms_with_neighbor_count_of(graph, 2)
    solos = get_rooms_with_neighbor_count_of(graph, 1)
    branches = set()
    forks = set()
    # itterate prospects
    # travel through neighbors of each room until you reach a fork
    # each room will have step count incremented by 1
    # if a rooms step count is equal to its neighbor count it is will be added to branches
    # if a rooms step count is equal to its neighbors and its over 2 it will be added to prospects (these are branches within branches)
    prospects = solos
    while len(prospects) != 0:
        new_prospects = set()
        for prospect in prospects:
            branches.add(prospect)
            for neighbor in prospect.neighbors:
                if neighbor not in branches:
                    neighbor.steps += 1
                    branches.add(neighbor)
                    if len(neighbor.neighbors) == neighbor.steps: # and len(neighbor.neighbors) > 2:
                        new_prospects.add(neighbor)
                        #continue
                    if len(neighbor.neighbors) > 2:
                        branches.remove(neighbor)
                        forks.add(neighbor)
        prospects = new_prospects 
    # add all the forks that didnt make it into the prospects to branches
    "[branches.add(fork) for fork in forks]"
    "cell.color = DARKEST_GREY"

    for cell in forks:
        cell.color = DARKER_GREY
        
    for cell in branches:
        draw(win, graph, ROWS, width)
        cell.color = DARKEST_GREY
        cell.set_is_branch()



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

    return cell_dict


class Counter:
    def __init__(self, count):
        self.count = count

    def increase_by(self, num): self.count = self.count + num

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
        self.steps = 1
        self.is_branch = False
        self.is_seen = False
        self.id = None
        
	#def is_closed(self): return self.color == GREY
	#def is_open(self): return self.color == LIGHT_GREY
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_target(self): return self.color == TURQUOISE

    def set_none(self): self.color = DARK_GREY
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
    def set_back_track(self): self.color = RED
    def set_id(self):
        if self.id == None: self.id = uuid.uuid1()
    def set_is_seen(self): self.is_seen = True
    def set_is_branch(self): self.is_branch = True
    def get_pos(self): return self.row, self.col
    def get_active_neighbors(self): return [neighbor for neighbor in self.neighbors if neighbor.color != BLACK]
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


def reconstruct_path(came_from, current, draw, counter):
    while current in came_from:
        current = came_from[current]
        #if current.color == PURPLE: current.set_back_track()
        #else: current.set_path()
        current.set_path()
        counter.increase_by(1)
        draw()


def algorithm(draw, grid, start, target, counter):
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
            reconstruct_path(came_from, target, draw, counter)
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
             cell = Cell(i, j, gap, rows)
             grid[i].append(cell)

    
    if preset:
        for k, v in preset.items():
            x = v[0][0] * 2 - 1
            y = v[0][1] * 2 - 1
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
    find_branches(win, grid, ROWS, width)
    start = None
    target = None
    seen = set()
    all_cells = all_cells_of(grid)
    counter = Counter(0)

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
                if event.key == pygame.K_SPACE and start:
                    # current position is circuit flag
                    circuit_flag = start
                    branch_flags = []

                    while len(seen) != len(all_cells):
                        
                        start.set_is_seen()
                        seen.add(start)
                        print(f'start is {start.x} , {start.y}')
                        # if branch flag at current position remove it
                        branch_flags = [ _ for _ in branch_flags if _ != start ]
                        # if 2 or more current neighbors are untraveled nodes branch flag here
                        unseen = [neighbor for neighbor in start.neighbors if not neighbor.is_seen]
                        if len(unseen) > 1: branch_flags.append(start)
                        # if 2 or more current neighbors are untraveled circuit nodes circuit flag here
                        unseen_circuit_cells = [neighbor for neighbor in unseen if not neighbor.is_branch and not neighbor.is_seen]
                        if len(unseen_circuit_cells) > 1: circuit_flag = start

                        # if no untraveled neighbors, target is last branch flag
                        print(f'unseen = {[neighbor.x for neighbor in start.neighbors if not neighbor.is_seen]}')
                        if unseen == []:
                            if branch_flags != []:
                                target = branch_flags[-1]
                            elif branch_flags == []:
                                # if no branch flag return to circuit flag
                                if target != start:
                                    target = circuit_flag
                                # if current position is circuit flag maze should be complete ???????????
                                if target == start:
                                    print('this shouldn\'t print unless everything is explored') 
                        
                        # if any neighbor is untraveled branch node target is that node pick node farther from last circuit flag
                        print(f'unseen = {[neighbor.x for neighbor in start.neighbors if not neighbor.is_seen]}')
                        if unseen != []:
                            unseen_branch_cells = [neighbor for neighbor in unseen if neighbor.is_branch]
                            # this is not optimal, need a tie breaker function that travels shortest dead end first
                            print(f'unseen branches = {[neighbor for neighbor in unseen if neighbor.is_branch]}')
                            if unseen_branch_cells != []: target = unseen_branch_cells[0]
                            else:
                                print(f'unseen circuits = {[neighbor for neighbor in unseen if not neighbor.is_branch]}')
                                # if any neighbor is untraveled circuit node target pick optimal path
                                if len(unseen_circuit_cells) == 4: target = circuit_compare(circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1]), circuit_compare(unseen_circuit_cells[2],unseen_circuit_cells[3]))
                                if len(unseen_circuit_cells) == 3: target = circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1],unseen_circuit_cells[2])
                                if len(unseen_circuit_cells) == 2: target = circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1])
                                else: target = unseen_circuit_cells[0]

                        if len(unseen) == 1: target = unseen[0]

                        for row in grid:
                            for cell in row:
                                cell.update_neighbors(grid)
                        print(f'target is {target.x} , {target.y}')
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, target, counter)

                        start = target
                        start.color = ORANGE
                        target = None
                
                
                print(f'step count = {counter.count}')
                print(len(all_cells))
                print(len(seen))


                if event.key == pygame.K_c:
                    start = None
                    target = None
                    grid = set_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH, cell_graph)