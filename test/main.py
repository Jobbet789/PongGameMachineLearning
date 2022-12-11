# import modules
import pygame
import neat
import pickle

# importing from /lib
from lib import window
from lib import bat
from lib import pingPongBall
from lib import middleLine

# winner file name
winnerFile = "winner.pkl"
# config file
config_path = "config-feedforward.txt"


# creating objects
Window = window.Window() # Creating window object

# creating Bat objects
BatLeft = bat.Bat(Window.WIN_HEIGHT, False)
BatLeft.init((50), (Window.WIN_HEIGHT/2-BatLeft.HEIGHT/2)) # initializing bat object

BatLeft.HEIGHT = Window.WIN_HEIGHT

generation = -1

MiddleLine = middleLine.MiddleLine(Window) # Middle Line object



def trainBotWithoutEnemyBot(genomes, config):
	global generation
	generation += 1
	time = 0
	# setting up the game
	win = Window.setup() # setting up the window
	run = True # game loop variable
	clock = pygame.time.Clock() # clock for the game loop

	# creating the neural network
	bots = []
	balls = []
	nets = []
	ge = []

	BatLeft.HEIGHT = Window.WIN_HEIGHT

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		bots.append(bat.Bat(Window.WIN_HEIGHT, True))
		bots[-1].init((Window.WIN_WIDTH - bots[-1].WIDTH - 50), (Window.WIN_HEIGHT/2-bots[-1].HEIGHT/2))
		balls.append(pingPongBall.PingPongBall((Window.WIN_WIDTH, Window.WIN_HEIGHT)))
		g.fitness = 0
		ge.append(g)
	
	# game loop
	while run:
		#clock.tick(30)
		time += 1/30/60

		if len(bots) == 0:
			run = False
			break
		# event handling
		for event in pygame.event.get():

			# quit game
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()



		for x, bot in enumerate(bots):
			bot.move()
			ge[x].fitness += 0.05
			output = nets[x].activate([bot.y - balls[x].y, bot.x - balls[x].x, Window.WIN_HEIGHT, Window.WIN_WIDTH])

			bot.direction = 0

			if output[0] > 0.5:
				bot.direction = -1

			if output[1] > 0.5:
				bot.direction = 1

			balls[x].move()
			if balls[x].bounce():
				ge[x].fitness += 1




		for x, bot in enumerate(bots):
			if balls[x].collide_with_paddles([BatLeft, bot]):
				ge[x].fitness += 4

		BatLeft.y = 0

		if time >= 20:
			run = False
			return

		# Call draw functions
		if generation >= 1000:
			Window.draw_window(win, balls, [BatLeft, *bots], generation, time, MiddleLine)

		# Check for scores
		for x, ball in enumerate(balls):
			edge = ball.isTouchingLeftOrRightEdge()
			if edge:
				if edge == "left":
						bots[x].score += 1
						ge[x].fitness += 1
						balls[x].reset()
				else:
					ge[x].fitness -= 10
					bots.pop(x)
					balls.pop(x)
					nets.pop(x)
					ge.pop(x)



def trainBotWithEnemyBot(genomes, config):
	# add to the generation variable every time this function is called
	global generation, netTrained
	generation += 1

	# setting up the game
	time = 0
	fps = 60
	win = Window.setup() # setting up the window
	run = True # game loop variable

	clock = pygame.time.Clock() # clock for the game loop


	# create a list of nets, genomes, bots and balls
	nets = []
	ge = []
	bots = []
	balls = []
	trainedBots = []

	for _, g in genomes: # create a bot for each genome
		# create a neural network
		net = neat.nn.FeedForwardNetwork.create(g, config)
		# add the neural network to the list
		nets.append(net)

		# create a bot
		bots.append(bat.Bat(Window.WIN_HEIGHT, True))
		# init the bot
		bots[-1].init((Window.WIN_WIDTH - bots[-1].WIDTH - 50), (Window.WIN_HEIGHT/2-bots[-1].HEIGHT/2))
		# add a ball to the list
		balls.append(pingPongBall.PingPongBall((Window.WIN_WIDTH, Window.WIN_HEIGHT)))
	
		# add an enemy bot to the list
		trainedBots.append(bat.Bat(Window.WIN_HEIGHT, False))

		# init the bot
		trainedBots[-1].init(50, (Window.WIN_HEIGHT/2-trainedBots[-1].HEIGHT/2))

		
		# set the fitness to 0
		g.fitness = 0
		# add the genome to the list
		ge.append(g)
	

	# game loop
	while run:
		# only do this if you want visuals
		# clock.tick(fps) # set the fps to 60
		time += 1/fps/60 # add to the time in minutes
		
		# check if there are no bots left
		if len(bots) == 0:
			run = False
			break

		# check for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
				break
		
		for x, bot in enumerate(bots):
			# call move function
			bot.move()
			ge[x].fitness += 0.05 # add 0.05 to the fitness of the bot every frame

			# get the output of the network in training
			outputTraining = nets[x].activate([bot.y - balls[x].y, bot.x - balls[x].x, Window.WIN_HEIGHT, Window.WIN_WIDTH])

			bot.direction = 0 

			# if the output[0] is greater than 0.5, move the bot up
			if outputTraining[0] > 0.5:
				bot.direction = -1

			# if the output[1] is greater than 0.5, move the bot down
			if outputTraining[1] > 0.5:
				bot.direction = 1

			# move the balls
			balls[x].move()
			# check if the ball bounces off the ball, and add fitness if it does
			if balls[x].bounce():
				ge[x].fitness += 1

			# move the trained bots
			trainedBots[x].move()

			# get the output of the network that is already trained
			outputTrained = netTrained.activate(
					[trainedBots[x].y - balls[x].y,
					(trainedBots[x].x + trainedBots[x].WIDTH) + (balls[x].x + balls[x].WIDTH), 
					Window.WIN_HEIGHT,
					Window.WIN_WIDTH])

			# get the direction
			trainedBots[x].direction = 0 # set the direction to 0
			# if the output[0] is greater than 0.5, move the bot up
			if outputTrained[0] > 0.5:
				trainedBots[x].direction = -1

			# if the output[1] is greater than 0.5, move the bot down
			if outputTrained[1] > 0.5:
				trainedBots[x].direction = 1


			# check if the ball collides with the paddles
			if balls[x].collide_with_paddles([trainedBots[x], bot]):
				ge[x].fitness += 4 # add 4 to the fitness of the bot if it collides with the ball


			# check for the scores
			edge = balls[x].isTouchingLeftOrRightEdge() # get the edge

			if edge: # check if it actually touches one
				if edge == "left": # if it touches the left edge, add 1 to the score of the right paddle
					bot.score += 1 # add 1 to the score of the bot
					ge[x].fitness += 1 # add 1 to the fitness of the bot
					balls[x].reset()
				else: # if it touches the right edge, the paddle is removed from the generation
					ge[x].fitness -= 10 # remove 10 from the fitness of the bot
					bots.pop(x) # remove the bot from the list
					balls.pop(x) # remove the ball from the list
					ge.pop(x) # remove the genome from the list
					nets.pop(x) # remove the network from the list
					trainedBots.pop(x) # remove the trained bot from the list




		if time >= 20: # if the time is greater than 20, end the generation
			# set the run var to false
			run = False
			return # return
		
		# draw the window with everything ontop
		if generation >= 99: # only draw the last two generations
			#Window.draw_window(win, balls, [*trainedBots, *bots], generation, time, MiddleLine) # draw the window
			pass



