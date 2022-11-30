import sys
import pygame
import warnings
import numpy as np

from interface                          import Interface
from constants                          import *
from environment                        import CoverageMissionEnv
from utils                              import plot_results

warnings.filterwarnings("ignore")

# Create environment
env = CoverageMissionEnv()

# Render interface
#interface = Interface()
# Init episode

algebraic_connectivity = np.zeros((200, 720))
robustness_level = np.zeros((200, 720))

for episode in range(200):
    timesteps = 0
    done = False
    env.reset(episode)

    while not done:
        timesteps += 1
        # Execute actions and communication
        dones, infos = env.step()
        
        # # Draws at every dt
        # interface.clock.tick(FREQUENCY)
        # agents, obstacles, state, leader = env.render()
        # interface.draw(agents, obstacles, state, leader)
        
        # # Get Pygame Events 
        # for event in pygame.event.get():
        #     # Qui Event
        #     if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
        #         sys.exit()
        #     # Pause Event
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         while True:
        #             pause = True
        #             for event in pygame.event.get():
        #                 if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #                     pause = False
        #                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
        #                     sys.exit()
        #             if not pause:
        #                 break
        done = list(dones.values())[0]
        algebraic_connectivity[episode, timesteps-1] = env.state.algebraic_connectivity
        robustness_level[episode, timesteps-1] = env.state.network_robustness
    print(f"Episode {episode}")

# Plot Algebraic Connectivity, Area Coverage, Robustness Level
plot_results(NUM_DRONES, 720, robustness_level, algebraic_connectivity)