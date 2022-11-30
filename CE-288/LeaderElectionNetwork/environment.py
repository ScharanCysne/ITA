import math
import pygame
import scipy.io
import operator
import numpy as np
import networkx as nx

from constants        import *
from utils            import distance
from drone            import Drone
from constants        import SAMPLE_TIME, SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS, FREQUENCY

class CoverageMissionEnv():
    """Coverage Mission Environment """
    
    def __init__(self):
        # Load initial positions
        index = np.random.randint(1,200) 
        positions = scipy.io.loadmat(f'model/positions/{index}/position.mat')["position"]
        obstacles = scipy.io.loadmat(f'model/positions/{index}/obstacles.mat')["obstacles"]
        obstacles = [pygame.math.Vector2(obs[0], 2*obs[1]) for obs in obstacles]

        # Create 20 initial Drones
        agents = []
        for index in range(NUM_DRONES):
            agents.append(Drone(positions[index], index, obstacles))

        # Define agents
        self.agents = ["Drone " + str(i) for i in range(20)]
        self.agent_name_mapping = dict(
            zip(self.agents, agents)
        )
        
        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # Environment variables
        self.obstacles = obstacles
        self.state = State(NUM_DRONES)
        self.attack_time = np.arange(2, int(0.7 * NUM_DRONES), 1)
        self.time_executing = 0
        self.state.update_state(self.agent_name_mapping)

        self.leader = self.select_leader()
        self.last_known_position = self.agent_name_mapping[self.leader].location


    def reset(self, index):
        # Load initial positions
        positions = scipy.io.loadmat(f'model/positions/{index+1}/position.mat')["position"]
        obstacles = scipy.io.loadmat(f'model/positions/{index+1}/obstacles.mat')["obstacles"]
        obstacles = [pygame.math.Vector2(obs[0], 2*obs[1]) for obs in obstacles]

        # Create 20 initial Drones
        agents = []
        for index in range(NUM_DRONES):
            agents.append(Drone(positions[index], index, obstacles))

        # Define agents
        self.agents = ["Drone " + str(i) for i in range(20)]
        self.agent_name_mapping = dict(
            zip(self.agents, agents)
        )

        # Environment variables
        self.obstacles = obstacles
        self.state = State(NUM_DRONES)
        self.attack_time = np.arange(2, int(0.7 * NUM_DRONES), 1)
        self.time_executing = 0
        self.state.update_state(self.agent_name_mapping)

        self.leader = self.select_leader()
        self.last_known_position = self.agent_name_mapping[self.leader].location


    def step(self):
        self.time_executing += SAMPLE_TIME
        # Get drones positions
        neighbors_positions = [agent.location for agent in self.agent_name_mapping.values()]
        # Guideline
        guideline = pygame.math.Vector2(1,0)
        # If leader alive
        if self.leader in self.agent_name_mapping and self.state.network_connectivity:
            self.last_known_position = self.agent_name_mapping[self.leader].location

        # 1. Execute actions
        for name in self.agents:
            if name in self.agent_name_mapping:
                agent = self.agent_name_mapping[name]
                # Calculate acceleration given potential field and execute action
                agent.calculate_potential_field(neighbors_positions) 
                agent.execute(guideline, self.state.network_connectivity, self.last_known_position)
        
        # 2. Update swarm state
        self.state.update_state(self.agent_name_mapping)

        # 4. Check completion
        dones = self.state.check_completion(self.agent_name_mapping, self.agents, self.time_executing)

        # 6. Return Infos
        infos = {agent:{} for agent in self.agents}

        # Generate attack
        if len(self.attack_time) > 0 and self.time_executing > self.attack_time[0]:
            self.attack_time = self.attack_time[1:]
            terminated_node = self.attack_network()
            del self.agent_name_mapping[terminated_node] 
            if terminated_node == self.leader:
                self.leader = self.select_leader()

        # Update alive agents
        self.agents = [agent for agent in self.agents if not dones[agent]]

        return dones, infos


    def render(self):
        return self.agent_name_mapping, self.obstacles, self.state, self.leader
        

    def seed(self, seed=None):
        pass


    def close(self):
        pass


    def attack_network(self):
        BCs = self.state.calculate_betweenees_centrality()
        return max(BCs.items(), key=operator.itemgetter(1))[0] 


    def select_leader(self):
        BCs = self.state.calculate_betweenees_centrality()
        return min(BCs.items(), key=operator.itemgetter(1))[0] 


    def update(self):
        self.state.update_state(self.agents)
        

class State:
    def __init__(self, num_agents):
        self.agents = []
        self.num_agents = num_agents
        # Network 
        self.G = nx.Graph()
        self.adjacencyMatrix = np.zeros((num_agents,num_agents))
        # Global state
        self.algebraic_connectivity = 0
        self.betweenees_centrality = dict()
        self.network_connectivity = 0
        self.network_robustness = 0
        self.network_coverage = 0
        self.possible_coverage = num_agents * math.pi * OBSERVABLE_RADIUS**2
        self.cm = 0


    def clear_network(self):
        self.G = nx.Graph()
        self.G.add_nodes_from(self.agents.keys())


    def update_state(self, agents):
        self.agents = agents
        # Update graph connectivity
        self.calculate_connectivity()
        # Update graph robustness
        self.calculate_robustness()


    def calculate_connectivity(self):
        # Clear edges from network
        self.clear_network()
        # Get network objects
        drones = list(self.agents.values())
        self.num_agents = len(drones)
        for i in range(self.num_agents):
            for j in range(i+1, self.num_agents):
                # Check if they are linked
                connected = distance(drones[i], drones[j]) < OBSERVABLE_RADIUS
                idx_i = drones[i].id
                idx_j = drones[j].id
                # Update Adjacency Matrix
                if connected:
                    self.adjacencyMatrix[idx_i][idx_j] = 1 
                    self.adjacencyMatrix[idx_j][idx_i] = 1 
                    # Add edge in networkX graph
                    self.G.add_edge(drones[i].name, drones[j].name)
                else:
                    self.adjacencyMatrix[idx_i][idx_j] = 0 
                    self.adjacencyMatrix[idx_j][idx_i] = 0
        # Update Algebraic Connectivity 
        self.algebraic_connectivity = nx.algebraic_connectivity(self.G)
        self.network_connectivity = 1 if self.algebraic_connectivity > 10e-3 else 0


    def calculate_robustness(self):
        self.network_robustness = nx.node_connectivity(self.G) / self.num_agents


    def calculate_betweenees_centrality(self):
        self.betweenees_centrality = nx.betweenness_centrality(self.G)
        return self.betweenees_centrality


    def check_completion(self, agents, possible_agents, time_executing):
        dones = dict()
        env_done = True if time_executing > TIME_MAX_SIMULATION else False 
        dones = { agent:env_done for agent in possible_agents }
        return dones
