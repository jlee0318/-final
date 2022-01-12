import sys
import heapq
import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* path finding algorithm")

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

OFFSET = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIST = 10

OPEN = 0
CLOSED = 1

class Node:
    def __init__(self, total_rows, width, row, col):
        self.pos = None
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.parent = None
        self.g = None
        self.h = None
        self.f = None
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.col, self.row

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

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

def manhattan(dx, dy):
    return dx + dy

heuristic_dict = {
    0: manhattan
}

class Astar:
    def __init__(self, graphtext, sourceX, sourceY, targetX, targetY, heuristic=0):
        self.nodes = graphtext
        self.rows = len(self.nodes)
        self.cols = len(self.nodes[0])
        self.source = (sourceX, sourceY)
        self.target = (targetX, targetY)
        #for row in range(self.rows):
            #for col in range(self.cols):
                #if self.nodes[row][col].is_start():
                 #   self.source = (col, row)
              #  elif self.nodes[row][col].is_closed():
                    #self.target = (col, row)

        self.openlist = []
        self.closedlist = []
        self.nodetracker = {}
        #self.nodes = [[Node() for col in range(self.cols)] for row in range(self.rows)]

        self.h_func = heuristic_dict.get(heuristic, None)
        if self.h_func is None:
            #raise InvalidHeuristic
            pass

    def find_path(self):
        self.openlist.clear()
        self.closedlist.clear()

        startnode = self.nodes[self.source[1]][self.source[0]]
        startnode.pos = self.source
        startnode.make_open()
        startnode.f = 0
        startnode.g = 0
        startnode.h = 0
        heapq.heappush(self.openlist, startnode)
        success = False
        offset = len(OFFSET)
        while self.openlist:
            current = heapq.heappop(self.openlist)
            self.closedlist.append(current)
            current.make_closed()
            if current.pos == self.target:
                success = True
                break
            for i in range(offset):
                dx, dy = OFFSET[i]
                x = current.pos[0] + dx
                y = current.pos[1] + dy
                if self._is_walkable(x, y):
                    self._expand(current, x, y, DIST)

        return success

    def walks(self):
        if not self.closedlist:
            return []
        paths = []
        current = self.closedlist[-1]
        if current.pos != self.target:
            return []
        while current is not None:
            paths.append(current.pos)
            current = current.parent
        return paths[::-1]

    def _is_walkable(self, x, y):
        return x >= 0 and x < self.cols and y >= 0 and y < self.rows and self.nodes[y][x].color != BLACK

    def _expand(self, parent, x, y, g_cost):
        node = self.nodes[y][x]
        if node.is_closed():
            return
        
        if node.color != GREEN:
            node.make_open()
            self._update_node(node, x, y, parent, g_cost)
            heapq.heappush(self.openlist, node)
        else:
            if self._update_node(node, x, y, parent, g_cost):
                heapq.heapify(self.openlist)

    def _update_node(self, node, x, y, parent, g_cost):
        new_g = parent.g + g_cost
        if node.g is None or new_g < node.g:
            node.pos = (x, y)
            node.parent = parent
            node.g = new_g
            node.h = self._calc_h(x, y)
            node.f = node.g + node.h
            return True
        return False

    def _calc_h(self, x, y):
        dx = abs(x - self.target[0])
        dy = abs(y - self.target[1])
        return self.h_func(dx, dy) * 10

def make_grid(rows, width):
    grid = []
    cellWidth = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(rows, cellWidth, i, j)
            grid[i].append(node)

    return grid

def draw_line(win, rows, width):
    cellWdith = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * cellWdith), (width, i*cellWdith))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*cellWdith, 0), (j*cellWdith, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_line(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    cellWidth = width // rows
    x, y = pos

    row = y // cellWidth
    col = x // cellWidth

    return row, col

def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)
    #grid[x][y]

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: #left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    startpos = start.get_pos()

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    endpos = end.get_pos()
                    #print(end.get_pos())

                elif spot != end and spot != start:
                    spot.make_barrier()
            
            #print(end.get_pos)


            elif pygame.mouse.get_pressed()[2]: #right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started: # run algorithm
                    #for row in grid:
                        #for spot in row:
                            #spot.update_neighbors(grid)
                    astar = Astar(grid, startpos[0], startpos[1], endpos[0], endpos[1])
                    astar.find_path()
                    answer = astar.walks()
                    print(answer)
                    for i in range(len(answer)):
                        
                        #print(answer[i])
                        grid[answer[i][1]][answer[i][0]].make_path()
                        start.make_start()
                        end.make_end()
                
                if event.key == pygame.K_r: # reset graph
                    grid = make_grid(ROWS, width)
                    start = None
                    end = None
                

    pygame.quit()

main(WIN, WIDTH)