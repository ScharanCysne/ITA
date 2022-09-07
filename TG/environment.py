import scipy.io
import pygame 
import numpy as np

from gym              import spaces
from utils            import distance
from drone            import Drone
from constants        import SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS
from pettingzoo       import ParallelEnv

class CoverageMissionEnv(ParallelEnv):
    """Coverage Mission Environment that follows PettingZoo Gym interface"""

    """
        State Space:
        - Position [x,y]
        - Vulnerability level of a node v regarding failures: P_\theta(v)
        - Local estimate of algebraic connectivity given a node v: \lambda_v
        - Resulting potential field due to obstacles in agent's position: [F_ox, F_oy]
        - Resulting potential field due to other drones in agent's position: [F_dx, F_dy]

        Total number of states: 8
    """
    N_SPACE = 8
    metadata = {'render.modes': ['human']}

    def __init__(self, num_obstacles, num_agents):
        """
        The init method takes in environment arguments and should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces

        These attributes should not be changed after initialization.
        """
        # Define possible agents
        self.possible_agents = ["Drone " + str(r) for r in range(num_agents)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(num_agents)))
        )
        # Define action and state space
        self.action_spaces = dict(
            zip(self.possible_agents, [spaces.Box(low=np.array([0]),high=np.array([1]), dtype=np.float32) for _ in range(num_agents)])
        )
        self.observation_spaces = dict(
            zip(self.possible_agents, [spaces.Discrete(self.N_SPACE) for _ in range(num_agents)])
        ) 
        
        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        # Environment variables
        self.num_obstacles = num_obstacles
        self.env_state = State(num_agents)
        

    def observation_space(self, agent):
        return self.observation_spaces[agent]


    def action_space(self, agent):
        return self.action_spaces[agent]


    def step(self, actions):
        """
        step(action) takes in an action for each agent and should return the
        - observations
        - rewards
        - dones
        - infos
        dicts where each dict looks like {agent_1: item_1, agent_2: item_2}
        """
        if not actions:
            self.agents = []
            return {}, {}, {}, {}
        


        return {}, {}, {}, {}

        #return states, rewards, done, info


    def reset(self, seed=None, return_info=False, options=None):
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.

        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.

        Returns the observations for each agent
        """

        # Initialize agents and obstacles positions
        self.generate_agents()
        self.generate_obstacles()
        
        observations = self.env_state.get_global_state(self.drones)
        return observations  

    def render(self, mode='human'):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        
        if len(self.agents) == 2:
            string = "Current state: Agent1: {} , Agent2: {}".format(
                MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]
            )
        else:
            string = "Game over"
        print(string)
        """
        pass

    def seed(self, seed=None):
        pass

    def close(self):
        pass

    def generate_agents(self):
        self.agents = self.possible_agents[:]
        self.drones = []
        # Load initial positions
        mat = scipy.io.loadmat(f'model/positions/{np.random.randint(1,200)}/position.mat')
        initial_positions = mat["position"]
        # Create N Drones
        for index in range(self.num_agents):
            drone = Drone(initial_positions[index][0], initial_positions[index][1], index)
            self.drones.append(drone)

    def generate_obstacles(self, random=False):
        self.obstacles = []
        if random:
            for _ in range(self.num_obstacles):
                pos_x = random.uniform(SCREEN_WIDTH*0.1, SCREEN_WIDTH*0.9)
                pos_y = random.uniform(0, SCREEN_HEIGHT)
                self.obstacles.append(pygame.math.Vector2(pos_x, pos_y)) 
        else:
            mat = scipy.io.loadmat(f'model/positions/{np.random.randint(1,200)}/obstacles.mat')
            obstacles_positions = mat["obstacles"]
            for index in range(len(obstacles_positions)):
                self.obstacles.append(pygame.math.Vector2(obstacles_positions[index][0], obstacles_positions[index][1])) 
                                  
    def get_obstacles(self):
        return self.obstacles

    def update(self):
        self.env_state.update_state(self.agents)
        
    def scan(self, simulation, list_obst):
        for drone in simulation.swarm:
            # checks if drones colided with eachother
            drone.collision_avoidance(simulation.swarm)
            drone.check_collision(simulation.swarm, list_obst) 
            drone.update()
            # Print if drone reached destination
            if not drone.reached and drone.reached_goal(simulation.target_simulation):
                print(f"Drone {drone.id} reached target")

class State:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        # Network status
        self.adjacencyMatrix = np.zeros((num_agents,num_agents))
        self.degreeMatrix = np.zeros((num_agents,num_agents))
        self.laplacianMatrix = np.zeros((num_agents,num_agents))
        self.connectivity = 0
        # Global state
        self.network_connectivity = 0
        self.network_robustness = 0


    def update_state(self, agents):
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


    def isConnected(self, i, j):
        return self.adjacencyMatrix[i][j]


    def get_global_state(self, agents):
        """
        State Space:
        - Position [x,y]
        - Vulnerability level of a node v regarding failures: P_\theta(v)
        - Local estimate of algebraic connectivity given a node v: \lambda_v
        - Resulting potential field due to obstacles in agent's position: [F_ox, F_oy]
        - Resulting potential field due to other drones in agent's position: [F_dx, F_dy]

        Total number of states: 8
        """
        self.update_state(agents)
        self.observations = dict()
        for agent in agents:
            self.observations[agent.name] = agent.get_state()
        return self.observations


    def get_state(self, agent):
        """
        State Space:
        - Position [x,y]
        - Vulnerability level of a node v regarding failures: P_\theta(v)
        - Local estimate of algebraic connectivity given a node v: \lambda_v
        - Resulting potential field due to obstacles in agent's position: [F_ox, F_oy]
        - Resulting potential field due to other drones in agent's position: [F_dx, F_dy]

        Total number of states: 8
        """
        return self.observations[agent.name]
