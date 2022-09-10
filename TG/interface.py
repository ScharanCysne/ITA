import pygame

from constants import *

class Interface(object):
    def __init__(self):
        pygame.init()
        self.resolution = RESOLUTION
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT 
        self.font20 = pygame.font.SysFont(None, 20)
        self.font24 = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.time_executing = 0

        # Title
        self.title = self.font24.render('Deep Reinforcement Learning for Drones in Coverage Missions', True, BLACK)
        # Flow Chart
        #self.flow = FlowField(resolution)
        # Drones' start srea
        self.start_area = pygame.Surface((SCREEN_WIDTH*0.1, SCREEN_HEIGHT))
        self.start_area.set_alpha(50)
        pygame.draw.rect(self.start_area, BLUE, self.start_area.get_rect(), 1)
        # Drones' end area
        self.end_area = pygame.Surface((SCREEN_WIDTH*0.1, SCREEN_HEIGHT))
        self.end_area.set_alpha(50)
        pygame.draw.rect(self.end_area, BLUE, self.end_area.get_rect(), 1)
        # Simulation Time
        self.sim_time = self.font24.render(f"Time: 0.00s", True, BLACK)

    def draw(self, swarm, obstacles, env_state, num_swarm, out_time):
        self.time_executing += SAMPLE_TIME # count time of execution based on the sampling
        self.update_screen(swarm, obstacles, env_state, num_swarm, out_time)

    def update_screen(self, swarm=[], obstacles=[], state=None, num_agents=0, out_time=[]):
        # Background
        self.screen.fill(LIGHT_GRAY)                             
        # Starting area
        self.screen.blit(self.start_area, (0, 0))                
        # Ending area
        self.screen.blit(self.end_area, (SCREEN_WIDTH*0.9, 0))   
        # Flow Chart
        #self.flow.draw(self.screen)                              
        # Drone field of vision
        self.draw_observable_area(swarm, 4, state, num_agents)       
        # Obstacles
        self.draw_obstacles(obstacles)                           
        # Connections
        self.draw_connections(swarm, num_agents, state)          
        # Drones
        self.draw_drones(swarm)  
        # Field vectors
        self.draw_field_vectors(swarm, obstacles)                                
        # Running Time
        self.sim_time = self.font24.render(f"Time: {self.time_executing:.2f} s", True, BLACK)
        self.screen.blit(self.sim_time, (1490, 20))   
        # Title
        self.screen.blit(self.title, (20, 20))
        # Print time of each iteration
        for idx, t in enumerate(out_time):
            try:
                img = self.font20.render(f'{idx+1} - Scan Time: {t:.2f}', True, BLACK)
            except:
                img = self.font20.render(f'{idx+1} - Scan Time: {t}', True, BLACK)
            self.screen.blit(img, (20, 20*(idx+2)))
        # Flip screen
        pygame.display.flip()
        
    def draw_obstacles(self, obstacles):
        for coordinate in obstacles: 
            pygame.draw.circle(self.screen, RED, coordinate, radius=RADIUS_OBSTACLES//4, width=20)
            pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES, width=1)
            #pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE, width=1)

    def draw_connections(self, swarm, num_agents, state):
        for i in range(num_agents):
            for j in range(i+1, num_agents):
                if state.adjacencyMatrix[i][j]:
                    pos_i = swarm[i].location
                    pos_j = swarm[j].location
                    pygame.draw.line(self.screen, BLACK, pos_i, pos_j, 1)

    def draw_drones(self, swarm):
        for drone in swarm:
            # Draw drone's position            
            drone.draw(self.screen) 
            # writes drone id
            img = self.font20.render(f'Drone {drone.id}', True, BLACK)
            self.screen.blit(img, drone.location + (0,20))
            # writes drone current position in column and row
            p = drone.location
            col = p.x // RESOLUTION + 1
            row = p.y // RESOLUTION + 1
            img = self.font20.render(f'Pos:{col},{row}', True, BLUE)
            self.screen.blit(img, drone.location + (0,35))

    def draw_observable_area(self, swarm, drone, state, num_agents):
        paintable = set()
        hops = list()
        for i in range(num_agents):
            if state.adjacencyMatrix[drone][i]:
                hops.append(i)
                paintable.add(i)
        for neighbor in hops:
            for i in range(num_agents):
                if state.adjacencyMatrix[neighbor][i]:
                    paintable.add(i)
        paintable.add(drone)

        for drone in paintable:
            self.paint_observable_area(swarm, drone)        

    def paint_observable_area(self, swarm, drone):
        for drone in swarm:
            #pos = swarm[drone].location
            pos = drone.location
            pygame.draw.circle(self.screen, LIGHT_YELLOW, pos, radius=OBSERVABLE_RADIUS)

    def draw_field_vectors(self, drones, obstacles):
        for drone in drones:
            pos_i = drone.location
            # Obstacles vector
            pos_j = drone.location + drone.obstacles * OBSERVABLE_RADIUS // 4
            pygame.draw.line(self.screen, RED, pos_i, pos_j, 1)
            # Neighbors vector
            pos_j = drone.location + drone.neighbors * OBSERVABLE_RADIUS // 4
            pygame.draw.line(self.screen, BLACK, pos_i, pos_j, 1)
