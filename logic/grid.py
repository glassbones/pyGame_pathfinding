from graphics.constants import RGB
from graphics.display import canvas
from logic.cell import Cell
from ast import literal_eval

class Grid:
    def __init__(self, width, row_num = 60):
        self.width = width
        self.row_num = row_num
        self.gap = width // row_num
        self.cells = []
        self.seen = set()

    def get_all_non_inactive_cells(self): return [cell for row in self.cells for cell in row if not cell.is_inactive()]
    def get_all_non_inactive_cell_ids(self): return [cell.id for row in self.cells for cell in row if not cell.is_inactive()]

    def get_cells_with_neighbor_count_of(self, num):
        non_inactive_cells = self.get_all_non_inactive_cells()
        for cell in non_inactive_cells: cell.update_neighbors()
        return [cell for cell in non_inactive_cells if len(cell.neighbors) == num] 

    def load_map(self, num):
        paths = ['logic/data/maps/main_maze.txt']

        map = literal_eval(open(paths[num-1], "r").read())
        # needs overhall
        # this load method converts edges to cells for the time being :/
        for k, v in map.items():
            x = v[0][0] * 2 - 1
            y = v[0][1] * 2 - 1
            self.cells[x][y].set_active()
            #if k == 0 : grid[x][y].set_start()
            if 'n' in v[1].keys(): self.cells[x][y+1].set_active()
            if 's' in v[1].keys(): self.cells[x][y-1].set_active()
            if 'e' in v[1].keys(): self.cells[x+1][y].set_active()
            if 'w' in v[1].keys(): self.cells[x-1][y].set_active()

    def set_grid(self, rows, width, preset=None):
        self.rows = rows
        self.width = width
        # making a square grid here based off the rows value
        for i in range(rows):
            self.cells.append([])
            for j in range(rows):
                cell = Cell(i, j, self)
                self.cells[i].append(cell)
                cell.set_id()
        # if there is a map param load that map
        if preset: self.load_map(preset)

    def find_branches(self):
        prospects = self.get_cells_with_neighbor_count_of(1)
        branches = set()
        forks = set()
        # itterate prospects
        while len(prospects) != 0:
            new_prospects = set()
            for prospect in prospects:
                branches.add(prospect)
                # travel through neighbors of each cell until we reach a fork
                for neighbor in prospect.neighbors:
                    if neighbor not in branches:
                        # each cell will have it's step count incremented by 1
                        neighbor.steps += 1
                        branches.add(neighbor)
                        # if a cell step count is equal to its neighbor count it is will be added to branches
                        if len(neighbor.neighbors) == neighbor.steps:
                            new_prospects.add(neighbor)
                         # if a cell step count is equal to its neighbors and its over 2 it will be added to prospects (these are branches within branches)
                        if len(neighbor.neighbors) > 2:
                            branches.remove(neighbor)
                            forks.add(neighbor)
            prospects = new_prospects 
        # paint out the branches
        canvas.draw_circuit(self, forks, branches)


#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################

def all_cells_of(graph):
    [cell.set_id() for row in graph for cell in row]
    return [cell.id for row in graph for cell in row if cell.color != RGB.BLACK]


    #return [cell for row in graph for cell in row if len(cell.neighbors) == num]





