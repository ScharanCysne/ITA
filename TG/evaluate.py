import sys
import pygame

from interface                          import Interface
from constants                          import *
from environment                        import CoverageMissionEnv
from stable_baselines3                  import PPO
from pettingzoo.test                    import parallel_api_test

NUM_DRONES = 20
NUM_OBSTACLES = 50
NUM_EPISODES = 10
NUM_TIMESTEPS = 10000

# Load Model
#model = PPO.load(f"tmp/model_10_2000")
model = PPO.load(f"output/policy_10_3000")
#model = PPO.load(f"model_b_3")
#model = PPO.load(f"model_b_4")
#model = PPO.load(f"model_b_5")
#model = PPO.load(f"model_b_20")

# Creation of Environment
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES, EVALUATION)
parallel_api_test(env, num_cycles=1000)

# Render interface
interface = Interface()
episode_time = []
timesteps = 0
record = True

for episode in range(NUM_EPISODES):
    # Init episode
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
        agents, obstacles, env_state, num_agents, time_executing = env.render()
        interface.draw(agents, obstacles, env_state, num_agents, episode_time, time_executing, record)
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
    record = False
