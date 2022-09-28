import os
import supersuit as ss
import matplotlib.pyplot as plt

from callback                                   import Callback
from constants                                  import *
from environment                                import CoverageMissionEnv
from stable_baselines3                          import PPO
from stable_baselines3.common.policies          import ActorCriticPolicy
from stable_baselines3.common.results_plotter   import plot_results, X_TIMESTEPS

# Training Parameters
NUM_DRONES = 3
NUM_OBSTACLES = 20
NUM_EPISODES = 1
TOTAL_TIMESTEPS = NUM_EPISODES * TIMESTEPS_PER_ITERATION

print(" ---------- ")
print("Number of Agents: " + str(NUM_DRONES))
print("Number of Obstacles: " + str(NUM_OBSTACLES))
print("Number of Episodes: " + str(NUM_EPISODES))
print("Number of Timesteps per Episode: " + str(TIMESTEPS_PER_ITERATION))
print(" ---------- ")

# Test Env Variables
ENABLE_TARGET = False
ENABLE_OBSTACLES = True

# Create log dir
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)

# Creation of Environment
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES, ENABLE_TARGET, ENABLE_OBSTACLES)
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, 1, num_cpus=8, base_class='stable_baselines3')

# Callback function
callback = Callback(check_freq=1200, log_dir=log_dir)

# Creation of PPO Multi-Agent model
model = PPO(
    ActorCriticPolicy,
    env,
    verbose=1,
    device="cuda",
    n_steps=TIMESTEPS_PER_ITERATION,
    batch_size=60
)
model = model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=callback)
model.save(f"output/policy_{NUM_DRONES}_{NUM_EPISODES}_{ENABLE_TARGET}_{ENABLE_OBSTACLES}")

plot_results([log_dir], TOTAL_TIMESTEPS, X_TIMESTEPS, "PPO CoverageMission")
plt.savefig(f"output/rewards_{NUM_DRONES}_{NUM_EPISODES}_{ENABLE_TARGET}_{ENABLE_OBSTACLES}")