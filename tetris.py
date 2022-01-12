import pygame
import random
from pygame.locals import *

pygame.init()
WIN = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Tetris 2P")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Tiles:
    def __init__(self, total_rows, width, row, col):
        self.pos = None
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.col, self.row

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

def make_grid(rows, width):
    grid = []
    cellWidth = width // rows 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tiles = Tiles(rows, cellWidth, i, j)
            grid[i].append(tiles)
    return grid

def draw_line(win, rows, width):
    cellWidth = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * cellWidth), (width, i * cellWidth))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * cellWidth, 0), (j * cellWidth, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_line(win, rows, width)
    pygame.display.update()

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    run = True
    while (run):
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main(WIN, 800)

