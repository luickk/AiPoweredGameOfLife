import os
import time
import tf_agents
import numpy as np
import tensorflow as tf

from gameOfLifeEnv import GolEnv

from absl import logging

from tf_agents.agents.ddpg import ddpg_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common
from tf_agents.networks import network
from tf_agents.networks import utils
from tf_agents.specs import tensor_spec

def main():
  train_eval()

def train_eval(
    golMatchFieldDims=(20, 20),
    golMatchFieldNiter=20,
    earlyEvolutionPenalty=4000,
    num_iterations=1000,
    actor_learning_rate=0.001,
    critic_learning_rate=0.001,
    initial_collect_steps=100,
    replay_buffer_capacity=100000,
    collect_steps_per_iteration=1,
    batch_size=12,
    fc_layer_params=(400,400),
    observation_fc_layer_params=(400, 400),
    # fitnessParameters available: entropy, simpleComplexity
    fitnessParameter="simpleComplexity"):

    global_step = tf.compat.v1.train.get_or_create_global_step()

    tf_env = tf_py_environment.TFPyEnvironment(GolEnv(golMatchFieldDims[0], golMatchFieldDims[1], golMatchFieldNiter, earlyEvolutionPenalty, fitnessParameter=fitnessParameter))

    actor_net = ActorNetworkCustom(tf_env.observation_spec(), tf_env.action_spec(), activation_fn=tf.nn.relu, fc_layer_params=fc_layer_params, name='ActorNetwork')

    critic_net = tf_agents.agents.ddpg.critic_network.CriticNetwork((tf_env.action_spec(), tf_env.observation_spec()), observation_fc_layer_params=observation_fc_layer_params, activation_fn=tf.nn.relu, name='CriticNetwork')

    tf_agent = ddpg_agent.DdpgAgent(
        tf_env.time_step_spec(),
        tf_env.action_spec(),
        actor_network=actor_net,
        critic_network=critic_net,
        actor_optimizer=tf.compat.v1.train.AdamOptimizer(
            learning_rate=actor_learning_rate),
        critic_optimizer=tf.compat.v1.train.AdamOptimizer(
            learning_rate=critic_learning_rate),
        train_step_counter=global_step)

    tf_agent.initialize()

    collect_policy = tf_agent.collect_policy

    # collect_policy = random_tf_policy.RandomTFPolicy(action_spec=tf_env.action_spec(), time_step_spec=tf_env.time_step_spec())

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

    # Dataset generates trajectories with shape [Bx2x...]
    dataset = replay_buffer.as_dataset(
        num_parallel_calls=1,
        sample_batch_size=1,
        num_steps=2).prefetch(3)

    iterator = iter(dataset)
    loss = []
    reward = []
    for i in range(num_iterations):
        time_step, policy_state = collect_driver.run(time_step=time_step, policy_state=policy_state)
        experience, _ = next(iterator)
        train_loss = tf_agent.train(experience)
        # print(str(i)+"-Loss: " + str(train_loss.loss.numpy()))
        print(str(i)+"-Reward: "+ str(time_step.reward.numpy()[0]))
        loss.append(train_loss.loss.numpy())
        reward.append(time_step.reward.numpy()[0])
        if i == num_iterations-1:
            est = np.around(collect_policy.action(time_step)[0].numpy()).astype(np.uint8)
            print(est)
            np.save("latestRes.npy", np.array((loss, reward, golMatchFieldDims, golMatchFieldNiter, est, (num_iterations, actor_learning_rate, critic_learning_rate, batch_size, fc_layer_params, observation_fc_layer_params)), dtype=np.object))
    tf_env.close()

class ActorNetworkCustom(network.Network):
  """Creates a custom actor network."""

  def __init__(self,
               input_tensor_spec,
               output_tensor_spec,
               fc_layer_params=None,
               dropout_layer_params=None,
               conv_layer_params=None,
               activation_fn=tf.keras.activations.relu,
               kernel_initializer=None,
               last_kernel_initializer=None,
               name='ActorNetwork'):

    super(ActorNetworkCustom, self).__init__(
        input_tensor_spec=input_tensor_spec,
        state_spec=(),
        name=name)

    output_tensor_spec = tensor_spec.from_spec(output_tensor_spec)

    if len(tf.nest.flatten(input_tensor_spec)) > 1:
      raise ValueError('Only a single observation is supported by this network')

    flat_action_spec = tf.nest.flatten(output_tensor_spec)
    if len(flat_action_spec) > 1:
      raise ValueError('Only a single action is supported by this network')
    self._single_action_spec = flat_action_spec[0]

    if self._single_action_spec.dtype not in [tf.float32, tf.float64]:
      raise ValueError('Only float actions are supported by this network.')

    if kernel_initializer is None:
      kernel_initializer = tf.compat.v1.keras.initializers.VarianceScaling(
          scale=1. / 3., mode='fan_in', distribution='uniform')
    if last_kernel_initializer is None:
      last_kernel_initializer = tf.keras.initializers.RandomUniform(
          minval=-0.003, maxval=0.003)

    # TODO(kbanoop): Replace mlp_layers with encoding networks.
    self._mlp_layers = utils.mlp_layers(
        conv_layer_params,
        fc_layer_params,
        dropout_layer_params,
        activation_fn=activation_fn,
        kernel_initializer=kernel_initializer,
        name='input_mlp')

    self._mlp_layers.append(
        tf.keras.layers.Dense(
            flat_action_spec[0].shape.num_elements(),
            activation=lambda x: tf.nn.tanh(x),
            kernel_initializer=last_kernel_initializer,
            name='action'))

    self._output_tensor_spec = output_tensor_spec

  def call(self, observations, step_type=(), network_state=(), training=False):
    del step_type  # unused.
    observations = tf.nest.flatten(observations)
    output = tf.cast(observations[0], tf.float32)
    for layer in self._mlp_layers:
      output = layer(output, training=training)

    actions = common.scale_to_spec(output, self._single_action_spec)
    output_actions = tf.nest.pack_sequence_as(self._output_tensor_spec,
                                              [actions])

    return output_actions, network_state

if __name__ == '__main__':
  main()
