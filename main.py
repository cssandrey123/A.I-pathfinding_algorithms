import pygame
from pygame.locals import *
import math
from queue import PriorityQueue, Queue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.init()
pygame.display.set_caption("AI algorithms")


OLIVE = (107, 142, 35)
KAKI = (240, 230, 140)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHOCOLATE = (210, 105, 30)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
BLUE = (0, 191, 255)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neigbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == OLIVE

    def is_open(self):
        return self.color == KAKI

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = OLIVE

    def make_open(self):
        self.color = KAKI

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = CHOCOLATE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # updateaza posibilii vecini
    def update_neighbors(self, grid):
        self.neigbors = []

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # STANGA
            self.neigbors.append(grid[self.row][self.col - 1])
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):  # DREAPTA
            self.neigbors.append(grid[self.row][self.col + 1])

        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):  # JOS
            self.neigbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # SUS
            self.neigbors.append(grid[self.row - 1][self.col])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_From, current, drawM):
    while current in came_From:
        current = came_From[current]
        current.make_path()
        drawM()


def runAStar(drawM, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_From = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # stocheaza aceleasi noduri (doar nodurile) ca si open_set, doar ca aici putem sti ce noduri exista
    open_set_hash = {start}

    while not open_set.empty():
        # Daca se inchide interfata in timp ce algoritmul merge, inchide si interfata. Ca sa nu genereze erori
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # pozitia [2] ia nodul
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # a gasit calea
        if current == end:
            reconstruct_path(came_From, end, drawM)
            end.make_end()
            return True

        for neigbor in current.neigbors:
            # plus unu deoarece simulam ca am ajuns la nodul vecin din nodul curent (fiecare pas costa 1)
            temp_g_score = g_score[current] + 1

            # daca calea pe care am parcurs-o acum este mai scurta decat calea salvata pana la vecinul curent, salveaz-o pe asta
            if temp_g_score < g_score[neigbor]:
                came_From[neigbor] = current
                g_score[neigbor] = temp_g_score
                f_score[neigbor] = temp_g_score + h(neigbor.get_pos(), end.get_pos())
                if neigbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neigbor], count, neigbor))
                    open_set_hash.add(neigbor)
                    neigbor.make_open()
        drawM()

        if current != start:
            current.make_closed()
    return False


def runGBFS(drawM, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_From = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # stocheaza aceleasi noduri (doar nodurile) ca si open_set, doar ca aici putem sti ce noduri exista
    open_set_hash = {start}

    while not open_set.empty():
        # Daca se inchide interfata in timp ce algoritmul merge, inchide si interfata. Ca sa nu genereze erori
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # pozitia [2] ia nodul
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # a gasit calea
        if current == end:
            reconstruct_path(came_From, end, drawM)
            end.make_end()
            return True

        for neigbor in current.neigbors:
            # plus unu deoarece simulam ca am ajuns la nodul vecin din nodul curent (fiecare pas costa 1)
            temp_g_score = g_score[current] + 1

            # daca calea pe care am parcurs-o acum este mai scurta decat calea salvata pana la vecinul curent, salveaz-o pe asta
            if temp_g_score < g_score[neigbor]:
                came_From[neigbor] = current
                g_score[neigbor] = temp_g_score
                f_score[neigbor] = h(neigbor.get_pos(), end.get_pos())
                if neigbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neigbor], count, neigbor))
                    open_set_hash.add(neigbor)
                    neigbor.make_open()
        drawM()

        if current != start:
            current.make_closed()
    return False


def runBFS(drawM, grid, start, end):
    open_set = Queue()
    open_set.put(start)
    came_From = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # stocheaza aceleasi noduri (doar nodurile) ca si open_set, doar ca aici putem sti ce noduri exista
    open_set_hash = {start}

    while not open_set.empty():
        # Daca se inchide interfata in timp ce algoritmul merge, inchide si interfata. Ca sa nu genereze erori
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # pozitia [2] ia nodul
        current = open_set.get()
        open_set_hash.remove(current)

        # a gasit calea
        if current == end:
            reconstruct_path(came_From, end, drawM)
            end.make_end()
            return True

        for neigbor in current.neigbors:
            # plus unu deoarece simulam ca am ajuns la nodul vecin din nodul curent (fiecare pas costa 1)
            temp_g_score = g_score[current] + 1

            # daca calea pe care am parcurs-o acum este mai scurta decat calea salvata pana la vecinul curent, salveaz-o pe asta
            if temp_g_score < g_score[neigbor]:
                came_From[neigbor] = current
                g_score[neigbor] = temp_g_score
                if neigbor not in open_set_hash:
                    open_set.put(neigbor)
                    open_set_hash.add(neigbor)
                    neigbor.make_open()
        drawM()

        if current != start:
            current.make_closed()
    return False


