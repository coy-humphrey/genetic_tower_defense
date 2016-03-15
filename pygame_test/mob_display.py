import pygame
from grid import *

class StatBar:
	def __init__(self, color, value, pos, width, height):
		self.width = width
		self.height = height
		self.x, self.y = pos
		self.color = color
		self.value = value # float between 0 and 1

	def draw(self, screen):
		pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.width, self.height))
		pygame.draw.rect(screen, self.color, (self.x+1, self.y+1, self.value * (self.width - 2), self.height - 2))

class HealthBar (StatBar):
	def __init__(self, mob):
		self.width = 20
		self.height = 7
		self.color = (255,0,0)
		self.x, self.y = (mob.x - mob.RAD, mob.y - mob.RAD)
		self.value = (mob.HP / float(mob.max_health))

	def update(self, mob):
		self.x, self.y = (mob.x- mob.RAD, mob.y - mob.RAD)
		self.value = (mob.HP / float(mob.max_health))

class MobInfo:
	font = None
	COLOR = (0,0,0)
	def __init__(self, mob_array):
