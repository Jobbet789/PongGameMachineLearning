import pygame

class MiddleLine:
	def __init__(self, Window):
		self.color = (255, 255, 255)
		self.width = 20
		self.points = []

		self.gap = 40
		length = 40

		totalLength = Window.WIN_HEIGHT

		dashes = totalLength / (self.gap + length)

		self.dash = []
		lastEnd = 0
		for i in range(int(dashes)):
			# append points with all the lines
			self.points.append((Window.WIN_WIDTH / 2, lastEnd))
			self.points.append((Window.WIN_WIDTH / 2, lastEnd + length))

			lastEnd = lastEnd + self.gap + length



	def draw(self, win):
		# for every 2 points, draw a line
		for i in range(0, len(self.points), 2):
			pygame.draw.line(win, self.color, [self.points[i][0], self.points[i][1]+self.gap/2], [self.points[i + 1][0], self.points[i + 1][1] + self.gap/2], self.width)
