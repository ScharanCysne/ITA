import sys, pygame

from constants  import *
from simulation import Simulation, ScreenSimulation, RateSimulation

def pause(paused):
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                sys.exit()
    return paused

# Create screen
screenSimulation = ScreenSimulation(RESOLUTION)
# defines initial target
target = pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT//2)
# simulator object
simulation = Simulation(screenSimulation, RateSimulation(5, [10,20,30]), 10)

run = True
paused = False
while run:
    # Draws at every dt
    screenSimulation.clock.tick(FREQUENCY)

    # Get Pygame Events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            sys.exit()
        # Key 'd' pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            for drone in simulation.swarm:
                drone.set_debug()
        # Mouse click - set new taget or new drone 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            target = pygame.math.Vector2(pos_x, pos_y)
            # right button - New Drone
            if pygame.mouse.get_pressed()[MOUSE_RIGHT] == True:
                simulation.add_new_uav(target)              
            # left button - New Target
            #if pygame.mouse.get_pressed()[MOUSE_LEFT] == True:
            #    simulation.set_target(target)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
            paused = pause(paused)

    # Run simulation  
    run = simulation.run_simulation()
    # Draw Components
    simulation.draw()
    
    pygame.display.flip()
    if not run:
        pygame.time.wait(5000) 
