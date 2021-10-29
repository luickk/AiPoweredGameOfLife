# Ai Powered Game Of Life

The goal of the project is create a neural net which trains on finding most "creative" form of life.
The idea is to iterate over different fitness parameters to find the most interesting form of autonomous life.

Intersting parameters:
- Kolmogorov complexity <br>
The Kolmogorov complexity parameter represents the amounts of operations (rules) applied per game.
It represents the [Kolmogorov complexity](https://en.wikipedia.org/wiki/Kolmogorov_complexity) for a certain match field.
Maximizing for this parameter probably equals in an absolutely chaotic system since only increasing the complexity is not really helpfull to find stable life.

- Entropy // todo <br>
The entropy parameter returns the entropy of a match field.
The calculations for the entropy are taken from [this](https://www-users.cs.york.ac.uk/kazakov/papers/aamas-paper.pdf) paper and can be found at chapter 4 "Entropy Based Fitness of Cellular Automata".
As mentioned in the paper its advantage is that this parameter is great to find "stable" life forms since reduced entropy equals a higher amount of order.

- Algorithmic Specified Complexity in the Game of Life //todo
> "Algorithmic specified complexity (ASC) measures the degree to which an object is meaningful [...]"
> -Abstract from the [Paper](https://robertmarks.org/REPRINTS/2015_AlgorithmicSpecifiedComplexityInTheGameOfLife.pdf)

This parameter seems to be really promising since it considers important patterns & complexity and thus seems to be the better version of the Kolmogorov parameter.

## Lib Game Of Life

Path: `libGameOfLife/` <br>
It is a static C lib which contains the game of life which then can easily be used as training environment for the reinforcement learning.
The parameter calculation is also implemented here.

## Reinforcement learning // todo

## libGameOfLife Cython wrapper

Path: `AiGameOfLife/Cython` <br>

In order to train fast the game of life is not implemented in python but instead in C. The cython wrapper is very easy to use and leverages the c performance increase.
Please don't use any python functions in the training loop (not even print) since this will dramatically alter the game of life speed.
