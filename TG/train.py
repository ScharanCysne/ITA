import supersuit as ss

from constants                          import *
from environment                        import CoverageMissionEnv
from stable_baselines3                  import PPO
from stable_baselines3.common.policies  import ActorCriticPolicy

# Trining Parameters
NUM_EPISODES = 1
NUM_TIMESTEPS = 1

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
model.learn(total_timesteps=NUM_EPISODES)
model.save("policy")