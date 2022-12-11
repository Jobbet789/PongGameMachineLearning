`networkWithoutEnemyBot` Class
==============================

Description
-----------

The `networkWithoutEnemyBot` class is a class that handles a network of neural networks for a game with no enemy bot.

Arguments
---------

The `networkWithoutEnemyBot` class takes the following arguments:

*   `genomes`: A list of genomes used to create the neural networks.
*   `config`: A `neat` configuration object used to configure the neural networks.
*   `bots`: A list of bots in the game.
*   `balls`: A list of balls in the game.

Attributes
----------

The `networkWithoutEnemyBot` class has the following attributes:

*   `bots`: A list of bots in the game.
*   `balls`: A list of balls in the game.
*   `genomes`: A list of genomes used to create the neural networks.
*   `config`: A `neat` configuration object used to configure the neural networks.
*   `generation`: The generation number of the networks.
*   `nets`: A list of neural networks created from the genomes.
*   `ge`: A list of genomes.

Methods
-------

The `networkWithoutEnemyBot` class has the following methods:

*   `get_output`: This method takes a `Window` object as input and returns a list of outputs from the neural networks. It calculates the output of each neural network by activating it with inputs derived from the `bots`, `balls`, and `Window` objects. It also increments the `generation` attribute by 1.

Example
-------

Here is an example of how to use the `networkWithoutEnemyBot` class:
``` python

import neat

# Create a networkWithoutEnemyBot object
nw = networkWithoutEnemyBot(genomes, config, bots, balls)

# Get the outputs from the neural networks
outputs = nw.get_output(Window)

```
