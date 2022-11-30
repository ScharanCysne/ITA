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


    def draw(self, agents, obstacles, state, leader):
        self.timestep += 1

        # Background
        self.screen.fill(LIGHT_GRAY)                             
        # Obstacles
        self.draw_obstacles(obstacles)                           
        # Connections
        self.draw_connections(agents, state)          
        # Drones
        self.draw_drones(agents, leader)  
        # Flip screen
        pygame.display.flip()
        # Record
        #pygame.image.save(self.screen, f"record/screenshot_{self.timestep}.jpeg")
        

    def draw_obstacles(self, obstacles):
        for coordinate in obstacles:
            pygame.draw.circle(self.screen, RED, RATIO * coordinate, radius=SIZE_OBSTACLES, width=20)
            pygame.draw.circle(self.screen, BLACK, RATIO * coordinate, radius=RATIO * AVOID_DISTANCE, width=1)
            #pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE, width=1)


    def draw_connections(self, agents, state):
        drones = list(agents.values())
        num_agents = len(drones)
        for i in range(num_agents):
            for j in range(i+1, num_agents):
                idx_i = drones[i].id
                idx_j = drones[j].id
                if state.adjacencyMatrix[idx_i][idx_j]:
                    pos_i = RATIO * drones[i].location
                    pos_j = RATIO * drones[j].location
                    pygame.draw.line(self.screen, BLACK, pos_i, pos_j, 1)


    def draw_drones(self, agents, leader):
        for tag, agent in agents.items():
            if tag == leader:
                continue
            else:
                # Draw drone's position            
                pygame.draw.circle(self.screen, BLUE, RATIO * agent.location, radius=SIZE_DRONE, width=20)
                pygame.draw.circle(self.screen, BLACK, RATIO * agent.location, radius=RATIO * AVOID_DISTANCE, width=1)
            
            # Draw leader's position            
            pygame.draw.circle(self.screen, GREEN, RATIO * agents[leader].location, radius=1.2 * SIZE_DRONE, width=20)
            pygame.draw.circle(self.screen, BLACK, RATIO * agents[leader].location, radius=RATIO * AVOID_DISTANCE, width=1)