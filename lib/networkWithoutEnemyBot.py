# A class that handles the network without enemy bot
import neat

class networkWithoutEnemyBot:
	def __init__(self, genomes: list, config, bots: list, balls: list):
		# arguments for the class 
		self.bots = bots # list of bots
		self.balls = balls # list of balls
		self.genomes = genomes # list of genomes
		self.config = config # neat configuration

		self.generation = -1 # generation number


		
		self.nets: list = [] # list of neural networks
		self.ge: list = [] # list of genomes
		
		for _, g in self.genomes: # for each genome
			net = neat.nn.FeedForwardNetwork.create(g, self.config) # Create the network
			self.nets.append(net) # add the network to the list

			g.fitness = 0 # start with fitness level of 0
			self.ge.append(g) # Add genome to list of genomes


	def get_output(self, Window) -> list: # get the output of the neural network
		self.generation += 1 # increase the generation number

		outputs: list = [] # list of outputs
		for x, net in enumerate(self.nets): # for each network
			# get the output of the network
			output: list = net.activate([self.bots[x].y - self.balls[x].y, 
						  self.bots[x].x - self.balls[x].x,
						  self.balls[x].direction]) 
			
			outputs.append(output) # add the output list to the list of outputs

		return outputs # return the list of outputs

			
