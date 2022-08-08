import time, numpy as np

from state         import State
from utils         import FlowField, distance
from drone         import Drone
from behavior      import Behavior
from obstacle      import Obstacles
from interface     import Grader
from constants     import *

class Simulation(object):
    def __init__(self, interface, num_swarm=NUM_DRONES, num_obstacles=NUM_OBSTACLES):
        self.target_simulation = SCREEN_WIDTH
        self.interface = interface
        self.start_watch = 0
        self.stop_watch = 0
        self.sim_time = self.interface.font24.render(f"Time: 0.00s", True, BLACK)
        self.rate = Grader(5, [10,20,30])
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
        for index in range(1, self.num_swarm+1):
            drone = Drone(10, SCREEN_HEIGHT*index/(self.num_swarm + 1), self.behavior, index)
            self.swarm.append(drone)

    def run_simulation(self):
        if self.start_watch == 0:
            self.start_watch = time.time()

        self.state.scan(self, self.list_obst)
        self.time_executing += SAMPLE_TIME # count time of execution based on the sampling
        self.sim_time = self.interface.font24.render(f"Time: {self.time_executing:.2f} s", True, BLACK)
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
                img = self.interface.font20.render(f'{idx+1} - Scan Time: {t:.2f}', True, BLACK)
            except:
                img = self.interface.font20.render(f'{idx+1} - Scan Time: {t}', True, BLACK)
            self.interface.screen.blit(img, (20, 20*(idx+2)))

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
            del drone

        self.swarm = []
        self.time_executing = 0 # Reset timer
        self.start_watch = 0
        self.stop_watch = 0
        self.num_swarm = self.rate.num_swarm[self.rate.current_repetition]
        self.state = State(self.num_swarm)
        self.create_swarm()

    def draw(self):
        self.interface.update_screen(self.swarm, self.list_obst, self.state, self.sim_time, self.num_swarm)