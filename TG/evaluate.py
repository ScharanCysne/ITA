import sys
import pygame
import supersuit as ss

from interface                          import Interface
from constants                          import *
from environment                        import CoverageMissionEnv
from stable_baselines3                  import PPO
from pettingzoo.test                    import parallel_api_test

NUM_DRONES = 10
NUM_OBSTACLES = 20
NUM_TIMESTEPS = 30000
NUM_EPISODES = 10

# Test Env Variables
ENABLE_TARGET = False
ENABLE_OBSTACLES = True

# Load Model
model = PPO.load(f"policy_{NUM_DRONES}_{NUM_TIMESTEPS}_{ENABLE_TARGET}_{ENABLE_OBSTACLES}")

# Creation of Environment
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES, ENABLE_TARGET, ENABLE_OBSTACLES)
parallel_api_test(env, num_cycles=1000)

# Render interface
interface = Interface()
episode_time = []
timesteps = 0
for episode in range(NUM_EPISODES):
    timesteps = 0
    done = False
    obs = env.reset()
    while not done:
        timesteps += 1
        actions = dict()
        for agent in obs:
            actions[agent] = model.predict(obs[agent], deterministic=True)[0]
        obs, rewards, dones, infos = env.step(actions)
        
        # Draws at every dt
        interface.clock.tick(FREQUENCY)
        swarm, obstacles, env_state, num_swarm, time_executing = env.render()
        interface.draw(swarm, obstacles, env_state, num_swarm, episode_time, time_executing)
        # Get Pygame Events 
        for event in pygame.event.get():
            # Qui Event
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                sys.exit()
            # Pause Event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                while True:
                    pause = True
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            pause = False
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                            sys.exit()
                    if not pause:
                        break
        if dones[agent]:
            done = True
    env.close()