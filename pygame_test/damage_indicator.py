import pygame

class DamageIndicator:
	font = None
	COLOR = (60,0,0)
	def __init__(self, damage):
		if not DamageIndicator.font:
			DamageIndicator.font = pygame.font.SysFont("monospace", 32)
		self.damage = damage
		self.offset_y = -10
		self.label = DamageIndicator.font.render(str(damage), 1, DamageIndicator.COLOR)

	def draw(self, screen, mob):
		if self.offset_y < -40: return 0
		location = (mob.x - mob.RAD, mob.y + self.offset_y)
		self.offset_y -= 2
		screen.blit(self.label, location)
		return 1
