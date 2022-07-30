import sys, pygame

from scan       import TargetScan
from utils      import FlowField
from constants  import *
from simulation import Simulation, ScreenSimulation, RateSimulation

def draw():
    screenSimulation.screen.fill(LIGHT_GRAY)                        # Background
    screenSimulation.screen.blit(start_area, (0, 0))                # Starting area
    screenSimulation.screen.blit(end_area, (SCREEN_WIDTH*0.9, 0))   # Ending area
    flowField.draw(screenSimulation.screen)                         # Flow
    simulation.draw_observable_area(4)
    simulation.draw_obstacles()                                     # Obstacles
    simulation.draw_connections()                                   # Connections
    simulation.draw_drones()                                        # Drones
    screenSimulation.screen.blit(simulation.sim_time, (1490, 20))   # Running Time
    screenSimulation.screen.blit(title, (20, 20))                   # Title

screenSimulation = ScreenSimulation(RESOLUTION)
flowField = FlowField(RESOLUTION)

# Title
title = screenSimulation.font24.render('DeepRL for Swarm of Drones', True, BLACK)
# defines initial target
target = pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT//2)
# simulator object
simulation = Simulation(screenSimulation, RateSimulation(5, [10,20,30], TargetScan()))
# Drones' start srea
start_area = pygame.Surface((SCREEN_WIDTH*0.1, SCREEN_HEIGHT))
start_area.set_alpha(50)
pygame.draw.rect(start_area, BLUE, start_area.get_rect(), 1)
# Drones' end area
end_area = pygame.Surface((SCREEN_WIDTH*0.1, SCREEN_HEIGHT))
end_area.set_alpha(50)
pygame.draw.rect(end_area, BLUE, end_area.get_rect(), 1)

run = True
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

    # Draw Components
    draw()
    # Run simulation  
    run = simulation.run_simulation()

    pygame.display.flip()
    if not run:
        pygame.time.wait(5000) 
