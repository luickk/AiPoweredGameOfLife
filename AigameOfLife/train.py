import os
import time
import tf_agents
import tensorflow as tf

from gameOfLifeEnv import GolEnv

from absl import logging

from tf_agents.agents.ddpg import ddpg_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common

def main():
  tf.compat.v1.enable_v2_behavior()
  logging.set_verbosity(logging.INFO)
  train_eval()

def train_eval(
    golMatchFieldDims=(12,12),
    num_iterations=2000000,
    actor_learning_rate=1e-4,
    critic_learning_rate=1e-3,
    initial_collect_steps=1000,
    replay_buffer_capacity=100000,
    collect_steps_per_iteration=1,
    batch_size=12):

    global_step = tf.compat.v1.train.get_or_create_global_step()

    tf_env = tf_py_environment.TFPyEnvironment(GolEnv(golMatchFieldDims[0],golMatchFieldDims[1]))

    actor_net = tf_agents.agents.ddpg.actor_network.ActorNetwork(tf_env.observation_spec(), tf_env.action_spec(), activation_fn=tf.keras.activations.relu, name='ActorNetwork')

    critic_net = tf_agents.agents.ddpg.critic_network.CriticNetwork((tf_env.action_spec(), tf_env.observation_spec()), activation_fn=tf.nn.relu, name='CriticNetwork')

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

    my_random_tf_policy = random_tf_policy.RandomTFPolicy(action_spec=tf_env.action_spec(), time_step_spec=tf_env.time_step_spec())

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        tf_agent.collect_data_spec,
        batch_size=tf_env.batch_size,
        max_length=replay_buffer_capacity)

    initial_collect_driver = dynamic_step_driver.DynamicStepDriver(
        tf_env,
        my_random_tf_policy,
        observers=[replay_buffer.add_batch],
        num_steps=initial_collect_steps)

    collect_driver = dynamic_step_driver.DynamicStepDriver(
        tf_env,
        my_random_tf_policy,
        observers=[replay_buffer.add_batch],
        num_steps=collect_steps_per_iteration)

    # Collect initial replay data.
    logging.info(
        'Initializing replay buffer by collecting experience for %d steps with '
        'a random policy.', initial_collect_steps)
    initial_collect_driver.run()

    time_step = None
    policy_state = my_random_tf_policy.get_initial_state(tf_env.batch_size)

    # Dataset generates trajectories with shape [Bx2x...]
    dataset = replay_buffer.as_dataset(
        num_parallel_calls=1,
        sample_batch_size=1,
        num_steps=2).prefetch(3)

    iterator = iter(dataset)

    for i in range(num_iterations):
        time_step, policy_state = collect_driver.run(time_step=time_step, policy_state=policy_state)
        experience, _ = next(iterator)
        train_loss = tf_agent.train(experience)
        print(train_loss.loss)
    return train_loss

if __name__ == '__main__':
  main()
