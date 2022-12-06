import sys
import pygame
import logging
import scipy.io
import warnings
import numpy as np

from utils                              import display_info
from drone                              import Drone
from interface                          import Interface
from constants                          import *
from environment                        import CoverageMissionEnv
from multiprocessing                    import Process, Queue, Lock

warnings.filterwarnings("ignore")
logging.basicConfig(filename='network.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# Create Logger
logger=logging.getLogger(__name__)
logger.info("Initiate Logger")

# Create communication Queues (pipes)
processes = []
queues = [Queue() for _ in range(NUM_DRONES + 1)] # 20 Drones + 1 Env

# Load random initial positions
index = np.random.randint(200)
positions = scipy.io.loadmat(f'model/positions/{index+1}/position.mat')["position"]
obstacles = scipy.io.loadmat(f'model/positions/{index+1}/obstacles.mat')["obstacles"]
obstacles = [pygame.math.Vector2(obs[0], 2*obs[1]) for obs in obstacles] # Scale to fit

# Create drones
for idx in range(NUM_DRONES):
    p = Process(target=Drone, args=(idx, positions, obstacles, queues, logger))
    processes.append(p)
    p.start()

# Create environment
env = CoverageMissionEnv(positions, obstacles, queues, logger)

# Render interface
interface = Interface()

# Init episode
timesteps = 0
done = False

while not done:
    timesteps += 1
    # Execute actions and communication
    done, infos = env.step()
    
    # Draws at every dt
    interface.clock.tick(FREQUENCY)
    positions, state, leader, alive = env.render()
    interface.draw(positions, obstacles, state, leader, alive)
    
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
    display_info(infos)

for idx in range(NUM_DRONES):
    processes[idx].join()