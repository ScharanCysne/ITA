import pygame

from constants import *

class Interface(object):
    def __init__(self, resolution=RESOLUTION):
        pygame.init()
        self.resolution = resolution
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT 
        self.font20 = pygame.font.SysFont(None, 20)
        self.font24 = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

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

    def update_screen(self, swarm=[], obstacles=[], state=None, simulation_time=0, swarm_size=0):
        # Background
        self.screen.fill(LIGHT_GRAY)                             
        # Starting area
        self.screen.blit(self.start_area, (0, 0))                
        # Ending area
        self.screen.blit(self.end_area, (SCREEN_WIDTH*0.9, 0))   
        # Flow Chart
        #self.flow.draw(self.screen)                              
        # Drone field of vision
        self.draw_observable_area(swarm, 4, state, swarm_size)       
        # Obstacles
        self.draw_obstacles(obstacles)                           
        # Connections
        self.draw_connections(swarm, swarm_size, state)          
        # Drones
        self.draw_drones(swarm)                                  
        # Running Time
        self.screen.blit(simulation_time, (1490, 20))            
        # Title
        self.screen.blit(self.title, (20, 20))                   
        # Flip screen
        pygame.display.flip()
        
    def draw_obstacles(self, obstacles):
        for coordinate in obstacles: 
            pygame.draw.circle(self.screen, RED, coordinate, radius=RADIUS_OBSTACLES//4, width=20)
            pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES, width=1)
            #pygame.draw.circle(self.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE, width=1)

    def draw_connections(self, swarm, swarm_size, state):
        for i in range(swarm_size):
            for j in range(i+1, swarm_size):
                if state.adjacencyMatrix[i][j]:
                    pos_i = swarm[i].get_position()
                    pos_j = swarm[j].get_position()
                    pygame.draw.line(self.screen, BLACK, pos_i, pos_j, 1)

    def draw_drones(self, swarm):
        for drone in swarm:
            # Draw drone's position            
            drone.draw(self.screen) 
            # writes drone id
            img = self.font20.render(f'Drone {drone.id}', True, BLACK)
            self.screen.blit(img, drone.get_position() + (0,20))
            # writes drone current position in column and row
            p = drone.get_position()
            col = p.x // RESOLUTION + 1
            row = p.y // RESOLUTION + 1
            img = self.font20.render(f'Pos:{col},{row}', True, BLUE)
            self.screen.blit(img, drone.get_position()+(0,35))

    def draw_observable_area(self, swarm, drone, state, swarm_size):
        paintable = set()
        reachable_hops = list()
        for i in range(swarm_size):
            if state.adjacencyMatrix[drone][i]:
                reachable_hops.append(i)
                paintable.add(i)
        for i in range(len(reachable_hops)):
            if state.adjacencyMatrix[reachable_hops[i]][i]:
                paintable.add(i)
        paintable.add(drone)

        for drone in paintable:
            self.paint_observable_area(swarm, drone)        

    def paint_observable_area(self, swarm, drone):
        pos = swarm[drone].get_position()
        pygame.draw.circle(self.screen, LIGHT_YELLOW, pos, radius=OBSERVABLE_RADIUS)
                
        """
        blockSize = self.resolution    # Set the size of the grid block
        pos_x, pos_y = swarm[drone].get_position()
        
        pos_x = (pos_x // blockSize) * blockSize
        pos_y = (pos_y // blockSize) * blockSize

        grid_x_i = int(pos_x - 10*blockSize)
        grid_x_f = int(pos_x + 10*blockSize)
        grid_y_i = int(pos_y - 10*blockSize)
        grid_y_f = int(pos_y + 10*blockSize)
        
        for x in range(grid_x_i, grid_x_f, blockSize):
            for y in range(grid_y_i, grid_y_f, blockSize):
                if distance(pos_x, pos_y, x, y) < OBSERVABLE_RADIUS:
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(self.screen, LIGHT_RED, rect)
                    pygame.draw.rect(self.screen, LIGHT_GRAY, rect, 1)
        """


class Grader(object):
    def __init__(self, repetitions, num_swarm):
        self.current_repetition = 0
        # Number of repetitions in total
        self.repetitions = repetitions
        # Number of drones in swarm for each iteration
        self.num_swarm = []
        for n in num_swarm:
            self.num_swarm = self.num_swarm + [n]*repetitions
        # Outputs of Rate
        self.out_time = []
        self.print_simulation()

    def set_out(self, out_time):
        self.out_time.append(out_time)

    def next_simulation(self):
        if self.repetitions - 1 == self.current_repetition:
            return False
        else:
            self.current_repetition = self.current_repetition + 1
            self.print_simulation()
            return True

    def print_simulation(self):
        print(f'{self.current_repetition+1} - num_swarm: {self.num_swarm[self.current_repetition]}')
