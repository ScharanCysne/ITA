import time, pygame, numpy as np

from state         import State
from utils         import FlowField, distance
from drone         import Drone
from obstacle      import Obstacles
from constants     import *
from behavior      import Behavior

class RateSimulation(object):
    def __init__(self, repetitions, num_swarm):
        self.current_repetition = 0
        
        # Number of repetitions in total
        self.repetitions = repetitions * len(num_swarm)
        # Number of drones in swarm for each iteration
        self.num_swarm = []
        for n in num_swarm:
            self.num_swarm = self.num_swarm + [n] * (self.repetitions // len(num_swarm))

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


class ScreenSimulation(object):
    def __init__(self, resolution=RESOLUTION):
        pygame.init()
        self.resolution = resolution
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT 
        self.font20 = pygame.font.SysFont(None, 20)
        self.font24 = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # Title
        self.title = self.font24.render('DeepRL for Swarm of Drones', True, BLACK)
        # Flow Chart
        self.flow = FlowField(resolution)
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
        self.draw_drones(swarm, swarm_size)                                  
        # Running Time
        self.screen.blit(simulation_time, (1490, 20))            
        # Title
        self.screen.blit(self.title, (20, 20))                   

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

    def draw_drones(self, swarm, swarm_size):
        for i in range(swarm_size):
            drone = swarm[i]
            # Draw drone's position            
            drone.draw(self.screen) 
            # writes drone id
            img = self.font20.render(f'Drone {i}', True, BLACK)
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

class Simulation(object):
    def __init__(self, screenSimulation, rate, num_swarm=NUM_DRONES, num_obstacles=NUM_OBSTACLES):
        self.target_simulation = SCREEN_WIDTH
        self.screenSimulation = screenSimulation
        self.start_watch = 0
        self.stop_watch = 0
        self.sim_time = self.screenSimulation.font24.render(f"Time: 0.00s", True, BLACK)
        self.rate = rate
        self.time_executing = 0 
        
        # variables for obstacles
        self.obstacles = Obstacles(num_obstacles, (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.list_obst = []
        self.generate_obstacles()
        
        # state machines for each Drone
        self.behavior = Behavior(self.target_simulation) 
        
        # Current simulations 
        self.num_swarm = num_swarm
        self.swarm = []
        self.create_swarm()
        
        # Simulation State 
        self.state = State(num_swarm)

    def generate_obstacles(self):
        # Generates obstacles
        self.obstacles.generate_obstacles()
        self.list_obst = self.obstacles.get_coordenates()

    def create_swarm(self):
        # TODO: Change to Cinara's code
        # Create N simultaneous Drones
        for d in range(1, self.num_swarm+1):
            drone = Drone(10, SCREEN_HEIGHT*d/(self.num_swarm + 1), self.behavior)
            self.swarm.append(drone)

    def add_new_uav(self, target):
        drone = Drone(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, self.behavior)
        drone.set_target(target)
        self.append_uav(drone)

    def append_uav(self, drone):
        self.swarm.append(drone)

    def set_target(self, target):
        self.target_simulation = target
        for drone in self.swarm:
            drone.set_target(target)

    def run_simulation(self):
        if self.start_watch == 0:
            self.start_watch = time.time()

        self.state.scan(self, self.list_obst)
        self.time_executing += SAMPLE_TIME # count time of execution based on the sampling
        self.sim_time = self.screenSimulation.font24.render(f"Time: {self.time_executing:.2f} s", True, BLACK)
        self.state.updateMatrix(self.swarm)

        if self.completed_simulation() >= 0.8 and self.stop_watch == 0 or self.time_executing > TIME_MAX_SIMULATION:
            self.stop_watch = time.time()
            
            if self.rate and self.rate.next_simulation():
                self.reset_simulation()
            else:
                return False

        # Print time of each iteration
        for idx, t in enumerate(self.rate.out_time):
            try:
                img = self.screenSimulation.font20.render(f'{idx+1} - Scan Time: {t:.2f}', True, BLACK)
            except:
                img = self.screenSimulation.font20.render(f'{idx+1} - Scan Time: {t}', True, BLACK)
            self.screenSimulation.screen.blit(img, (20, 20*(idx+2)))

        return True

    def completed_simulation(self):
        count_completed = 0
        for drone in self.swarm:
            if drone.reached_goal(self.target_simulation):
                count_completed = count_completed + 1 
        return count_completed/self.rate.num_swarm[self.rate.current_repetition]

    def reset_simulation(self):
        # new obstacles
        self.generate_obstacles()

        time = self.stop_watch - self.start_watch
        if self.time_executing > TIME_MAX_SIMULATION:
            time = "Goal not reached"
        self.rate.set_out(time)
            
        for drone in self.swarm:
            drone.set_target(None)
            del drone

        self.swarm = []
        self.time_executing = 0 # Reset timer
        self.start_watch = 0
        self.stop_watch = 0
        self.num_swarm = self.rate.num_swarm[self.rate.current_repetition]
        self.state = State(self.num_swarm)
        self.create_swarm()

    def draw(self):
        self.screenSimulation.update_screen(self.swarm, self.list_obst, self.state, self.sim_time, self.num_swarm)