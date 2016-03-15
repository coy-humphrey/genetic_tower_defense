import pygame
import random
from mob import *

class Wave:
    def __init__(self, waveSize, mob_start, mob_path, breed):
        self.mob_list = [Mob(mob_start, (255,0,0), mob_path, [random.random() for i in range(5)]) for j in range(waveSize)]
        self.waveSize = waveSize
        self.mob_start = mob_start
        self.mob_path = mob_path
        self.delay = 500
        self.last_spawned = 0

    def step(self, moblist):
        if not self.mob_list: return
        if pygame.time.get_ticks() - self.last_spawned > self.delay:
            moblist.append(self.mob_list.pop())
            self.last_spawned = pygame.time.get_ticks()

    def is_done(self):
        return bool(self.mob_list)