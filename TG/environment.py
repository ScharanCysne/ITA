import random
import pygame 
import numpy as np

from utils     import distance
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, OBSERVABLE_RADIUS

class Environment(object):
    def __init__(self, num_obstacles, num_agents):
        super().__init__()
        # Environment constraints
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        # Environment variables
        self.num_obstacles = num_obstacles
        self.num_agents = num_agents
        # Network status
        self.adjacencyMatrix = np.zeros((num_agents,num_agents))
        self.degreeMatrix = np.zeros((num_agents,num_agents))
        self.laplacianMatrix = np.zeros((num_agents,num_agents))
        self.connectivity = 0
        # Global state
        self.network_connectivity = 0
        self.network_robustness = 0

    def generate_obstacles(self):
        self.obstacles = []
        for _ in range(self.num_obstacles):
            pos_x = random.uniform(SCREEN_WIDTH*0.1, SCREEN_WIDTH*0.9)
            pos_y = random.uniform(0, SCREEN_HEIGHT)
            self.obstacles.append(pygame.math.Vector2(pos_x, pos_y)) 
                                  
    def get_obstacles(self):
        return self.obstacles

    def isConnected(self, i, j):
        return self.adjacencyMatrix[i][j]

    def update(self, swarm):
        number_drones = len(swarm)
        for i in range(number_drones):
            for j in range(i+1, number_drones):
                connected = distance(swarm[i], swarm[j]) < OBSERVABLE_RADIUS
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

    def scan(self, simulation, list_obst):
        for drone in simulation.swarm:
            # checks if drones colided with eachother
            drone.collision_avoidance(simulation.swarm)
            drone.check_collision(simulation.swarm, list_obst) 
            drone.update()
            # Print if drone reached destination
            if not drone.reached and drone.reached_goal(simulation.target_simulation):
                print(f"Drone {drone.id} reached target")
