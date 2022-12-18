import pygame

class Bat: # Class for the bat
	WIDTH = 20 # the width of the bat
	HEIGHT = 80 # the height of the bat
	def __init__(self, WINHEIGHT, side): # initialize the bat
		self.vel = 0 # the real velocity
		self.speed = 7 # the velocity when moving
		self.direction = 0 # the direction of the bat (1, -1 or 0)

		self.side = side # the side of the bat (left or right)

		self.WINHEIGHT = WINHEIGHT # the height of the window

		self.score = 0 # the score of the abd

	def init(self, startX, startY): # initialize the bat
		self.x = startX # the x position of the bat
		self.y = startY # the y position of the bat

	def move(self): # move the bat
		self.vel = self.speed*self.direction # calculate the velocity

		self.y += self.vel # move the bat

		self.y = max(0, min(self.y, self.WINHEIGHT - self.HEIGHT)) # maximize and minimize the y position of the bat

	def draw(self, win): # draw the bat
		pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)) # draw the bat




