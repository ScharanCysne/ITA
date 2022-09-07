import supersuit as ss

from constants                          import *
from environment                        import CoverageMissionEnv
from stable_baselines3                  import PPO
from stable_baselines3.common.policies  import ActorCriticPolicy

# Trining Parameters
NUM_EPISODES = 250
NUM_TIMESTEPS = 25000

from pettingzoo.test import parallel_api_test

# Shared Actor Critic Policy
# Creation of Environment
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES)
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, 4, num_cpus=4, base_class='stable_baselines3')

# Creation of PPO Multi-Agent model
model = PPO(
    ActorCriticPolicy,
    env,
    verbose=1
)
model.learn(total_timesteps=NUM_TIMESTEPS)
model.save("policy")