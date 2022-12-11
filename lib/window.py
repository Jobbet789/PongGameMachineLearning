import pygame
import os

class Window:
	pygame.font.init()
	STAT_FONT = pygame.font.SysFont('comicsans', 50)

	WIN_WIDTH = 1100
	WIN_HEIGHT = 900

	def __init__(self):
		# self.ballImg = pygame.transform.scale2x(pygame.image.load(ballImgLoc))
		# self.batImg = pygame.transform.scale2x(pygame.image.load(batImgLoc))

		# self.bgImg = pygame.transform.scale2x(pygame.image.load(bgImgLoc))
		pass

	def draw_window(self, win, balls, bats, gen, time, MiddleLine):
		pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, self.WIN_WIDTH, self.WIN_HEIGHT))
		MiddleLine.draw(win)

		for bat in bats:
			bat.draw(win)
		for ball in balls:	
			ball.draw(win)
		
		# check if this is not training
		if gen == -1:
			# draw the score
			text = self.STAT_FONT.render("Score: " + str(bats[0].score), 1, (255, 255, 255))
			win.blit(text, (100, 10))
			
			text = self.STAT_FONT.render("Score: " + str(bats[1].score), 1, (255, 255, 255))
			win.blit(text, (self.WIN_WIDTH - text.get_width() - 100, 10))
	


		# check if this is training
		else:
			# draw the generator
			text = self.STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
			win.blit(text, (100, 10))

			# draw the amount of balls
			text = self.STAT_FONT.render("Alive: " + str(len(balls)), 1, (255, 255, 255))
			win.blit(text, (100, 50))

			#draw the time
			text = self.STAT_FONT.render("Time: " + str(int(time)), 1, (255, 255, 255))
			win.blit(text, (100, 90))



		pygame.display.update()

	def setup(self):
		return pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
