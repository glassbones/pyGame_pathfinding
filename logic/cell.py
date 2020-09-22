import pygame
import uuid
from ..graphics.constants import RGB

class Cell:
    def __init__(self, row, col, width, total_rows, grid):
        #position
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.total_rows = total_rows
        self.grid = grid
        # graphic attrs
        self.color = RGB.BLACK
        self.width = width
        # data attrs
        self.id = None
        self.neighbors = []
        self.steps = 1
        self.is_branch = False
        self.is_seen = False

    # check color
    def is_inactive(self): return self.color == RGB.BLACK
    def is_start(self): return self.color == RGB.ORANGE
    def is_target(self): return self.color == RGB.TURQUOISE
    # set color
    def set_active(self): self.color = RGB.DARK_GREY
    def set_inactive(self): self.color = RGB.BLACK
    def set_start(self): self.color = RGB.ORANGE
    def set_target(self): self.color = RGB.TURQUOISE
    def set_path(self): self.color = RGB.PURPLE
    def set_back_track(self): self.color = RGB.RED
    def set_open(self): self.lighten_color()     
    def set_closed(self): self.lighten_color()
    # lighten color
    def lighten_color(self):
        if self.color[0] <= 240: self.color = (self.color[0]+16, self.color[1], self.color[2])
        if self.color[1] <= 240: self.color = (self.color[0], self.color[1]+16, self.color[2])
        if self.color[2] <= 240: self.color = (self.color[0], self.color[1], self.color[2]+16)   
    # set data attrs
    def set_id(self): self.id = uuid.uuid1()
    def set_is_seen(self): self.is_seen = True
    def set_is_branch(self): self.is_branch = True
    def set_northern_neighbor(self): self.neighbors.append(self.grid[self.row - 1][self.col])
    def set_southern_neighbor(self): self.neighbors.append(self.grid[self.row + 1][self.col])
    def set_eastern_neighbor(self): self.neighbors.append(self.grid[self.row][self.col + 1])
    def set_western_neighbor(self): self.neighbors.append(self.grid[self.row][self.col - 1])
    # check data attrs
    def is_not_in_first_row(self): return not bool(self.row)
    def is_not_in_last_row(self): return not bool(self.row - (self.total_rows - 1))
    def is_not_in_first_column(self): return not bool(self.col)
    def is_not_in_last_column(self): return not bool(self.row - (self.total_rows - 1))
    def has_active_northern_neighbor(self): return not bool(self.grid[self.row - 1][self.col].is_inactive())
    def has_active_southern_neighbor(self): return not bool(self.grid[self.row + 1][self.col].is_inactive())
    def has_active_eastern_neighbor(self): return not bool(self.grid[self.row][self.col + 1].is_inactive())
    def has_active_western_neighbor(self): return not bool(self.grid[self.row][self.col - 1].is_inactive())
    def update_neighbors(self): # neighbors cannot be inactive cells
        self.neighbors = []
        if self.is_not_in_first_row() and self.has_active_northern_neighbor(): self.set_northern_neighbor()
        if self.is_not_in_last_row() and self.has_active_southern_neighbor(): self.set_southern_neighbor()
        if self.is_not_in_last_column() and self.has_active_eastern_neighbor(): self.set_eastern_neighbor()
        if self.is_not_in_first_column() and self.has_active_western_neighbor(): self.set_western_neighbor()
    # get data attrs
    def get_pos(self): return self.row, self.col
    def get_active_neighbors(self): return [neighbor for neighbor in self.neighbors if neighbor.color != RGB.BLACK]
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def __lt__(self, other): return False