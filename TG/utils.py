import copy
import numpy as np
import pygame
import random

from math      import exp 
from constants import *

def distance(x0, y0, x1, y1):
    return np.sqrt((x0 - x1)**2 + (y0 - y1)**2)

def normalFunction(omega, center, position):
    f = exp( -omega*((position.x - center.x) + (position.y - center.y)))
    return f

def bivariateFunction(alpha, beta, center, position):
    '''
        Calculates the bivariate function
        
        position: (x,y)
        center of the function: (xc,yc)
        control variables: Alpha and Beta will control the stringthof the vectors in x and y directions
        return: point in the bivariate function
    '''
    k = 10
    f = exp( -alpha*(position.x - center.x)/k**2 - beta*(position.y - center.y)/k**2 )
    return f
 
def derivativeBivariate(alpha, beta, center, position):
    '''
        Calculates the bivariate function
        
        position: (x,y)
        center of the function: (xc,yc)
        control variables: Alpha and Beta will control the stringthof the vectors in x and y directions
        return: point in the bivariate function
    '''
    f = bivariateFunction(alpha,beta,center,position)
    dx = f * (-2*alpha*(position.x-center.x))
    dy = f * (-2*beta*(position.y-center.y))
    return pygame.math.Vector2(dx,dy)

def constrain_ang(ang, min_angle, max_angle):
    ang = min(ang, max_angle)
    ang = max(ang, min_angle)
    return ang

def random_color():
    """"
        Picks a random color R,G or B

        :return: color picked
        :rtype : tuple
    """
    rgbl = [random.uniform(0,255), random.uniform(0,255), random.uniform(0,255)]
    random.shuffle(rgbl)
    return tuple(rgbl)

def limit(v2, max):
    """
        Limits magnitude of vector2

        :param v2: Vector2 to be normalized
        :type v2: pygame.Vector2
        :param max: maximum length of vector
        :type max: int
        :return v: returns vector 
        :rtype v: vector2
    """
    v = copy.deepcopy(v2)
    if v.length() > max:
        v.scale_to_length(max)
    return v

def constrain(v2,w,h):
    """
        Constrains movement of drone inside the canvas

        :param v2: Vector2 to be constrained
        :type v2: pygame.Vector2
        :param w: maximum width
        :type w: int
        :param h: maximum height
        :type h: int
        :return v2: returns vector within the limits
        :rtype v2: vector2
    """
    v2.x = min(max(v2.x, 0), w)
    v2.y = min(max(v2.y, 0), h)
    return v2


class FlowField():
    def __init__(self, resolution):
        self.cols = SCREEN_WIDTH // resolution    # Cols of the grid
        self.rows = SCREEN_HEIGHT // resolution   # Rows of the grid
        self.resolution = resolution              # Resolution of grid relative to window width and height in pixels
        
        # create grid
        self.field = [[pygame.math.Vector2(random.uniform(0,1),random.uniform(0,1)) for _ in range(self.cols)] for _ in range(self.rows)]  
        
    def draw(self, screen):
        blockSize = self.resolution #Set the size of the grid block
        for x in range(0, SCREEN_WIDTH, blockSize):
            for y in range(0, SCREEN_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)


class NPC(pygame.sprite.Sprite):
    """
        Represents a simple visual animated npc 
        Can load sprites, rotate and update animation
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        #for i in range(1,4):
        self.sprites.append(pygame.image.load(f'model/reddot.png').convert())
        self.sprites[-1] = pygame.transform.rotozoom(self.sprites[-1], 0, 1)

        self.atual = 0
        # inherited from the pygame sprite class it is the first element of the drone
        self.image = self.sprites[self.atual]
        # scales down drone sprites to (70,70)
        # self.image = pygame.transform.scale(self.image,(RADIUS_OBSTACLES,RADIUS_OBSTACLES))
        # rect is inherited from Sprite
        # defines the sprite's position on the screen
        # take the image size
        self.rect = self.image.get_rect()

    def update(self, position, angle, size = SIZE_DRONE* PIX2M):
        
        # animation update speed is controle by this parameter
        self.atual += .001
        if self.atual >= len(self.sprites)-1:
            self.atual = 0

        self.image = self.sprites[round(self.atual)]
    
        # Rotates image -> angle should be in degrees
        # rotozoom(Surface, angle, scale) -> Surface
        #self.image = pygame.transform.rotozoom(self.image, 0, .2)
        self.rect = self.image.get_rect()
        # positions center of rect in acual drone position
        self.rect.midbottom = position.x,position.y+20
