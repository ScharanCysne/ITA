import pygame

from constants import *

class Interface(object):
    def __init__(self):
        pygame.init()
        self.resolution = RESOLUTION
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT 
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.timestep = 0


    def draw(self, positions, obstacles, state, leader, alive):
        self.timestep += 1

        # Background
        self.screen.fill(LIGHT_GRAY)                             
        # Obstacles
        self.draw_obstacles(obstacles)                           
        # Connections
        self.draw_connections(positions, state)          
        # Drones
        self.draw_drones(positions, leader, alive)  
        # Flip screen
        pygame.display.flip()
        # Record
        #pygame.image.save(self.screen, f"record/screenshot_{self.timestep}.jpeg")
        

    def draw_obstacles(self, obstacles):
        for coordinate in obstacles:
            pygame.draw.circle(self.screen, RED, RATIO * coordinate, radius=SIZE_OBSTACLES, width=20)
            pygame.draw.circle(self.screen, BLACK, RATIO * coordinate, radius=RATIO * AVOID_DISTANCE, width=1)
            #pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE, width=1)


    def draw_connections(self, positions, state):
        num_agents = len(positions)
        for i in range(num_agents):
            if i not in state.alive: continue
            for j in range(i+1, num_agents):
                if j not in state.alive: continue
                if state.adjacencyMatrix[i][j]:
                    pos_i = RATIO * positions[i]
                    pos_j = RATIO * positions[j]
                    pygame.draw.line(self.screen, BLACK, pos_i, pos_j, 1)


    def draw_drones(self, positions, leader, alive):
        for idx, position in enumerate(positions):
            if idx != leader and idx in alive:
                # Draw drone's position            
                pygame.draw.circle(self.screen, BLUE, RATIO * position, radius=SIZE_DRONE, width=20)
                pygame.draw.circle(self.screen, BLACK, RATIO * position, radius=RATIO * AVOID_DISTANCE, width=1)
            
        # Draw leader's position   
        if leader > -1 and leader in alive:         
            pygame.draw.circle(self.screen, GREEN, RATIO * positions[leader], radius=1.2 * SIZE_DRONE, width=22)
            pygame.draw.circle(self.screen, BLACK, RATIO * positions[leader], radius=RATIO * AVOID_DISTANCE, width=1)