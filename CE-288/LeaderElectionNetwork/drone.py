import pygame 

from math      import sqrt 
from utils     import limit, constrain
from constants import *

class Drone():
    def __init__(self, pos, index, obstacles):
        """
            Idealized class representing a drone
            :param x and y: represents inicial position 
        """
        # Variables used to move drone 
        self.location = pygame.math.Vector2(pos[0], pos[1]) * 2 
        self.velocity = pygame.math.Vector2(0,0) 
        self.acceleration = pygame.math.Vector2(0,0)
        self.reached = False
        self.alive = True

        # Variables related to State Machine
        self.id = index
        self.name = "Drone " + str(index)

        # State variables
        self.leader = pygame.math.Vector2(0,0)
        self.obstacles = obstacles
        self.vulnerability = 0
        self.connectivity = 0


    def reached_goal(self):
        self.reached = THRESHOLD_TARGET < self.location[0]
        return self.reached


    def applyForce(self, force):
        self.acceleration += force/MASS 


    def execute(self, guideline, connectivity, leader):
        """
            Execute action
            Suffer effects from the environment
        """
        # Check connectivity - regroup if disconnected, follow leader's guideline if not
        # Updates velocity at every step and limits it to max_speed
        if connectivity:
            self.velocity += self.acceleration + guideline + (leader - self.location) / 100
        else:
            self.velocity = leader - self.location
        # Limit velocity
        self.velocity = limit(self.velocity, FORWARD_SPEED)
        # Updates position
        self.location += self.velocity 
        # Constrains position to limits of screen 
        self.location = constrain(self.location, UPPER_X, UPPER_Y)
        self.acceleration *= 0
                

    def calculate_potential_field(self, pos_drones):
        """
            Determine resulting potential field given obstacles and other drones
        """
        # --- Repulsion drones
        for position in pos_drones:
            distance = (self.location - position).magnitude()
            if 0 < distance < OBSERVABLE_RADIUS:
                # Proporcional to the distance. The closer the stronger needs to be
                f_repulsion = (position - self.location).normalize() / distance 
                self.applyForce(-f_repulsion)

        # --- Repulsion obstacles 
        for pos_x, pos_y in self.obstacles:
            position = pygame.math.Vector2(pos_x, pos_y)
            distance = (self.location - position).magnitude()
            if 0 < distance < OBSERVABLE_RADIUS:
                # Proporcional to the distance. The closer the stronger needs to be
                f_repulsion = 3 * (position - self.location).normalize() / sqrt(distance)
                self.applyForce(-f_repulsion)

        # --- Repulsion walls
        # Distance to Bottom
        distance = UPPER_Y - self.location[1] 
        # Proporcional to the distance. The closer the stronger needs to be
        if distance > 0:
            f_repulsion = pygame.math.Vector2(0,2) / sqrt(distance)
        else:
            f_repulsion = pygame.math.Vector2(0,2) * SEEK_FORCE
        self.applyForce(-f_repulsion)
        
        # Distance to Top
        distance = self.location[1] - LOWER_Y 
        # Proporcional to the distance. The closer the stronger needs to be
        if distance > 0:
            f_repulsion = pygame.math.Vector2(0,-2) / sqrt(distance)
        else:
            f_repulsion = pygame.math.Vector2(0,-2) * SEEK_FORCE
        self.applyForce(-f_repulsion)