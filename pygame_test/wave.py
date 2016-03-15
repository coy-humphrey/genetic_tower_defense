import pygame
import random
from mob import *
import genetics

class Wave:
    def __init__(self, waveSize, mob_start, mob_path, breed):
        self.waveSize = waveSize
        self.mob_start = mob_start
        self.mob_path = mob_path
        self.delay = 500
        self.last_spawned = 0
        self.breedlist = breed[:]
        self.create_mob_list(waveSize, breed, mob_start, mob_path)
        print ("Created Wave", waveSize)

    def step(self, moblist):
        if not self.mob_list: return
        if pygame.time.get_ticks() - self.last_spawned > self.delay:
            moblist.append(self.mob_list.pop())
            self.last_spawned = pygame.time.get_ticks()

    def is_done(self):
        return not bool(self.mob_list)

    def create_mob_list(self, waveSize, breed, mob_start, mob_path):
        tmplist = []
        if breed:
            parents = genetics.get_n_winners(breed, 7)
            tmplist += genetics.get_n_crossovers(parents, 15, mob_start, mob_path)
            tmplist += genetics.get_n_mutants(parents, 10, mob_start, mob_path)

        self.mob_list = tmplist + [Mob(mob_start, (255,0,0), mob_path, [random.random() for i in range(5)]) for j in range(waveSize - len(tmplist))]
        random.shuffle(self.mob_list)