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
parallel_api_test(env, num_cycles=1000)
# Creation of PPO Multi-Agent model
model = PPO(
    ActorCriticPolicy,
    env,
    verbose=3,
    gamma=0.95,
    n_steps=256,
    ent_coef=0.0905168,
    learning_rate=0.00062211,
    vf_coef=0.042202,
    max_grad_norm=0.9,
    gae_lambda=0.99,
    n_epochs=5,
    clip_range=0.3,
    batch_size=256,
)
model.learn(total_timesteps=NUM_TIMESTEPS)
model.save("policy")

# Rendering
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES)
model = PPO.load("policy")
env.reset()
for agent in env.agent_iter():
    obs, reward, done, info = env.last()
    act = model.predict(obs, deterministic=True)[0] if not done else None
    env.step(act)
    env.render()
