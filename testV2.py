import neat
import pickle
import pygame

from lib import window
from lib import middleLine
from lib import pingPongBall
from lib import bat
from lib import network
# winner file name
winnerFile = 'assets/winner.pkl'
# config file name
configFile = "assets/config-feedforward.txt"


# creating objects
Window = window.Window() # Window object

MiddleLine = middleLine.MiddleLine(Window) # Middle Line object

Network = network.Network(configFile, winnerFile, Window)

generation = -1

fps = 60


def trainBot(genomes, config):
    global generation
    generation += 1
    time = 0
    # setting up the game
    win = Window.setup() # setting up the window
    run = True # game loop
    clock = pygame.time.Clock() # clock object

    # Creating the left WALL
    BatLeft = bat.Bat(Window.WIN_HEIGHT, False) # left bat object
    BatLeft.init((50), (Window.WIN_HEIGHT / 2 - BatLeft.HEIGHT / 2)) # initializing the bat
    BatLeft.HEIGHT = Window.WIN_HEIGHT # setting the bat's height to the window's height

    generationDict = Network.setupNNetwork(genomes, config)

    # creating the generation's lists
    bots = generationDict['bots']
    nets = generationDict['nets']
    ge = generationDict['ge']
    balls = generationDict['balls']

    while run:
        #clock.tick(fps) # setting the clock to 60 fps
        time += 1/fps # adding the time in seconds

        # check for end gen
        if Network.checkForEndgen(bots, time):
            run = False
            break

        # checking for events
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # if the user clicks the close button
                run = False # stop the game loop
                pygame.quit() # quit pygame
                break # break the loop

        for x, bot in enumerate(bots):
            # geting the output
            output = Network.getOutput(nets[x], bot, balls[x])
            # moving the bot
            Network.setDirectionOfBot(bot, output)

            balls[x].move() # moving the ball
            if balls[x].bounce(): # if the ball bounces
                ge[x].fitness += 1 # add 1 to the fitness

            # checking for collision
            if balls[x].collide_with_paddles([BatLeft, bot]):
                ge[x].fitness += 4 # add 4 to the fitness

            # scores
            edge = balls[x].isTouchingLeftOrRightEdge()
            if edge:
                if edge == 'left':
                    ge[x].fitness += 1
                    bot.score += 1
                    balls[x].reset()
                else:
                    ge[x].fitness -= 1
                    balls[x].reset()
                    bot.score -= 1

            # check for termination
            if bot.score <= -10: # if the bot's score is less than or equal to -10
                ge[x].fitness -= 10 # subtract 10 from the fitness
                # remove the bot from the list
                nets.pop(x)
                ge.pop(x)
                bots.pop(x)
                balls.pop(x)

            elif bot.score >= 10: # if the bot's score is greater than or equal to 10
                ge[x].fitness += 10 # add 10 to the fitness
                # remove the bot from the list
                nets.pop(x)
                ge.pop(x)
                bots.pop(x)
                balls.pop(x)

            bot.move() # moving the bot

        BatLeft.y = 0 # setting the bat's y to 0

        # drawing the objects
        Window.draw_window(win, balls, [BatLeft, *bots], generation, time, MiddleLine)


def run():
    winner = Network.p.run(trainBot, 50)
    Network.saveWinner(winner)


if __name__ == '__main__':
    run()

