import pygame
import numpy as np

class Mob:
    RAD = 10

    def __init__(self, start, color, path, speed, HP):
        self.x, self.y = start.get_center()
        self.color = color
        self.path = [x.get_center() for x in path[1:]]
        self.curr_dest = self.path[0]
        self.speed = speed
        self.distance_traveled = 0
        self.HP = HP

        print ("created mob")

    def move(self):
        if not self.curr_dest: return 0
        a,b = self.curr_dest
        if int(a) == int(self.x) and int(b) == int(self.y):
            if len (self.path) <= 1: return 0
            self.path.pop(0)
            self.curr_dest = self.path[0]

        if a > self.x:
            self.x += min(self.speed, a - self.x)
            self.distance_traveled += min(self.speed, a - self.x)
        elif a < self.x:
            self.x -= min(self.speed, self.x - a)
            self.distance_traveled += min(self.speed, self.x - a)
        if b > self.y:
            self.y += min(self.speed, b - self.y)
            self.distance_traveled += min(self.speed, b - self.y)
        elif b < self.y:
            self.y -= min(self.speed, self.y - b)
            self.distance_traveled += min(self.speed, self.y - b)
        return 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), Mob.RAD)


