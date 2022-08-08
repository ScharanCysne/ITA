import numpy as np

from constants import *

def distance(drone_0, drone_1):
    pos_x_0, pos_y_0 = drone_0.get_position()
    pos_x_1, pos_y_1 = drone_1.get_position()
    return np.sqrt((pos_x_0 - pos_x_1)**2 + (pos_y_0 - pos_y_1)**2)

class State:
    def __init__(self, n) -> None:
        self.n = n
        self.adjacencyMatrix = np.zeros((n,n))
        self.degreeMatrix = np.zeros((n,n))
        self.laplacianMatrix = np.zeros((n,n))
        self.connectivity = 0

    def isConnected(self, i, j):
        return self.adjacencyMatrix[i][j]

    def updateMatrix(self, swarm):
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
        index = 0 
        for drone in simulation.swarm:
            # checks if drones colided with eachother
            drone.collision_avoidance(simulation.swarm, index)
            drone.check_collision(simulation.swarm,list_obst,index) 
            drone.update()
            # Print if drone reached destination
            if drone.reached_goal(simulation.target_simulation):
                print(f"Drone {index} reached target")
            index += 1
