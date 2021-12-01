import tensorflow as tf
import numpy as np
import sys
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

    def __init__(self, xdim, ydim, nIterations, earlyEvolutionPenalty, fitnessParameter="simpleComplexity"):
        self.field = gameOfLife.matchFieldPy(xdim, ydim)
        self.field.zeroMatchFieldPy()
        self.nIteration = nIterations
        self.earlyEvolutionPenalty = earlyEvolutionPenalty

        self._action_spec = array_spec.BoundedArraySpec(shape=(xdim,ydim), dtype=np.float32, minimum=0, maximum=1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(xdim,ydim), dtype=np.float32, minimum=0, maximum=1, name='observation')

        self._state = self.field.fieldMatrix
        self.fitnessParameter = fitnessParameter
        self._episode_ended = False
        self.lastReward = 0

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

        rewardArr = np.ones(shape=(self.nIteration))

        # TODO: PERFOMANCE OPTIMISATIONS
        # implicitly casting between uint8 and float32
        self.field.fieldMatrix = np.around(action).astype(np.uint8)
        for i in range(self.nIteration):
            self.field.simpleComplexity = 0
            self.field.applyIterationPy()
            self.field.calcEntropyPy(i)
            if self.fitnessParameter == "simpleComplexity":
                rewardArr[i] = self.field.simpleComplexity
            elif self.fitnessParameter == "entropy":
                if not np.isinf(self.field.entropy):
                    rewardArr[i] = self.field.entropy
                elif np.isinf(self.field.entropy):
                    rewardArr[i] = 0

        self._state = self.field.fieldMatrix.astype(np.float32)

        if self._episode_ended:
            return ts.termination(self._state, self.field.simpleComplexity)
        else:
            reward = np.average(rewardArr) - self.calcDifferenceSumAvg(rewardArr)
            return ts.transition(self._state, reward=reward, discount=1)

    def calcDifferenceSumAvg(self, arr):
        # by https://www.geeksforgeeks.org/sum-absolute-differences-pairs-given-array/
        sum = 0
        n = len(arr)
        for i in range(n - 1, -1, -1):
            sum += i*arr[i] - (n-1-i) * arr[i]
            if i != 0:
                sum += self.earlyEvolutionPenalty/i
        return sum/n
