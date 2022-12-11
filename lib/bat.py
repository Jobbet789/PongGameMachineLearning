import pygame

class Bat:
	WIDTH = 20
	HEIGHT = 80
	def __init__(self, WINHEIGHT, side):
		# random velocity, change this later
		self.vel = 0
		self.speed = 7
		self.direction = 0

		self.side = side

		self.WINHEIGHT = WINHEIGHT

		self.score = 0

	def init(self, startX, startY):
		self.x = startX
		self.y = startY

	def move(self):
		self.vel = self.speed*self.direction

		self.y += self.vel

		self.y = max(0, min(self.y, self.WINHEIGHT - self.HEIGHT))

	def draw(self, win):
		pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT))




