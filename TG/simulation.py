import time

from utils         import FlowField
from drone         import Drone
from constants     import *
from environment   import Environment

class Simulation(object):
    def __init__(self, num_agents=NUM_DRONES, num_obstacles=NUM_OBSTACLES, repetitions=10):
        # Simulation variables
        self.repetitions = repetitions
        self.current_repetition = 1
        self.start_watch = 0
        self.stop_watch = 0
        self.time_executing = 0 
        self.out_time = []

        # Environment variables
        self.target_simulation = SCREEN_WIDTH
        self.environment = Environment(num_obstacles, num_agents)
        
        # Current simulation 
        self.num_obstacles = num_obstacles
        self.num_agents = num_agents

        # Create agents and obstacles
        self.create_swarm()
        self.generate_obstacles()

    def create_swarm(self):
        # TODO: Change to Cinara's code
        self.swarm = []
        # Create N Drones
        for index in range(1, self.num_agents+1):
            drone = Drone(10, SCREEN_HEIGHT*index/(self.num_agents + 1), index)
            self.swarm.append(drone)

    def generate_obstacles(self):
        # Generates obstacles
        self.environment.generate_obstacles()
        self.obstacles = self.environment.get_obstacles()

    def run_simulation(self):
        if self.start_watch == 0:
            self.start_watch = time.time()
        self.time_executing += SAMPLE_TIME

        self.environment.scan(self, self.obstacles)
        self.environment.update(self.swarm)
        return self.continue_simulation()

    def continue_simulation(self):
        if self.rate_of_completion() >= 0.8 and self.stop_watch == 0 or self.time_executing > TIME_MAX_SIMULATION:
            self.stop_watch = time.time()
            if self.next_simulation():
                self.reset_simulation()
            else:
                return False
        return True

    def rate_of_completion(self):
        count_completed = 0
        for drone in self.swarm:
            if drone.reached_goal(self.target_simulation):
                count_completed = count_completed + 1 
        return count_completed / self.num_agents

    def reset_swarm(self):
        for drone in self.swarm:
            del drone
        self.create_swarm()

    def reset_simulation(self):
        time = self.stop_watch - self.start_watch
        if self.time_executing > TIME_MAX_SIMULATION:
            time = "Goal not reached"
        self.set_out_time(time)
            
        self.generate_obstacles()
        self.reset_swarm()
        
        self.time_executing = 0 
        self.start_watch = 0
        self.stop_watch = 0
    
    def get_status(self):
        return self.swarm, self.obstacles, self.environment, self.num_agents, self.out_time

    def set_out_time(self, out_time):
        self.out_time.append(out_time)

    def next_simulation(self):
        if self.repetitions - 1 == self.current_repetition:
            return False
        else:
            self.current_repetition += 1
            self.print_simulation()
            return True

    def print_simulation(self):
        print(f'{self.current_repetition+1} - num_agents: {self.num_agents}')