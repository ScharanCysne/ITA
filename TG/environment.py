import math
import time
import pygame 
import scipy.io
import numpy as np
import functools

from constants        import *
from gym              import spaces
from utils            import distance, intersection
from drone            import Drone
from constants        import SAMPLE_TIME, SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS, FREQUENCY
from pettingzoo       import ParallelEnv

from stable_baselines3.common.monitor import ResultsWriter

writer = ResultsWriter(
    "tmp/3_5000",
    header={"t_start": 0, "env_id": 0 }
)

class CoverageMissionEnv(ParallelEnv):
    """Coverage Mission Environment that follows PettingZoo Gym interface"""
    metadata = {'render.modes': ['human']}
    N_SPACE = 8

    def __init__(self, num_obstacles, num_agents, enable_target=False, enable_obstacles=True):
        """
        The init method takes in environment arguments and define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces

        These attributes should not be changed after initialization.

        State Space:
        - Position [x,y]
        - Vulnerability level of a node v regarding failures: P_\theta(v)
        - Local estimate of algebraic connectivity given a node v: \lambda_v
        - Resulting potential field due to obstacles in agent's position: [F_ox, F_oy]
        - Resulting potential field due to other drones in agent's position: [F_dx, F_dy]
        
        Total number of states: 8
        
        Actions Space:
        - velocity in x axis
        - velocity in y axis
        """
        # Monitor parameters
        self.spec = 0
        self.t_start = time.time()

        # Define possible agents
        self.possible_agents = ["Drone " + str(i) for i in range(num_agents)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(num_agents)))
        )
        self.num_drones = num_agents
        
        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.target = SCREEN_WIDTH

        # Environment variables
        self.enable_target = enable_target
        self.enable_obstacles = enable_obstacles
        self.num_obstacles = num_obstacles
        self.env_state = State(num_agents)
        self.cummulative_rewards = { agent:0 for agent in self.possible_agents }
        self.target_algebraic_connectivity = 0


    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # Define state space (pos_x, pos_y, vulnerability, connectivity, obstacles_x, obstacles_y, neighbors_x, neighbors_y)
        return spaces.Box(low=np.zeros(self.N_SPACE), high=np.array([10]*self.N_SPACE), dtype=np.float64)

    
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # Define action space (vel_x, vel_y)
        return spaces.Box(low=np.array([0, 0]), high=np.array([1, 1]), dtype=np.float64)


    def step(self, actions: dict):
        """
        step(action) takes in an action for each agent and should return the
        - observations
        - rewards
        - dones
        - infos

        Inputs and outputs are dicts where each dict looks like {agent_1: item_1, agent_2: item_2}
        """
        self.time_executing += SAMPLE_TIME

        if not actions:
            self.agents = []
            return {}, {}, {}, {}

        # Get drones positions
        neighbors_positions = [drone.location for drone in self.drones]
        obstacles_positions = self.obstacles

        # 1. Execute actions
        for agent, action in actions.items():
            id = self.agent_name_mapping[agent]
            # Calculate acceleration given potential field and execute action
            self.drones[id].scan_neighbors(neighbors_positions)
            self.drones[id].scan_obstacles(obstacles_positions)
            self.drones[id].calculate_potential_field(neighbors_positions, obstacles_positions) 
            self.drones[id].execute(action, obstacles_positions, self.drones, self.enable_target)
            
        # 2. Update swarm state
        self.env_state.update_state(self.drones)

        # 3. Retrieve swarm state
        observations = self.env_state.get_global_state(self.agents, self.agents_mapping)

        # 4. Check completion
        dones = self.env_state.check_completion(self.agents, self.agents_mapping, self.time_executing)

        # 5. Calculate rewards
        rewards = self.env_state.calculate_rewards(self.agents, self.agents_mapping, observations, self.target_algebraic_connectivity)

        infos = {agent: {} for agent in self.agents}

        # Update alive agents
        self.agents = [agent for agent in self.agents if not dones[agent]]

        # Monitor current performance
        self.monitor(dones, rewards) 

        return observations, rewards, dones, infos


    def reset(self, seed=None, return_info=False, options=None):
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.

        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.

        Returns the observations for each agent
        """

        # Time executing
        self.time_executing = 0

        # Initialize agents and obstacles positions
        self.generate_agents()
        self.generate_obstacles()
        self.cummulative_rewards = { agent:0 for agent in self.possible_agents }
        
        # Reset observations
        self.env_state.update_state(self.drones)
        observations = self.env_state.get_global_state(self.agents, self.agents_mapping)
        return observations  


    def render(self, mode='human'):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        return self.drones, self.obstacles, self.env_state, self.num_agents, self.time_executing
        

    def monitor(self, dones, rewards):
        # Update episode cummulative reward
        for agent in rewards:
            self.cummulative_rewards[agent] += rewards[agent]
        # Check if episode is finished
        alldone = True 
        for agent in dones:
            if not dones[agent]:
                alldone = False 

        # If all done, record episode rewards
        if alldone:
            ep_rew = sum([reward for reward in self.cummulative_rewards.values()])
            ep_len = self.time_executing
            ep_info = {"r": round(ep_rew, 6), "l": ep_len, "t": round(time.time() - self.t_start, 6)}
            writer.write_row(ep_info)
    

    def seed(self, seed=None):
        pass


    def close(self):
        pass


    def generate_agents(self):
        # Create new swarm of drones
        self.agents = self.possible_agents[:]
        self.drones = []
        self.agents_mapping = dict()
        # Load initial positions
        index = 18 #np.random.randint(1,200)
        positions = scipy.io.loadmat(f'model/positions/{index}/position.mat')["position"]
        properties = scipy.io.loadmat(f'model/positions/{index}/properties.mat')['properties']
        self.target_algebraic_connectivity = properties[0][4]
        # Create N Drones
        for index in range(self.num_agents):
            drone = Drone(positions[index][0], positions[index][1], index)
            self.drones.append(drone)
            self.agents_mapping[drone.name] = drone


    def generate_specific_obstacle(self, positions):
        self.obstacles = []
        for x, y in positions:
            self.obstacles.append(pygame.math.Vector2(x, y))


    def generate_obstacles(self, deterministic=True):
        self.obstacles = []
        if self.enable_obstacles:
            mat = scipy.io.loadmat(f'model/positions/{np.random.randint(1,200)}/obstacles.mat')
            obstacles_positions = mat["obstacles"]
            for index in range(len(obstacles_positions)):
                self.obstacles.append(pygame.math.Vector2(obstacles_positions[index][0], obstacles_positions[index][1])) 
        

    def get_obstacles(self):
        return self.obstacles


    def update(self):
        self.env_state.update_state(self.agents)
        

class State:
    def __init__(self, num_agents):
        self.agents = []
        self.num_agents = num_agents
        self.target = SCREEN_WIDTH
        # Network status
        self.adjacencyMatrix = np.zeros((num_agents,num_agents))
        self.degreeMatrix = np.zeros((num_agents,num_agents))
        self.laplacianMatrix = np.zeros((num_agents,num_agents))
        self.algebraic_connectivity = 0
        # Global state
        self.network_connectivity = 0
        self.network_robustness = 0
        self.network_coverage = 0
        self.possible_coverage = num_agents * math.pi * OBSERVABLE_RADIUS**2
        self.cm = 0


    def update_state(self, agents):
        self.agents = agents
        # Update graph robustness
        self.calculate_robustness(agents)
        # Update graph connectivity
        self.calculate_connectivity(agents)
        # Update graph area coverage
        self.calculate_coverage(agents)
        # Update CM of topology
        self.cm = self.calculate_center(agents)


    def calculate_center(self, agents):
        cm = pygame.Vector2(0,0)
        for agent in agents:
            cm += agent.location 
        return cm / len(agents)


    def calculate_connectivity(self, agents):
        for i in range(self.num_agents):
            for j in range(i+1, self.num_agents):
                connected = distance(agents[i], agents[j]) < OBSERVABLE_RADIUS
                # Update Adjacency Matrix
                self.adjacencyMatrix[i][j] = 1 if connected else 0
                self.adjacencyMatrix[j][i] = 1 if connected else 0
            # Update Degree Matrix
            self.degreeMatrix[i][i] = np.sum(self.adjacencyMatrix[i])
        # Update Laplacian Matrix
        self.laplacianMatrix = self.degreeMatrix - self.adjacencyMatrix
        eigenvalues, _ = np.linalg.eig(self.laplacianMatrix)
        eigenvalues.sort()
        self.algebraic_connectivity = eigenvalues[1] if type(eigenvalues[1]) == np.float64 else 0
        self.network_connectivity = 1 if self.algebraic_connectivity > 10e-3 else 0


    def calculate_robustness(self, agents):
        pass


    def calculate_coverage(self, agents):
        # compute the bounding box of the circles
        x_min = min(agent.location[0] - OBSERVABLE_RADIUS for agent in agents)
        x_max = min(agent.location[0] + OBSERVABLE_RADIUS for agent in agents)
        y_min = min(agent.location[1] - OBSERVABLE_RADIUS for agent in agents)
        y_max = min(agent.location[1] + OBSERVABLE_RADIUS for agent in agents)
        # Precision
        box_side = 40
        # Size of bounding box
        dx = (x_max - x_min) / box_side
        dy = (y_max - y_min) / box_side
        # Count of small blocks
        count = 0

        for r in range(box_side):
            y = y_min + r * dy
            for c in range(box_side):
                x = x_min + c * dx
                if any((agent.location - pygame.math.Vector2(x,y)).magnitude() <= OBSERVABLE_RADIUS for agent in agents):
                    count += 1
        self.network_coverage = count * dx * dy


    def is_connected(self, i, j):
        return self.adjacencyMatrix[i][j]


    def get_global_state(self, alive_agents, agents_mapping):
        self.observations = dict()
        for name in alive_agents:
            agent = agents_mapping[name]
            self.observations[name] = agent.get_state() if agent.alive else None
            self.observations[name][2] = self.network_robustness / 100
            self.observations[name][3] = self.algebraic_connectivity / self.num_agents
        return self.observations


    def check_completion(self, alive_agents, agents_mapping, time_executing):
        dones = dict()
        env_done = False
        for name in alive_agents:
            if not agents_mapping[name].reached_goal():
                env_done = False
        if time_executing > TIME_MAX_SIMULATION:
            env_done = True 
        #if self.network_connectivity == 0:
        #    env_done = True 
        dones = {agent : env_done for agent in alive_agents}
        return dones

    
    def calculate_rewards(self, alive_agents, agents_mapping, states, target_connectivity):
        rewards = dict()
        for name in alive_agents:
            agent = agents_mapping[name]
            # Connectivity Controller
            # if self.network_connectivity == 1: 
            # Coverage Controller - try to maximize coverage area
            #rewards[name] = self.network_coverage / self.possible_coverage / self.num_agents
            # Try to maintain delta in y axis - not to form a line
            rewards[name] = abs(agent.location[1] - self.cm[1]) / SCREEN_HEIGHT
            # Algebraic connectivity is bounded 0 < K < vertices - 1, the higher the better
            if self.network_connectivity == 1: # and self.algebraic_connectivity >= target_connectivity:
                # Reward if above threshold
                rewards[name] += 1 / self.num_agents
            #elif self.network_connectivity == 1:
            #    # Neutral Reward if connected, but not as high if above threshold
            #    rewards[name] += 0.001 
            #else:
            #    rewards[name] = PENALTY_DISCONNECTED / self.num_agents
            # Walking in border penalty
            if agent.location[1] == 50 or agent.location[1] == 0 or agent.location[0] == 0:
                rewards[name] += PENALTY_STEP
        
        return rewards