def run(config_path, savePath):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	
	winner = p.run(trainBotWithoutEnemyBot, 100)
	# save the winner to a file as gzip
	with open(savePath, 'wb') as f:
		pickle.dump(winner, f)


# make a function to run the winner
def run_winner(config_path, path):
	# import the winner
	with open(path, 'rb') as f:
		winner_genome = pickle.load(f)

	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)
	# create the winner's neural network
	net = neat.nn.FeedForwardNetwork.create(winner_genome, config)

	# create the game
	BatLeft = bat.Bat(Window.WIN_HEIGHT, False)
	Bot = bat.Bat(Window.WIN_HEIGHT, True)
	Ball = pingPongBall.PingPongBall((Window.WIN_WIDTH, Window.WIN_HEIGHT))


	# init paddles
	Bot.init((Window.WIN_WIDTH - Bot.WIDTH - 50), (Window.WIN_HEIGHT/2-Bot.HEIGHT/2))
	BatLeft.init(50, (Window.WIN_HEIGHT/2-BatLeft.HEIGHT/2))

	# create the clock
	clock = pygame.time.Clock()

	# create the run variable
	run = True

	# create the time variable
	time = 0
	fps = 60
	# create the window object
	win = Window.setup()
	
	# keep track of the keys pressed
	upKey = False
	downKey = False

	while run:
		# set the clock
		clock.tick(fps)
		time += 1/fps


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					BatLeft.direction = 1
					downKey = True
				elif event.key == pygame.K_w:
					BatLeft.direction = -1
					upKey = True

			if event.type == pygame.KEYUP:
				# if the key is released, stop moving
				if event.key == pygame.K_s:
					if not upKey:
						BatLeft.direction = 0
					downKey = False
				elif event.key == pygame.K_w:
					if not downKey:
						BatLeft.direction = 0
					upKey = False


		# moves
		BatLeft.move()
		
		# get the inputs of the bot

		output = net.activate([Bot.y - Ball.y, Bot.x - Ball.x, Window.WIN_HEIGHT, Window.WIN_WIDTH])

		# call move
		Bot.move()
		# set the direction of the bot
		Bot.direction = 0
		if output[0] > 0.5:
			Bot.direction = -1
		if output[1] > 0.5:
			Bot.direction = 1
	
		# call the move function of the ball
		Ball.move()
		Ball.bounce()
		
		# check for collisions with the bats
		Ball.collide_with_paddles([BatLeft, Bot])

		# check for collisions with the walls

		edge = Ball.isTouchingLeftOrRightEdge()
		if edge:
			if edge == "left":
				Bot.score += 1
			else:
				BatLeft.score += 1
			Ball.reset()

		# draw the game
		Window.draw_window(win, [Ball], [BatLeft, Bot], -1, time, MiddleLine)
	


# function to run the winner as the enemy of the new bots that are getting trained
def run_winner_against_new(config_path, winner_path, newWinner_path):
	global netTrained
	# import the winner
	with open(winner_path, 'rb') as f:
		winner = pickle.load(f)
	
	# set the config file (they are the same for both bots)
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							 neat.DefaultSpeciesSet, neat.DefaultStagnation,
							 config_path)
	# create the winners nearal network
	netTrained = neat.nn.FeedForwardNetwork.create(winner, config)

	# setup the population
	p = neat.Population(config)
	
	p.add_reporter(neat.StdOutReporter(True)) # print the stats
	stats = neat.StatisticsReporter() # get the stats
	p.add_reporter(stats) # add the stats to the population

	# run the population
	newWinner = p.run(trainBotWithEnemyBot, 100)

	# save the new winner
	with open(newWinner_path, 'wb') as f:
		pickle.dump(newWinner, f)




if __name__ == "__main__":
	#run(config_path, 'winner.pkl')
	run_winner(config_path, "winner.pkl")
	#run_winner_against_new(config_path, 'winner.pkl', 'newWinner.pkl')

	

