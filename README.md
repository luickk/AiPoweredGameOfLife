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

## Reinforcement learning

Path: `AiGameOfLife/` <br>

The reinforcement learning is realized with a [tf-agent ddpg network](https://www.tensorflow.org/agents/api_docs/python/tf_agents/agents/ddpg/actor_network/ActorNetwork). The DDPG with its GAN like Q-Function is used because its ability to explore huge continous actionsspaces. In this case the init state of a game of life.
> The main advantage is that stochastic policies ensure exploration of the state-action space [..]
>
> -- <cite>[Julien Vitay DPG](https://julien-vitay.net/deeprl/DPG.html)</cite>

## libGameOfLife Cython wrapper

Path: `AiGameOfLife/Cython` <br>

In order to train fast, the game of life is not implemented in python but instead in C. The cython wrapper is very easy to use and leverages the c performance increase.
Please don't use any python functions in the training loop (not even print) since this will dramatically alter the game of life speed.

## Network Improvement History

### First test evaluations of the project

The first few runs show several problem areas which need to be investigated.
- GAN(DDPG) reward calculation over n evolutions per gol game
  - The actor net action is the initial game of life matrix on which n gol evolution steps are performed. Thus the reward is calculated by adding up the „fitness parameters “ (the factors by which the gol game is rated. For example the simpleComplexity factor which represents the Kolmogorov complexity) per evolution every single round of gol.
  - A symptom of summing up the „fitness parameters“ for n evolutions of every gol is that the network focuses on the first(or which ever is mor efficient) evolution. The result is that the reward plateaus at a certain niveau because the network chooses the shortest path to the highest achievable reward and  does not compromise for the longevity of the factor of interest.
  - A possible solution to this problem is to calculate the “difference sum average” of the values for all evolutions. This would account for a possible focus of the network on one evolution.
