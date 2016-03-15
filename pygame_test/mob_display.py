import pygame
from grid import *
from mob import *
import random

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
		self.value = (mob.hp / float(mob.max_health))

	def update(self, mob):
		self.x, self.y = (mob.x- mob.RAD, mob.y - mob.RAD)
		self.value = (mob.hp / float(mob.max_health))

class MobInfo:
	font = None
	FONTCOLOR = (0,0,0)
	HEIGHT = 80
	WIDTH = 90
	STATS = ["SP", "HP", "ND", "FD", "MD"]
	def __init__(self, loc, mob_array, mob_color, dist):
		if not MobInfo.font:
			MobInfo.font = pygame.font.SysFont("monospace", 16)
		self.mob_array = mob_array
		self.x,self.y = loc
		self.mob_color = mob_color
		self.mob_dist = dist
		self.stat_bars = []
		x,y = (30,5)
		for m in self.mob_array:
			self.stat_bars.append(StatBar((255,0,0), m, (self.x + x, self.y + y), 28, 10))
			y += 15

	def draw(self, screen):
		pygame.draw.rect(screen, (0,0,0), (self.x, self.y, MobInfo.WIDTH, MobInfo.HEIGHT))
		pygame.draw.rect(screen, (255,255,255), (self.x + 1, self.y + 1, MobInfo.WIDTH - 1, MobInfo.HEIGHT - 1))
		for i,st in enumerate(self.stat_bars):
			label = MobInfo.font.render(MobInfo.STATS[i], 1, MobInfo.FONTCOLOR)
			location = (st.x - 28, st.y - 3)
			screen.blit(label, location)
			st.draw(screen)
		pygame.draw.circle(screen, self.mob_color, (self.x + 75, self.y + self.HEIGHT/2), 10)
		label = MobInfo.font.render(str(self.mob_dist), 1, (0,0,0))
		screen.blit(label, (self.x + 70, self.y + self.HEIGHT/2 + 20))

class MobInfoPanel:
	def __init__(self, loc):
		self.x, self.y = loc
		self.mob_panels = []

	def update (self, moblist):
		self.mob_panels = []
		for i,m in enumerate(moblist):
			self.mob_panels.append(MobInfo((self.x, i * MobInfo.HEIGHT), m.statArray, (255,0,0), m.distance_traveled))

	def draw (self, screen):
		for m in self.mob_panels:
			m.draw(screen)
