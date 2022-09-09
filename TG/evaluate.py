import sys
import pygame
import supersuit as ss

from interface                          import Interface
from constants                          import *
from environment                        import CoverageMissionEnv
from stable_baselines3                  import PPO

model = PPO.load("policy")

# Creation of Environment
env = CoverageMissionEnv(NUM_OBSTACLES, NUM_DRONES)
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, 4, num_cpus=4, base_class='stable_baselines3')
# Render interface
interface = Interface()

done = False
obs = env.reset()
while not done:
    actions = model.predict(obs, deterministic=True)[0]
    obs, rewards, dones, infos = env.step(actions)
    
    # Draws at every dt
    interface.clock.tick(FREQUENCY)
    swarm, obstacles, env_state, num_swarm, out_time = env.render()
    interface.draw(swarm, obstacles, env_state, num_swarm, out_time)
    # Get Pygame Events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            sys.exit()
env.close()