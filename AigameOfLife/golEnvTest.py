import tensorflow as tf
import numpy as np

from tf_agents.environments import utils

from gameOfLifeEnv import GolEnv

environment = GolEnv(10,10)
utils.validate_py_environment(environment, episodes=5)
