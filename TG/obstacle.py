import random
import pygame as pg

class Obstacles(object):
    def __init__(self, num_of_obstacles, map_size):
        super().__init__()
        self.num_of_obstacles = num_of_obstacles
        self.map_size = map_size
        self.obst = []
        
    def generate_obstacles(self):
        self.obst = []
        for _ in range(self.num_of_obstacles):
            pos_x = random.uniform(0, self.map_size[0])
            pos_y = random.uniform(0, self.map_size[1])
            self.obst.append(pg.math.Vector2(pos_x, pos_y)) 
                                  
    def get_coordenates(self):
        return self.obst
