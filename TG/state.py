import numpy as np

from constants import *

def distance(drone_0, drone_1):
    pos_x_0, pos_y_0 = drone_0.get_position()
    pos_x_1, pos_y_1 = drone_1.get_position()
    return np.sqrt((pos_x_0 - pos_x_1)**2 + (pos_y_0 - pos_y_1)**2)

class State:
    def __init__(self, n) -> None:
        self.n = n
        self.adjacencyMatrix = [[False for _ in range(n)] for _ in range(n)]
        for i in range(n):
            self.adjacencyMatrix[i][i] = True

    def isConnected(self, i, j):
        return self.adjacencyMatrix[i][j]

    def updateMatrix(self, swarm):
        number_drones = len(swarm)
        for i in range(number_drones):
            for j in range(i+1, number_drones):
                connected = distance(swarm[i], swarm[j]) < OBSERVABLE_RADIUS
                # keep matrix symetric
                self.adjacencyMatrix[i][j] = connected
                self.adjacencyMatrix[j][i] = connected