def runDFS(drawM, grid, start, end):
    open_set = []
    open_set.append(start)
    came_From = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # stocheaza aceleasi noduri (doar nodurile) ca si open_set, doar ca aici putem sti ce noduri exista
    visited = {start}

    while open_set:
        # Daca se inchide interfata in timp ce algoritmul merge, inchide si interfata. Ca sa nu genereze erori
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # pozitia [2] ia nodul
        visitedNeighbor = False
        current = open_set[-1]

        # a gasit calea
        if current == end:
            reconstruct_path(came_From, end, drawM)
            end.make_end()
            return True

        for neigbor in current.neigbors:
            # plus unu deoarece simulam ca am ajuns la nodul vecin din nodul curent (fiecare pas costa 1)
            if neigbor in visited:
                continue
            temp_g_score = g_score[current] + 1
            visitedNeighbor = True

            # daca calea pe care am parcurs-o acum este mai scurta decat calea salvata pana la vecinul curent, salveaz-o pe asta
            if temp_g_score < g_score[neigbor]:
                came_From[neigbor] = current
                g_score[neigbor] = temp_g_score
                if neigbor not in open_set:
                    visited.add(neigbor)
                    open_set.append(neigbor)
                    neigbor.make_open()
            break
        drawM()
        if visitedNeighbor == False:
            open_set.pop()
        if current != start:
            current.make_closed()
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # click stanga
                # ia pozitia actuala a mouselui in rap cu fereastra
                pos = pygame.mouse.get_pos()
                # o transforma intr-un indice care corespunde nodului din tablul cu noduri
                row, col = get_clicked_pos(pos, ROWS, width)
                nod = grid[row][col]
                if not start and nod != end:
                    # seteaza nodul de start
                    start = nod
                    nod.make_start()
                elif not end and nod != start:
                    # seteaza nodul de finish
                    end = nod
                    nod.make_end()
                elif nod != end and nod != start:
                    nod.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # click dreapta
                # ia pozitia actuala a mouselui in rap cu fereastra
                pos = pygame.mouse.get_pos()
                # o transforma intr-un indice care corespunde nodului din tablul cu noduri
                row, col = get_clicked_pos(pos, ROWS, width)
                nod = grid[row][col]
                nod.reset()

                # daca se apasa click dreapta pe nodurile de start/end, se reseteaza
                if nod == start:
                    start = None
                elif nod == end:
                    end = None
            # cand se apace pe space, incepe algoritmul
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and start and end:  # BFS alg pe tasta 1
                    for row in grid:
                        for nod in row:
                            # pentru fiecare nod, updateaza vecinii la care poate ajunge
                            nod.update_neighbors(grid)
                    # aici incepe algoritmul
                    runBFS(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_2 and start and end:  # DFS alg pe tasta 2
                    for row in grid:
                        for nod in row:
                            # pentru fiecare nod, updateaza vecinii la care poate ajunge
                            nod.update_neighbors(grid)
                    # aici incepe algoritmul
                    runDFS(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_3 and start and end:  # GBFS alg pe tasta 3
                    for row in grid:
                        for nod in row:
                            # pentru fiecare nod, updateaza vecinii la care poate ajunge
                            nod.update_neighbors(grid)
                    # aici incepe algoritmul
                    runGBFS(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_4 and start and end:  # A*
                    for row in grid:
                        for nod in row:
                            # pentru fiecare nod, updateaza vecinii la care poate ajunge
                            nod.update_neighbors(grid)
                    # aici incepe algoritmul

                    runAStar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
