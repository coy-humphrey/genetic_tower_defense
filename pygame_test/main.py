import pygame
from math import sqrt
from heapq import heappop, heappush
from grid import *
from mob import *
from random import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
COLORS = [WHITE, GREEN, BLACK, RED]

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 32
HEIGHT = 32
 
# This sets the margin between each cell
MARGIN = 0
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
GRID_WIDTH = 25
GRID_HEIGHT = 25

def draw_path(screen, path):
    for i,j in zip(path, path[1:]):
        pygame.draw.line(screen,RED, i.get_center(), j.get_center())

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
grid = Grid(0,0,25,25)

path = []
mobs = []
curr_cell = grid.get_cell(0,0)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to zero
            grid.cycle_cell(row,column)
            path = get_shortest_path(grid.get_cell(row,column), grid.get_cell(0,0))
            curr_cell = grid.get_cell(row,column)
            print("Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        	m = Mob(curr_cell, RED, path, random() + .5)
        	mobs.append(m)

    mobs = [m for m in mobs if m.move()]

 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    grid.draw_grid(screen)
    draw_path(screen, path)
    for m in mobs:
    	m.draw(screen)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
