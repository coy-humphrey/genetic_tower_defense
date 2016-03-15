import pygame
import numpy as np
from damage_indicator import *
from mob_display import *

class Mob:
    RAD = 10

    def __init__(self, start, color, path, statArray):
        self.statArray = statArray
        self.x, self.y = start.get_center()
        self.color = color
        self.path = [x.get_center() for x in path[1:]]
        self.curr_dest = self.path[0]
        self.distance_traveled = 0

        self.speed = statArray[0]
        self.HP = statArray[1]
        self.defense = statArray[2]
        self.fireDefense = statArray[3]
        self.max_health = self.HP
        
        self.hp_bar = HealthBar(self)
        self.damage_indicators = []

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
        self.hp_bar.update(self)
        self.hp_bar.draw(screen)
        self.damage_indicators = [d for d in self.damage_indicators if d.draw(screen, self)]

    def get_hurt(self, damage, type):
        self.HP -= damage
        self.damage_indicators.append(DamageIndicator(damage))



