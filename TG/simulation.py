import time, pygame

from utils         import NPC
from drone         import Drone
from obstacle      import Obstacles
from constants     import *
from state_machine import FiniteStateMachine, SeekState

class RateSimulation(object):
    def __init__(self, repetitions, num_swarm, algorithm):
        self.current_repetition = 0
        self.algorithm = algorithm
        
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
        print(f'{self.current_repetition+1} - num_swarm: {self.num_swarm[self.current_repetition]}, Algorithm: {self.algorithm.to_string()}')


class ScreenSimulation(object):
    def __init__(self):
        pygame.init()
        self.font20 = pygame.font.SysFont(None, 20)
        self.font24 = pygame.font.SysFont(None, 24)
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT 
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)


class Simulation(object):
    def __init__(self, screenSimulation, rate, num_obstacles=NUM_OBSTACLES):
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
        self.behaviors =[] 
        # Current simulations 
        self.swarm = []
        # npc target 
        self.npc = NPC()
        
        self.create_swarm_uav(rate.num_swarm[0])

    def generate_obstacles(self):
        # Generates obstacles
        self.obstacles.generate_obstacles()
        self.list_obst = self.obstacles.get_coordenates()

    def create_swarm_uav(self, num_swarm):
        # TODO: Change to Cinara's code
        # Create N simultaneous Drones
        for d in range(1, num_swarm+1):
            self.behaviors.append( FiniteStateMachine( SeekState() ) ) # Inicial state
            #using Old Drone: steering behavior
            drone = Drone(10, SCREEN_HEIGHT*d/(num_swarm + 1), self.behaviors[-1], self.screenSimulation.screen)
            #using potential fields
            self.swarm.append(drone)

    def add_new_uav(self, target):
        self.behaviors.append( FiniteStateMachine( SeekState() ) )
         #using Old Drone: steering behavior
        drone = Drone(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, self.behaviors[-1], self.screenSimulation.screen)
        #using potential fields
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

        self.rate.algorithm.scan(self, self.list_obst)
        self.time_executing += SAMPLE_TIME # count time of execution based on the sampling
        self.sim_time = self.screenSimulation.font24.render(f"Time: {self.time_executing:.2f} s", True, BLACK)
        
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

    def draw_obstacles(self):
        for coordinate in self.list_obst: 
            pygame.draw.circle(self.screenSimulation.screen, RED, coordinate, radius=RADIUS_OBSTACLES//4, width=20)
            pygame.draw.circle(self.screenSimulation.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES, width=1)
            pygame.draw.circle(self.screenSimulation.screen, BLACK, coordinate, radius=RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE, width=1)

    def draw_drones(self):
        for drone in self.swarm:
            drone.draw(self.screenSimulation.screen) 

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
        self.create_swarm_uav(self.rate.num_swarm[self.rate.current_repetition])