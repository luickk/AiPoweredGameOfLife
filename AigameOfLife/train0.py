# coding=utf-8
# Copyright 2020 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python2, python3
r"""Train and Eval DDPG.

To run:

```bash
tensorboard --logdir $HOME/tmp/ddpg/gym/HalfCheetah-v2/ --port 2223 &

python tf_agents/agents/ddpg/examples/v2/train_eval.py \
  --root_dir=$HOME/tmp/ddpg/gym/HalfCheetah-v2/ \
  --num_iterations=2000000 \
  --alsologtostderr
```
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import os
import time

from absl import app
from absl import flags
from absl import logging

import gin
from six.moves import range
import tensorflow as tf  # pylint: disable=g-explicit-tensorflow-version-import

from gameOfLifeEnv import GolEnv

from tf_agents.agents.ddpg import ddpg_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import parallel_py_environment
from tf_agents.environments import suite_mujoco
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.keras_layers import inner_reshape
from tf_agents.metrics import tf_metrics
from tf_agents.networks import nest_map
from tf_agents.networks import sequential
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common

def main():
  tf.compat.v1.enable_v2_behavior()
  logging.set_verbosity(logging.INFO)
  train_eval()

def train_eval(
    root_dir="tensLogData/",
    golMatchFieldDims=(12,12),
    num_iterations=2000000,
    # Params for collect
    initial_collect_steps=1000,
    collect_steps_per_iteration=1,
    num_parallel_environments=1,
    replay_buffer_capacity=100000,
    ou_stddev=0.2,
    ou_damping=0.15,
    # Params for target update
    target_update_tau=0.05,
    target_update_period=5,
    # Params for train
    train_steps_per_iteration=1,
    batch_size=64,
    actor_learning_rate=1e-4,
    critic_learning_rate=1e-3,
    actor_fc_layers=(400, 300),
    critic_obs_fc_layers=(400,),
    critic_action_fc_layers=None,
    critic_joint_fc_layers=(300,),
    dqda_clipping=None,
    td_errors_loss_fn=tf.compat.v1.losses.huber_loss,
    gamma=0.995,
    reward_scale_factor=1.0,
    gradient_clipping=None,
    use_tf_functions=True,
    # Params for eval
    num_eval_episodes=10,
    eval_interval=10000):


    global_step = tf.compat.v1.train.get_or_create_global_step()

    tf_env = tf_py_environment.TFPyEnvironment(GolEnv(golMatchFieldDims[0],golMatchFieldDims[1]))

    actor_net = create_actor_network(actor_fc_layers, tf_env.action_spec(), golMatchFieldDims)
    critic_net = create_critic_network(critic_obs_fc_layers,
                                       critic_action_fc_layers,
                                       critic_joint_fc_layers)


    print(tf_env.action_spec().shape)

    tf_agent = ddpg_agent.DdpgAgent(
        tf_env.time_step_spec(),
        tf_env.action_spec(),
        actor_network=actor_net,
        critic_network=critic_net,
        actor_optimizer=tf.compat.v1.train.AdamOptimizer(
            learning_rate=actor_learning_rate),
        critic_optimizer=tf.compat.v1.train.AdamOptimizer(
            learning_rate=critic_learning_rate),
        ou_stddev=ou_stddev,
        ou_damping=ou_damping,
        target_update_tau=target_update_tau,
        target_update_period=target_update_period,
        dqda_clipping=dqda_clipping,
        td_errors_loss_fn=td_errors_loss_fn,
        gamma=gamma,
        reward_scale_factor=reward_scale_factor,
        gradient_clipping=gradient_clipping,
        train_step_counter=global_step)
    tf_agent.initialize()

    eval_policy = tf_agent.policy
    collect_policy = tf_agent.collect_policy

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        tf_agent.collect_data_spec,
        batch_size=tf_env.batch_size,
        max_length=replay_buffer_capacity)

    initial_collect_driver = dynamic_step_driver.DynamicStepDriver(
        tf_env,
        collect_policy,
        observers=[replay_buffer.add_batch],
        num_steps=initial_collect_steps)

    collect_driver = dynamic_step_driver.DynamicStepDriver(
        tf_env,
        collect_policy,
        observers=[replay_buffer.add_batch],
        num_steps=collect_steps_per_iteration)

    # Collect initial replay data.
    logging.info(
        'Initializing replay buffer by collecting experience for %d steps with '
        'a random policy.', initial_collect_steps)
    initial_collect_driver.run()

    time_step = None
    policy_state = collect_policy.get_initial_state(tf_env.batch_size)

    time_acc = 0

    # Dataset generates trajectories with shape [Bx2x...]
    dataset = replay_buffer.as_dataset(
        num_parallel_calls=3,
        sample_batch_size=batch_size,
        num_steps=2).prefetch(3)
    iterator = iter(dataset)

    def train_step():
      experience, _ = next(iterator)
      return tf_agent.train(experience)

    if use_tf_functions:
      train_step = common.function(train_step)

    for _ in range(num_iterations):
      start_time = time.time()
      time_step, policy_state = collect_driver.run(
          time_step=time_step,
          policy_state=policy_state,
      )
      for _ in range(train_steps_per_iteration):
        train_loss = train_step()
      time_acc += time.time() - start_time

    return train_loss


dense = functools.partial(
    tf.keras.layers.Dense,
    activation=tf.keras.activations.relu,
    kernel_initializer=tf.compat.v1.variance_scaling_initializer(
        scale=1./ 3.0, mode='fan_in', distribution='uniform'))


def create_identity_layer():
  return tf.keras.layers.Lambda(lambda x: x)


def create_fc_network(layer_units):
  return sequential.Sequential([dense(num_units) for num_units in layer_units])


def create_actor_network(fc_layer_units, action_spec, golMatchFieldDims):
  """Create an actor network for DDPG."""
  flat_action_spec = tf.nest.flatten(action_spec)
  if len(flat_action_spec) > 1:
    raise ValueError('Only a single action tensor is supported by this network')
  flat_action_spec = flat_action_spec[0]

  fc_layers = [dense(num_units) for num_units in fc_layer_units]

  num_actions = flat_action_spec.shape.num_elements()
  action_fc_layer = tf.keras.layers.Dense(
      num_actions,
      activation=tf.keras.activations.tanh,
      kernel_initializer=tf.keras.initializers.RandomUniform(
          minval=-0.003, maxval=0.003))

  scaling_layer = tf.keras.layers.Lambda(
      lambda x: common.scale_to_spec(x, flat_action_spec))
  return sequential.Sequential(fc_layers + [action_fc_layer, scaling_layer])


def create_critic_network(obs_fc_layer_units,
                          action_fc_layer_units,
                          joint_fc_layer_units):
  """Create a critic network for DDPG."""

  def split_inputs(inputs):
    return {'observation': inputs[0], 'action': inputs[1]}

  obs_network = create_fc_network(
      obs_fc_layer_units) if obs_fc_layer_units else create_identity_layer()
  action_network = create_fc_network(
      action_fc_layer_units
  ) if action_fc_layer_units else create_identity_layer()
  joint_network = create_fc_network(
      joint_fc_layer_units) if joint_fc_layer_units else create_identity_layer(
      )
  value_fc_layer = tf.keras.layers.Dense(
      1,
      activation=None,
      kernel_initializer=tf.keras.initializers.RandomUniform(
          minval=-0.003, maxval=0.003))

  return sequential.Sequential([
      tf.keras.layers.Lambda(split_inputs),
      nest_map.NestMap({
          'observation': obs_network,
          'action': action_network
      }),
      nest_map.NestFlatten(),
      tf.keras.layers.Concatenate(),
      joint_network,
      value_fc_layer,
      inner_reshape.InnerReshape([1], [])
  ])

if __name__ == '__main__':
  main()
