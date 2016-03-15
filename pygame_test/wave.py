import pygame
import random
from mob import *




class Wave:

    moblist = []


    def __init__(self, waveSize, mob_start, mob_path):
        self.waveSize = waveSize
        self.mob_start = mob_start
        self.mob_path = mob_path
        self.delay = 500
        self.last_spawned = 0


    def wave(self):
        counter = self.waveSize
        if pygame.time.get_ticks() - self.last_spawned < self.delay:
            counter -= 1
            statArray = [random.randint(5,10), random.randint(5,10), random.randint(5,10), random.randint(5,10)]
            m = Mob(self.mob_start, RED, self.mob_path, statArray)
            self.moblist.append(m)

        self.last_spawned = pygame.time.get_ticks()