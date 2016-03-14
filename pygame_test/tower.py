import pygame
from mob import *
import numpy as np

class Tower:
    RED = (255,0,0)
    RAD = 10

    def __init__(self, location, color):
        self.x, self.y = location.get_center()
        self.c = color


        print ("created tower")

    def attack(self):
        return 1


    def draw(self, screen):
        pygame.draw.circle(screen, Tower.RED,(int(self.x),int(self.y)), 100, 1)
        pygame.draw.circle(screen, self.c, (int(self.x), int(self.y)), Tower.RAD)

    def mobs_in_range(self, mob_list):
        results = []
        for m in mob_list:
            mob_x = m.x
            mob_y = m.y

            tow_x = self.x
            tow_y = self.y
            
            if ((mob_x - tow_x)**2 + (mob_y - tow_y)**2) < 100**2:
                    results.append(m)
        return results
