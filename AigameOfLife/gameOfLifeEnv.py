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

  def __init__(self, xdim, ydim):
    self.field = gameOfLife.matchFieldPy(xdim, ydim)
    self.field.zeroMatchFieldPy()

    self._action_spec = array_spec.BoundedArraySpec(shape=(xdim,ydim), dtype=np.float32, minimum=0, maximum=1, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(shape=(xdim,ydim), dtype=np.float32, minimum=0, maximum=1, name='observation')

    self._state = self.field.fieldMatrix
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self.field.resetGamePy()
    self._episode_ended = False
    return ts.restart(np.array(self._state, dtype=np.float32))

  def _step(self, action):
    if self._episode_ended:
      return self.reset()
    self.field.simpleComplexity = 0

    # implicitly casting between uint8 and float32
    self.field.fieldMatrix = action.astype(np.uint8)
    self.field.applyIterationPy()
    self._state = self.field.fieldMatrix.astype(np.float32)

    # print(action)
    # print(self.field.simpleComplexity)

    if self._episode_ended:
      return ts.termination(self._state, self.field.simpleComplexity)
    else:
      return ts.transition(self._state, reward=self.field.simpleComplexity)
