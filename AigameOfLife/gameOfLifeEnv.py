import tensorflow as tf
import numpy as np
from Cython import gameOfLife

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

class GolEnv(py_environment.PyEnvironment):

  def __init__(self):
    self.field = gameOfLife.matchFieldPy(10, 10)
    self.field.zeroMatchFieldPy()

    self._action_spec = array_spec.BoundedArraySpec(shape=(10,10), dtype=np.uint8, minimum=0, maximum=1, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(shape=(10,10), dtype=np.uint8, minimum=0, maximum=1, name='observation')

    self._state = self.field.fieldMatrix
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self.field.resetGamePy()
    self._episode_ended = False
    return ts.restart(np.array(self._state, dtype=np.uint8))

  def _step(self, action):
    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()
    self.field.simpleComplexity = 0

    self.field.fieldMatrix = action
    self.field.applyIterationPy()
    self._state = self.field.fieldMatrix

    print(action)
    print(self.field.simpleComplexity)

    if self._episode_ended:
      return ts.termination(self._state, self.field.simpleComplexity)
    else:
      return ts.transition(self._state, reward=self.field.simpleComplexity)
