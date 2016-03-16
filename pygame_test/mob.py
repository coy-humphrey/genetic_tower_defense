import pygame
import numpy as np
from damage_indicator import *
from mob_display import *
import genetics

class Mob:
    RAD = 10
    SPEED = 0
    HP = 1
    DEFENSE = 2
    FIREDEFENSE = 3
    MAGICDEFENSE = 4

    def __init__(self, start, color, path, statArray):
        self.statArray = genetics.normalize(statArray)
        self.x, self.y = start.get_center()
        self.color = color
        self.path = [x.get_center() for x in path[1:]]
        self.curr_dest = self.path[0]
        self.distance_traveled = 0

        self.speed = 0
        self.hp = 0
        self.defense = 0
        self.fireDefense = 0
        self.magicDefense = 0

        self.statsFromArray()

        # self.speed = 2

        self.max_health = self.hp
        
        self.hp_bar = HealthBar(self)
        self.damage_indicators = []

        self.attacked = 0
        self.survived = 0

    def move(self):
        if not self.curr_dest: return 0
        a,b = self.curr_dest
        if int(a) == int(self.x) and int(b) == int(self.y):
            if len (self.path) <= 1: return 0
            self.path.pop(0)
            self.curr_dest = self.path[0]

        dx = 0
        dy = 0

        if a > self.x:
            dx = min(self.speed, a - self.x)
            self.x += dx
        elif a < self.x:
            dx = min(self.speed, self.x - a)
            self.x -= dx
        if b > self.y:
            dy = min(self.speed, b - self.y)
            self.y += dy
        elif b < self.y:
            dy = min(self.speed, self.y - b)
            self.y -= dy
        
        self.distance_traveled += (dx + dy)
        return 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), Mob.RAD)
        self.hp_bar.update(self)
        self.hp_bar.draw(screen)
        self.damage_indicators = [d for d in self.damage_indicators if d.draw(screen, self)]

    def get_hurt(self, damage, type):
        if type == 0:
            damage -= self.defense
        if type == 1:
            damage -= self.magicDefense
        if type == 2:
            damage -= self.fireDefense

        damage = max (damage, 0)
        self.hp -= damage
        self.damage_indicators.append(DamageIndicator(damage))
        self.attacked += 1

    def is_dead(self):
        return self.hp <= 0

    def statsFromArray(self):
        a = self.statArray
        self.speed = 1 + 5 * a[Mob.SPEED]
        self.hp = 10 + 30 * a[Mob.HP]
        self.defense = 15 * a[Mob.DEFENSE]
        self.fireDefense = 15 * a[Mob.FIREDEFENSE]
        self.magicDefense = 15 * a[Mob.MAGICDEFENSE]