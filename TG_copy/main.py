import sys, pygame

from constants  import *
from interface  import Interface
from simulation import Simulation

# Training mode
training = False
# Simulator object
simulation = Simulation(num_agents=5, num_obstacles=10, episodes=1000)
# Create interface screen
if not training:
    interface = Interface()

run = True
while run:
    # Run simulation  
    run = simulation.run()
    # Draw in Interface for non training runs
    if not training:
        # Draws at every dt
        interface.clock.tick(FREQUENCY)
        # Get Pygame Events 
        for event in pygame.event.get():
            # Quit simulation
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                sys.exit()
            # Pause simulation
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
        # Draw Components
        swarm, obstacles, env_state, num_swarm, out_time = simulation.get_status()
        interface.draw(swarm, obstacles, env_state, num_swarm, out_time)
        if not run:
            pygame.time.wait(5000) 
