"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
from math import sqrt
from heapq import heappop, heappush
import csv

class Cell:
    # Heigh and Width of cells
    HEIGHT = 32
    WIDTH = 32
    # Types
    EMPTY = 0
    PATH = 1
    START = 2
    END = 3
    def __init__(self, grid, r,c,v):
        self.r = r
        self.c = c
        self.v = v
        self.grid = grid

    def get_center(self):
        grid = self.grid
        return (grid.x + Cell.WIDTH * self.c + .5 * Cell.WIDTH, grid.y + Cell.HEIGHT * self.r + .5 * Cell.HEIGHT)

    def get_neighbors(self):
        r,c = (self.r, self.c)
        modifiers = [(i,j) for i in range(-1, 2) for j in range(-1,2) if bool(i) != bool(j)]
        return [self.grid.get_cell(r+i, c+j) for i,j in modifiers if self.grid.in_bounds(r+i, c+j) and self.grid.get_cell(r+i,c+j).v == Cell.PATH]

    def get_weight(self):
        return 0 if v != Cell.PATH else 1


class Grid:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 166, 55)
    BROWN = (222, 184, 135)
    RED = (255, 0, 0)
 
    COLORS = [GREEN, BROWN]

    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.start = []
        self.end = []
        self.cells = [[Cell(self, r,c,0) for c in range(w)] for r in range(h)]

    def draw_grid(self, screen):
        for row, arr in enumerate(self.cells):
            for col, cell in enumerate(arr):
                color = self.COLORS[cell.v]
                pygame.draw.rect(screen,
                             color,
                             [self.x + Cell.WIDTH * col,
                              self.y + Cell.HEIGHT * row,
                              cell.WIDTH,
                              cell.HEIGHT])

    def cycle_cell(self, r,c):
        cell = self.cells[r][c]
        cell.v += 1
        cell.v %= len(self.COLORS)

    def get_cell(self, r,c):
        return self.cells[r][c]

    def in_bounds(self, r, c):
        return r >= 0 and r < self.h and c >= 0 and c < self.w

 
def get_shortest_path(start, dest):
    pq = []
    dist = {start: 0}
    prev = {start: None}
    heappush(pq,(0,start))
    while pq:
        d,cell = heappop(pq)
        if (cell == dest):
            break
        for x in cell.get_neighbors():
            alt = dist[cell] + 1
            if alt < dist.get(x,alt+1):
                dist[x] = alt
                prev[x] = cell
                heappush(pq,(dist[x],x))
    result = []
    curr = dest
    while curr in prev:
        result.insert(0, curr)
        curr = prev[curr]
    return result

def make_grid_from_file(filename):
    results = []
    with open (filename, 'rb') as file:
        mapreader = csv.reader(file)
        for row in mapreader:
            results.append (row)
        print results

    h = len (results)
    if results:
        w = len(results[0])

    grid = Grid(0,0,w,h)
    for r,col in enumerate(results):
        for c,val in enumerate(col):
            if val == 'S':
                grid.start.append(grid.get_cell(r,c))
                val = Cell.PATH
            if val == 'E':
                grid.end.append(grid.get_cell(r,c))
                val = Cell.PATH
            grid.get_cell(r,c).v = int(val)

    return grid

