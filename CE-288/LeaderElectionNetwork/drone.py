import time
import pygame 
import logging 

import numpy as np

from math      import sqrt 
from utils     import limit, constrain
from constants import *

ENV_CHANNEL = 20

class Drone:
    def __init__(self, idx, positions, obstacles, queues, logger):
        """
            Idealized class representing a drone
            :param x and y: represents inicial position 
        """

        # Variables used to move drone
        pos = positions[idx] 
        self.position = pygame.math.Vector2(pos[0], pos[1]) * 2 
        self.velocity = pygame.math.Vector2(0,0) 
        self.acceleration = pygame.math.Vector2(0,0)
        self.reached = False
        self.alive = True

        # Agent Variables
        self.id = idx
        self.name = "Drone " + str(idx)
        self.positions = [pygame.math.Vector2(p[0], p[1]) for p in positions]
        self.obstacles = [pygame.math.Vector2(o[0], o[1]) for o in obstacles]
        self.betweenness = 0
        self.connectivity = 0
        
        # State variables
        self.leader = -1
        self.leader_position = pygame.math.Vector2(0,0)
        self.guideline = pygame.math.Vector2(1,0)
        self.state = FOLLOWER
        self.election = False

        # Initialize
        self.time_executing = 0
        self.timestamps = {i:0 for i in range(NUM_DRONES)}
        self.logger = logger
        self.queues = queues
        self.run()


    def read_channel(self):
        try:
            if not self.queues[self.id].empty():
                orig, dest, data = self.queues[self.id].get()
                return orig, dest, data
            else:
                return None, None, None
        except Exception as e:
            self.logger.error(e)


    def send_status(self, idx, data):
        try:
            self.queues[idx].put((self.id, idx, data))
        except Exception as e:
            self.logger.error(e)


    def parse(self, orig, dest, data):
        try:
            self.timestamps[orig] = self.time_executing
            self.leader = data.get('leader', self.leader)
            self.leader_position = self.positions[self.leader] if self.leader > -1 else self.leader_position
            self.alive = data.get('attack', self.alive)
            self.connectivity = data.get('connectivity', self.connectivity)
            self.betweenness = data.get('bc', self.betweenness)
            if orig != self.id:
                self.positions[orig] = data.get('position', self.positions[orig])
            self.guideline = data.get('guideline', self.guideline)
        except Exception as e:
            self.logger.error(e)
    

    def gossip(self):
        try:
            # Send own position first
            self.send_status(ENV_CHANNEL, {'position': self.position})
            for idx in range(NUM_DRONES):
                # Gossip
                if self.leader == idx:
                    self.send_status(idx, {'position': self.position, 'guideline': self.guideline})
                else:
                    self.send_status(idx, {'position': self.position})
            
            while True:
                # Read incoming messages
                orig, dest, data = self.read_channel()
                # Check if completed
                if orig is None and dest is None and data is None:
                    break
                # Parse incoming message
                self.parse(orig, dest, data)
        except Exception as e:
            self.logger.error(e)    
            

    def run(self):
        self.logger.info(f"INIT Drone {self.id}")
        try:
            while self.alive and self.position[0] < THRESHOLD_TARGET and self.time_executing < TIME_MAX_SIMULATION:
                self.time_executing += SAMPLE_TIME
                # Check if leader is alive
                if self.leader in self.alive:
                    # Communicate position
                    self.gossip()
                    # Calculate potential field in its position
                    self.calculate_potential_field() 
                else:
                    # Start new Election
                    self.election = True
                    self.state = CANDIDATE
                # Act
                self.execute()
                # Set next state
                self.next()
                time.sleep(1/FREQUENCY)
        except Exception as e:
            self.logger.error(e)
        self.logger.info(f"CLOSE Drone {self.id}")
    

    def apply_force(self, force):
        self.acceleration += force/MASS 


    def next(self):
        if self.state == LEADER:
            # Stays as leader until failure (upgrade: check if there is a better leader)
            self.state = LEADER 
        elif self.state == FOLLOWER:
            if self.leader == self.id:
                self.state = LEADER
            # if didnt received heartbeat: self.state = CANDIDATE
            if abs(self.time_executing - self.timestamps.get(self.leader, 0)) > 1:
                self.state == CANDIDATE
            else:   
                self.state = FOLLOWER
        elif self.state == CANDIDATE:
            # if election over and won: self.state = LEADER
            if self.election == False and self.leader == self.id:
                self.state = LEADER
            # elif election over and didnt win: self.state = FOLLOWER
            elif self.election == False and self.leader != self.id:
                self.state = FOLLOWER
            # elif election not over: 
            else: 
                self.state = CANDIDATE


    def execute(self):
        """
            Execute action
            Suffer effects from the environment
        """
        try:
            if self.state == LEADER:
                if self.connectivity > 0:
                    # Define guideline
                    self.guideline = pygame.math.Vector2(1,0)
                    # Step
                    self.velocity += self.acceleration + self.guideline
                else:
                    # Define guideline
                    self.guideline = pygame.math.Vector2(0,0)
                    # Step
                    self.velocity = pygame.math.Vector2(0,0)
            elif self.state == FOLLOWER:
                if self.connectivity > 0:
                    # Follow leader's guidelines
                    self.velocity += self.acceleration + self.guideline 
                else:
                    # Regroup behavior
                    self.velocity = self.leader_position - self.position
            elif self.state == CANDIDATE:
                # Raft
                for idx in range(NUM_DRONES):
                    self.send_status(idx)
            # Limit velocity
            self.velocity = limit(self.velocity, FORWARD_SPEED)
            # Updates position
            self.position += self.velocity 
            # Constrains position to limits of screen 
            self.position = constrain(self.position, UPPER_X, UPPER_Y)
            # Reset acceleration
            self.acceleration *= 0
            
        except Exception as e:
            self.logger.error(e)
    

    def calculate_potential_field(self):
        """
            Determine resulting potential field given obstacles and other drones
        """
        try:
            # --- Repulsion drones
            for position in self.positions:
                distance = (self.position - position).magnitude()
                if 0 < distance < OBSERVABLE_RADIUS:
                    # Proporcional to the distance. The closer the stronger needs to be
                    f_repulsion = (position - self.position).normalize() / distance 
                    self.apply_force(-f_repulsion)

            # --- Repulsion obstacles 
            for pos_x, pos_y in self.obstacles:
                position = pygame.math.Vector2(pos_x, pos_y)
                distance = (self.position - position).magnitude()
                if 0 < distance < OBSERVABLE_RADIUS:
                    # Proporcional to the distance. The closer the stronger needs to be
                    f_repulsion = 3 * (position - self.position).normalize() / sqrt(distance)
                    self.apply_force(-f_repulsion)

            # --- Repulsion walls
            # Distance to Bottom
            distance = UPPER_Y - self.position[1] 
            # Proporcional to the distance. The closer the stronger needs to be
            if distance > 0:
                f_repulsion = pygame.math.Vector2(0,2) / sqrt(distance)
            else:
                f_repulsion = pygame.math.Vector2(0,2) * SEEK_FORCE
            self.apply_force(-f_repulsion)
            
            # Distance to Top
            distance = self.position[1] - LOWER_Y 
            # Proporcional to the distance. The closer the stronger needs to be
            if distance > 0:
                f_repulsion = pygame.math.Vector2(0,-2) / sqrt(distance)
            else:
                f_repulsion = pygame.math.Vector2(0,-2) * SEEK_FORCE
            self.apply_force(-f_repulsion)
        except Exception as e:
            self.logger.error(e)
    