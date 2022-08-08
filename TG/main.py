import sys, pygame

from constants  import *
from interface  import Interface
from simulation import Simulation

# Create interface screen
interface = Interface(RESOLUTION)
# simulator object
simulation = Simulation(interface, 10)

run = True
while run:
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

    # Run simulation  
    run = simulation.run_simulation()
    # Draw Components
    simulation.draw()
    if not run:
        pygame.time.wait(5000) 
