import pygame
import math
from queue import PriorityQueue

# Window
width = 800
win = pygame.display.set_mode((width, width)) # this is the window height/width
pygame.display.set_caption("pygame pathfinding")

# Colors
RED = (255,0,0)
ORANGE = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
TURQUOISE = (64,224,208)
BLUE = (0,0,255)
PURPLE = (128,0,128) 

WHITE = (255,255,255)
GREY = (128,128,128)
BLACK = (0,0,0) 

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []