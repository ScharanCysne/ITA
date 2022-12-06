import time
import pygame
import operator
import numpy as np
import networkx as nx

from constants        import *
from utils            import distance
from constants        import SAMPLE_TIME, SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS, FREQUENCY

class CoverageMissionEnv:
    """Coverage Mission Environment """
    
    def __init__(self, positions, obstacles, queues, logger):
        # Define agents
        self.agents = ["Drone " + str(i) for i in range(NUM_DRONES)]
        self.alive = {i for i in range(NUM_DRONES)}

        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # Environment variables
        self.time_executing = 0
        self.attack_time = np.arange(2, int(0.7 * NUM_DRONES), 1)
        self.queues = queues
        self.positions = [pygame.math.Vector2(p[0], p[1]) for p in positions]
        self.obstacles = [pygame.math.Vector2(o[0], o[1]) for o in obstacles]

        # State Estimator 
        self.state = State(positions, self.alive)
        self.logger = logger
        

    def broadcast(self, data):
        # Broadcasting data for all drones (irrealistic)
        # Used for initialization only
        for idx in range(NUM_DRONES):
            if idx in self.alive:
                self.send_status(idx, data)


    def read_channel(self):
        if not self.queues[-1].empty():
            orig, dest, data = self.queues[-1].get()
            return orig, dest, data
        else:
            return None, None, None


    def send_status(self, idx, data):
        self.queues[idx].put((20, idx, data))


    def parse(self, orig, dest, data):
        self.positions[orig] = data.get('position', self.positions[orig])
        self.leader = data.get('leader', self.leader)
        if self.leader > -1:
            self.positions[self.leader] = self.positions[self.leader] 
    

    def step(self):
        self.time_executing += SAMPLE_TIME
        terminated_node = -1
        infos = {}

        # Generate attack
        if len(self.attack_time) > 0 and self.time_executing > self.attack_time[0]:
            self.attack_time = self.attack_time[1:]
            terminated_node = self.attack_network()
            self.alive.remove(terminated_node)
            self.send_status(terminated_node, {'attack':True})
            infos[terminated_node] = "TERMINATED"
            
        # Get drones' positions
        while True:
            # Read incoming messages
            orig, dest, data = self.read_channel()
            # Check if completed
            if orig is None and dest is None and data is None:
                break
            # Parse incoming message
            self.parse(orig, dest, data)
        # 2. Update swarm state
        self.state.update_state(self.positions, self.alive)
        if terminated_node == self.leader:
                self.leader = self.select_leader()
                infos[self.leader] = "ELECTED LEADER"

        # 3. Broadcast connectivity estimate
        self.broadcast({'connectivity':self.state.algebraic_connectivity})
        self.broadcast({'leader':self.leader})
        for idx in range(NUM_DRONES):
            if idx in self.alive:
                self.send_status(idx, {'bc': self.state.betweenees_centrality})


        # 4. Check completion
        done = self.state.check_completion(self.positions, self.time_executing)

        return done, infos


    def render(self):
        return self.positions, self.state, self.leader, self.alive
        

    def attack_network(self):
        BCs = self.state.calculate_betweenees_centrality()
        return max(BCs.items(), key=operator.itemgetter(1))[0] 


    def select_leader(self):
        BCs = self.state.calculate_betweenees_centrality()
        return min(BCs.items(), key=operator.itemgetter(1))[0] 


class State:
    def __init__(self, positions, alive):
        # Record of drones that are alive and their positions
        self.positions = positions
        self.alive = alive
        
        # Network 
        self.G = nx.Graph()
        self.adjacencyMatrix = np.zeros((NUM_DRONES, NUM_DRONES))
        
        # Global state
        self.algebraic_connectivity = 0
        self.betweenees_centrality = dict()
        self.network_connectivity = 0
        self.network_robustness = 0
        
        # Update graph connectivity
        self.calculate_connectivity()
        # Update graph robustness
        self.calculate_robustness()


    def clear_network(self):
        self.G = nx.Graph()
        self.G.add_nodes_from(self.alive)
        self.adjacencyMatrix = np.zeros((NUM_DRONES, NUM_DRONES))


    def update_state(self, positions, alive):
        self.positions = positions
        self.alive = alive
        # Update graph connectivity
        self.calculate_connectivity()
        # Update graph robustness
        self.calculate_robustness()


    def calculate_connectivity(self):
        # Clear edges from network
        self.clear_network()
        # Get network objects
        for i in range(NUM_DRONES):
            if i not in self.alive: continue
            for j in range(i+1, NUM_DRONES):
                if j not in self.alive: continue
                # Check if they are linked
                connected = distance(self.positions[i], self.positions[j]) < OBSERVABLE_RADIUS
                # Update Adjacency Matrix
                if connected:
                    self.adjacencyMatrix[i][j] = 1 
                    self.adjacencyMatrix[j][i] = 1 
                    # Add edge in networkX graph
                    self.G.add_edge(i, j)
                else:
                    self.adjacencyMatrix[i][j] = 0 
                    self.adjacencyMatrix[j][i] = 0
        # Update Algebraic Connectivity 
        self.algebraic_connectivity = nx.algebraic_connectivity(self.G)
        self.network_connectivity = 1 if self.algebraic_connectivity > 10e-3 else 0


    def calculate_robustness(self):
        self.network_robustness = nx.node_connectivity(self.G) / len(self.alive)


    def calculate_betweenees_centrality(self):
        self.betweenees_centrality = nx.betweenness_centrality(self.G)
        return self.betweenees_centrality


    def check_completion(self, positions, time_executing):
        return True if time_executing > TIME_MAX_SIMULATION else False 
