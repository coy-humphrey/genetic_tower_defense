import pygame
from math import sqrt
from heapq import heappop, heappush
from grid import *
from mob import *
import random
from tower import *
from operator import *
from mob_display import *
import genetics
from wave import *
 
# Some code borrowed from:
# http://programarcadegames.com/index.php?chapter=array_backed_grids

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
COLORS = [WHITE, GREEN, BLACK, RED]

TOWERS = [Tower, ArrowTower, BombTower, FireTower]

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
WINDOW_SIZE = [950, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Genetic Tower Defense")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
grid = make_grid_from_file("test.csv")

path = []
if (grid.start and grid.end):
    path = get_shortest_path(grid.start[0], grid.end[0])

tower_type = 0

mobs = []
towers = []
breed = []
curr_cell = grid.get_cell(0,0)
info_panel = MobInfoPanel((800,0))
wave = Wave(30,grid.start[0], path, breed)
wave_done = False
timer = pygame.time.get_ticks()
wave_delay = 10000
wave_delayed = True

num_survived = 0
num_survived_new = 0
round_num = 1
font = pygame.font.SysFont("monospace", 16)

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
            curr_cell = grid.get_cell(row,column)

            button = pygame.mouse.get_pressed()
            if button[0]:
                # Set that location to zero
                grid.cycle_cell(row,column)
                start = grid.get_cell(row, column)
                end = grid.get_cell(0,0)
                if grid.start:
                    start = grid.start[0]
                if grid.end:
                    end = grid.end[0]
                path = get_shortest_path(start, end)
            else:
                t = TOWERS[tower_type](curr_cell, BLACK)
                towers.append(t)
            
            print("Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mob_start = curr_cell
            mob_path = path
            if grid.start and grid.end:
                mob_start = random.choice(grid.start)
                mob_end = random.choice(grid.end)
                mob_path = get_shortest_path(mob_start, mob_end)
            statArray = genetics.normalize([random.random() for i in range(5)])
            m = Mob(mob_start, RED, mob_path, statArray)
            mobs.append(m)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            tower_type = (tower_type + 1) % len(TOWERS)


    if wave.is_done() and not wave_done:
        print ("wave done")
        wave_done = True

    if wave_done:
        if not mobs:
            print ("next wave")
            wave = Wave(30,grid.start[0], path, breed)
            num_survived = num_survived_new
            num_survived_new = 0
            info_panel.update(breed)
            breed = []
            wave_done = False
            round_num += 1

    if not wave_delayed or pygame.time.get_ticks() - timer > wave_delay:
        wave_delayed = False
        wave.step(mobs)

    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    grid.draw_grid(screen)
    draw_path(screen, path)

    for t in towers:
        t.attack(mobs)
        t.draw(screen)

    for m in mobs:
        if not m.move() or m.is_dead():
            breed.append(m)
            breed.sort(key=genetics.fitness, reverse = True)
            mobs.remove(m)
            if not m.is_dead():
                num_survived_new += 1
                m.survived = True
        else:
            m.draw(screen)

    info_panel.draw(screen)

    survivor_str = "Survivors Last Round: " + str(num_survived)
    label = font.render(survivor_str, 1, BLACK)
    location = (250, 30)
    screen.blit(label, location)
    round_str = "Round: " + str(round_num)
    label = font.render(round_str, 1, BLACK)
    location = (250, 60)
    screen.blit(label, location)


    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()