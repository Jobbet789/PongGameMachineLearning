class networkWithoutEnemyBot:
	def __init__(self, genomes: list, config, bots: list, balls: list):
		# arguments for the class 
		self.bots = bots # list of bots
		self.balls = balls # list of balls
		self.genomes = genomes # list of genomes
		self.config = config # neat configuration


		
		self.nets: list = [] # list of neural networks
		self.ge: list = [] # list of genomes
		
		for _, g in self.genomes: # for each genome
			net = neat.nn.FeedForwardNetwork.create(g, self.config) # Create the network
			self.nets.append(net) # add the network to the list

			g.fitness = 0 # start with fitness level of 0
			self.ge.append(g) # Add genome to list of genomes


	def get_output(self) -> list:
		# get the output of the neural network
		outputs: list = []
		for x, net in enumerate(self.nets):

			
