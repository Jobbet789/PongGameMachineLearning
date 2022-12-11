import pygame, random, math

# Define ping pong ball class
class PingPongBall:
    # Define constructor
	SIZE = 10
	WIDTH = SIZE
	HEIGHT = SIZE
	once = False

	def __init__(self, WINDIM: list):
		# place the ball at the middle of the screen
		self.x = WINDIM[0]/2 
		self.y = WINDIM[1]/2

		self.WINDIM = WINDIM # store the window dimensions

		# set the starting velocity
		# vector = (x2 - x1, y2 - y1)
		# (1, 0) = (x2 - 50, y2 - 50)
		
		# set the starting direction
		# 0 = right, 90 = down, 180 = left, 270 = up
		# the ball goes to the left or the right at random
		# the direction changes +- 45 degrees
		firstball = random.choice([0, 180])
		self.direction = firstball + random.randint(-45, 45)
		if firstball == 0:
			self.x -= WINDIM[0]/3
		else:
			self.x += WINDIM[0]/3


		self.vel = 7 # this is just a random value, change it later to the actual value

	def move(self): # move the ball 
		# Calculate the velocity vector using the direction and velocity
		velocity = Vector2(math.cos(math.radians(self.direction)), math.sin(math.radians(self.direction)))
		velocity *= self.vel

	    # Add the velocity vector to the position vector to get the new position
		self.x += velocity.x
		self.y += velocity.y

	def bounce(self):
		# Check if the ball is touching the top or bottom edge of the screen
		if self.y <= 0 or self.y + self.HEIGHT >= self.WINDIM[1]:
			# Flip the direction of the ball vertically
			self.direction = 360 - self.direction
		if self.direction < 270 and self.direction > 90:
			return True
		else:
			return False

	# a function to check if the ball is touching the left or right edge of the screen
	def isTouchingLeftOrRightEdge(self):
		if self.x <= 0:
			return "left"
		elif self.x + self.WIDTH >= self.WINDIM[0]:
			return "right"
		else:
			return False

	def collide_with_paddles(self, paddles):
		forgiveness = 5 # the amount of forgiveness for the collision

	    # Check if the ball is touching any of the paddles
		for paddle in paddles:

			if (
				self.x >= paddle.x and self.x + self.WIDTH <= paddle.x + paddle.WIDTH
				and self.y + forgiveness >= paddle.y and self.y - self.HEIGHT - forgiveness <= paddle.y + paddle.HEIGHT
			):
				# Calculate the relative position of the ball within the paddle
				relative_position = (self.y + self.HEIGHT / 2) - (paddle.y + paddle.HEIGHT / 2)
				

				# check if the paddle is very large (i.e. the wall)
				if paddle.HEIGHT >= 200:
					# if the paddle is the wall, then the ball will bounce off and add a random value between -45 and 45 to the direction
					self.direction = 0 + random.randint(-45, 45)
					return False



				if paddle.side:

					# Adjust the direction of the ball based on where it hits the paddle
					self.direction = (relative_position / paddle.HEIGHT) * 120 + 180
					self.vel = 10
					return True
				else:
					# Adjust the direction of the ball based on where it hits the paddle
					self.direction = -(relative_position / paddle.HEIGHT) * 120
					self.vel = 10
					return False

	def reset(self): # Reset the ball to the center of the screen
		self.__init__(self.WINDIM)



	def draw(self, win): # draw the ball on the window
		pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT))


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)
