import pygame

class Render:
    def __init__(self):
        self.WIDTH = 900

        def create_window(self):
            WIN = pygame.display.set_mode((self.WIDTH, self.WIDTH))
            pygame.display.set_caption("Path finding visualized")
            return WIN

class Color:
    def __init__(self):
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165 ,0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.TURQUOISE = (64, 224, 208)
        self.BLUE = (0, 255, 0)
        self.PURPLE = (128, 0, 128)

        self.WHITE = (255, 255, 255)
        self.LIGHT_GREY = (192, 192, 192)
        self.GREY = (128, 128, 128)
        self.DARK_GREY = (64, 64, 64)
        self.DARKER_GREY = (32, 32, 32)
        self.DARKEST_GREY = (16, 16, 16)
        self.BLACK = (0, 0, 0)

RGB = Color()
RENDER = Render()
WIN = RENDER.create_window() 