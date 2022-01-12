import math
import pygame, sys
from pygame.locals import *
from queue import PriorityQueue
import heapq

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,221,208)

ROWS = 30

        
def manhattan(dx, dy):
    return abs(dx + dy)

class Node:
    def __init__(self):
        self.pos = None
        self.parent = None
        self.g = None
        self.h = None
        self.f = None
        self.status = None
        self.color = WHITE
    
    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f
    
    def __str__(self):
        return "({}) [g: {}, h: {}, f: {}]".format(
            self.pos, self.g, self.h, self.f 
        )

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE




class AStar:
    def __init__(self, graph):
        self.graph = graph
        self.rows = len(self.graph)
        self.cols = len(self.graph)

        self.source = None
        self.target = None
        
        for y in range(self.rows):
            for x in range(self.cols):
                if self.graph[y][x].color == ORANGE:
                    self.source = (y, x)
                elif self.graph[y][x].color == TURQUOISE:
                    self.target = (y, x)
        
        self.open_list = []
        self.closed_list = []
        self.node_tracker = {}

    def find_path(self):
        self.open_list.clear()
        self.closed_list.clear()

        start_node = self.graph[self.source[1]][self.source[0]]

class Graph:
    def __init__(self, rows):
        self.rows = rows
        self.graph = []
        for i in range(self.rows):
            arr = []
            for j in range(self.rows):
                arr.append(Node)
            self.graph.append(arr)

def main(grid):
    
    run = True
    while run:
        WIN.fill(WHITE)
        nodeWidth = WIDTH//ROWS
        for i in range(grid.rows):
            for j in range(grid.rows):
                x, y = i * nodeWidth, j * nodeWidth
                rect = Rect(x, y, nodeWidth, nodeWidth)
                pygame.draw.rect(WIN, GREEN, rect, 10)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update
    pygame.quit()

if __name__ == "__main__":
    grid = Graph(ROWS)
    main(grid)


