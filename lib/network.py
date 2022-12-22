import neat
import pickle
from lib import bat
from lib import pingPongBall


class Network: # Class for the network
    def __init__(self, 
                config_path: str, # path to the config file
                save_path: str, # path to the save file
                Window: object,
                saved_path: str = None):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path) # Load configuration.

        self.save_path = save_path # Path to save the network
        self.saved_path = saved_path # Path to load the network

        self.p = neat.Population(self.config) # Create the population, which is the top-level object for a NEAT run.
        self.p.add_reporter(neat.StdOutReporter(True)) # Add a stdout reporter to show progress in the terminal.
        self.stats = neat.StatisticsReporter() # Add a statistics reporter to show progress in the terminal.
        self.p.add_reporter(self.stats)

        self.Window = Window # Window object


    def save_winner(self, winner: neat.Checkpointer): # Save the winner

        with open(self.save_path, 'wb') as f: # Open the file
            pickle.dump(winner, f) # Dump the winner


    def load_winner(self) -> neat.nn.FeedForwardNetwork: # Load the winner
        with open(self.saved_path, 'rb') as f: # Open the file
            winner = pickle.load(f) # Load the winner

        net = neat.nn.FeedForwardNetwork.create(winner, self.config) # Create the network

        return net # Return the network
    
    def setupNNetwork(self, genomes, config) -> dict: # Setup the network
        bots = [] # Create a list for the bots
        balls = [] # Create a list for the balls
        nets = [] # Create a list for the nets
        ge = [] # Create a list for the genomes

        for _, g in genomes: # Loop through the genomes
            net = neat.nn.FeedForwardNetwork.create(g, config) # Create the network
            nets.append(net) # Append the network to the list
            bots.append(bat.Bat(self.Window.WIN_HEIGHT, True)) # Append the bot to the list
            bots[-1].init((self.Window.WIN_WIDTH - bots[-1].WIDTH - 50), (self.Window.WIN_HEIGHT / 2 - bots[-1].HEIGHT / 2)) # init the bot object
            balls.append(pingPongBall.PingPongBall((self.Window.WIN_WIDTH, self.Window.WIN_HEIGHT))) # make a ball object for the network
            g.fitness = 0 # Set the fitness to 0
            ge.append(g) # Append the genome to the list

        return {'bots': bots, 'balls': balls, 'nets': nets, 'ge': ge} # Return the lists

    def gameLoop(self, lists: dict): # Game loop DONT USE THIS!!!!@@@!
        time = 0 # Set time to 0
        time += 1/60 # Add 1/60 to time

        if self.checkForEndgen(lists['bots']): # If there are no bots left
            # end the generation
            run = False

        for x, bot in enumerate(lists['bots']): # loop through the bots
            output = self.getOutput(lists['nets'][x], bot, lists['balls'][x]) # Get the output from the network
            self.setDirectionOfBot(bot, output) # Set the direction of the bot

    def checkForEndgen(self, bots: list, time: int) -> bool: 
        # a function that checks for the end of the generation
        if len(bots) == 0 or time >= 90: # If there are no bots left
            return True # Return True
        return False # else, return false
    
    def getOutput(self, net: neat.nn.FeedForwardNetwork, bot: object, ball: object) -> list:
        # get the output of the network
        output = net.activate([bot.y,
                               ball.y,
                               bot.x - ball.x,
                               ball.direction]) # Get the output from the network
        return output # returning the output list

    def setDirectionOfBot(self, bot: object, output: list): # Set the direction of the bot
        if output[0] > 0.5: # If the output is greater than 0.5
            bot.direction = -1 # Set the direction to -1
        elif output[1] > 0.5: # If the output is greater than 0.5
            bot.direction = 1 # Set the direction to 1
        else: # If the output is not greater than 0.5
            bot.direction = 0 # set the direction to 0, which means it's not moving





    def __call__(self) -> None:
        print("A network Object has been created")

    def __repr__(self) -> str:
        return f"Network Object, save_path: {self.save_path}, saved_path: {self.saved_path}"






