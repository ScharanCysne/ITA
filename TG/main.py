import sys, pygame

from scan import DefineTargetScan
from constants import *
from simulation import Simulation, ScreenSimulation, RateSimulation

screenSimulation = ScreenSimulation()

# defines initial target
target = pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT//2)
# simulator object
simulation = Simulation(screenSimulation, RateSimulation(5, [10,20], DefineTargetScan()))

run = True
while run:
    # Draws at every dt
    screenSimulation.clock.tick(FREQUENCY)
    # Get Pygame Events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        # Key 'd' pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            for drone in simulation.swarm:
                drone.set_debug()
        # Mouse click - set new taget or new drone 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            target = pygame.math.Vector2(pos_x, pos_y)
            # left button - New Target
            if pygame.mouse.get_pressed()[MOUSE_LEFT] == True:
                simulation.set_target(target)
            # right button - New Drone
            if pygame.mouse.get_pressed()[MOUSE_RIGHT] == True:
                simulation.add_new_uav(target)              
                
    # Background
    screenSimulation.screen.fill(LIGHT_GRAY)
    # Run one step of the simulation  
    run = simulation.run_simulation()
    # Print time of each iteration
    for idx, time in enumerate(simulation.rate.out_time):
        try:
            img = screenSimulation.font20.render(f'{idx+1} - Scan Time: {time:.2f}', True, BLACK)
        except:
            img = screenSimulation.font20.render(f'{idx+1} - Scan Time: {time}', True, BLACK)
        screenSimulation.screen.blit(img, (20, 20*(idx+2)))
    # Writes the simulation name in screen
    img = screenSimulation.font24.render('DeepRL for Swarm of Drones', True, BLACK)
    screenSimulation.screen.blit(img, (20, 20))

    pygame.display.flip()
    if not run:
        pygame.time.wait(5000) 