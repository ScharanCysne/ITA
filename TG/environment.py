import scipy.io
import pygame 
import random
import scipy.io
import numpy as np
import functools

from gym              import spaces
from utils            import distance
from drone            import Drone
from constants        import SAMPLE_TIME, SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS, FREQUENCY
from pettingzoo       import ParallelEnv

class CoverageMissionEnv(ParallelEnv):
    """Coverage Mission Environment that follows PettingZoo Gym interface"""
    metadata = {'render.modes': ['human']}
    N_SPACE = 8

    def __init__(self, num_obstacles, num_agents):
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
        # Define possible agents
        self.possible_agents = ["Drone " + str(i) for i in range(num_agents)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(num_agents)))
        )
        
        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.target = SCREEN_WIDTH

        # Environment variables
        self.num_obstacles = num_obstacles
        self.env_state = State(num_agents)


    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # Define state space (pos_x, pos_y, vulnerability, connectivity, obstacles_x, obstacles_y, neighbors_x, neighbors_y)
        return spaces.Box(low=np.zeros(self.N_SPACE), high=np.ones(self.N_SPACE), dtype=np.float64)


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
            self.drones[id].execute(action)
            
        # 2. Update swarm state
        self.env_state.update_state(self.drones)

        # 3. Retrieve swarm state
        observations = self.env_state.get_global_state(self.agents, self.agents_mapping)

        # 4. Check completion
        dones = self.env_state.check_completion(self.agents, self.agents_mapping)

        # 5. Calculate rewards
        rewards = self.env_state.calculate_rewards(self.agents, self.agents_mapping)

        infos = {agent: {} for agent in self.agents}

        # Update alive agents
        self.agents = [agent for agent in self.agents if not dones[agent]]

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
        
        # Reset observations
        self.env_state.update_state(self.drones)
        observations = self.env_state.get_global_state(self.agents, self.agents_mapping)
        return observations  


    def render(self, mode='human'):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        return self.drones, self.obstacles, self.env_state, self.num_agents
        

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
        mat = scipy.io.loadmat(f'model/positions/{np.random.randint(1,200)}/position.mat')
        initial_positions = self.rescale(mat["position"])
        # Create N Drones
        for index in range(self.num_agents):
            drone = Drone(initial_positions[index][0], initial_positions[index][1], index)
            self.drones.append(drone)
            self.agents_mapping[drone.name] = drone


    def generate_obstacles(self, deterministic=True):
        self.obstacles = []
        if deterministic:
            mat = scipy.io.loadmat(f'model/positions/{np.random.randint(1,200)}/obstacles.mat')
            obstacles_positions = self.rescale(mat["obstacles"])
            for index in range(len(obstacles_positions)):
                self.obstacles.append(pygame.math.Vector2(obstacles_positions[index][0], obstacles_positions[index][1])) 
        else:
            for _ in range(self.num_obstacles):
                pos_x = random.uniform(SCREEN_WIDTH*0.1, SCREEN_WIDTH*0.9)
                pos_y = random.uniform(0, SCREEN_HEIGHT)
                self.obstacles.append(pygame.math.Vector2(pos_x, pos_y)) 


    def rescale(self, positions):
        pos_max_x = max([position[0] for position in positions])
        pos_max_y = max([position[1] for position in positions])
        ratio_width = self.width / pos_max_x
        ratio_height = self.height / pos_max_y 
        for position in positions:
            position[0] *= 0.9*ratio_width
            position[1] *= ratio_height
        return positions


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
        self.connectivity = 0
        # Global state
        self.network_connectivity = 0
        self.network_robustness = 0


    def update_state(self, agents):
        self.agents = agents
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
        self.connectivity = eigenvalues[1]
        self.network_connectivity = 1 if self.connectivity else 0


    def isConnected(self, i, j):
        return self.adjacencyMatrix[i][j]


    def get_global_state(self, alive_agents, agents_mapping):
        self.observations = dict()
        for name in alive_agents:
            agent = agents_mapping[name]
            self.observations[agent.name] = agent.get_state() if agent.alive else None
            self.observations[agent.name][2] = self.network_robustness / 100
            self.observations[agent.name][3] = self.network_connectivity / 100
        return self.observations


    def check_completion(self, alive_agents, agents_mapping):
        dones = dict()
        env_done = True
        for name in alive_agents:
            if not agents_mapping[name].reached_goal():
                env_done = False 
        dones = {agent : env_done for agent in alive_agents}
        return dones

    
    def calculate_rewards(self, alive_agents, agents_mapping):
        rewards = dict()
        for name in alive_agents:
            agent = agents_mapping[name]
            rewards[agent.name] = - agent.location[0] / self.target    # Rate of completition
            rewards[agent.name] += 0    # add reward to connection failure
        return rewards