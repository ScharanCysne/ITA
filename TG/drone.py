import copy 
import random
import pygame 

from math      import cos, sin, atan2
from utils     import limit, constrain, derivativeBivariate
from constants import *

class Drone(object):
    def __init__(self, x, y, behavior):
        """
            idealized Drone representing a drone

            :param x and y: represents inicial target 
            :param behavior: State Machine 
        """

        # Variables used to move drone 
        self.location = pygame.math.Vector2(x,y) # Random position in screen
        self.velocity = pygame.math.Vector2(0.1,0) # Inicial speed
        self.target = SCREEN_WIDTH
        self.acceleration = pygame.math.Vector2(0,0)
        self.radius = SIZE_DRONE # Drone Size
        self.desired = pygame.math.Vector2()

        self.memory_location = [] # To draw track
        self.rotation = atan2(self.location.y, self.location.x) # inicital rotation

        # Arbitrary values
        self.max_speed = FORWARD_SPEED
        self.max_force = SEEK_FORCE
        self.angular_speed = ANGULAR_SPEED

        # Variables related to State Machine
        self.behavior = behavior
        self.theta = 0 # variavel para o eight somada no seek_around
        self.count = 0
     
    def reached_goal(self, target):
        return target - self.location[0] <= THRESHOLD_TARGET 
    
    def update(self):
        """
            Standart Euler integration
            Updates bahavior tree
        """
        # updates behavior in machine state
        self.behavior.execute(self)
        # Updates velocity at every step and limits it to max_speed
        self.velocity += self.acceleration * 1 
        self.velocity = limit(self.velocity, self.max_speed) 
        # updates position
        self.location += self.velocity 
        # Prevents it from crazy spinning due to very low noise speeds
        if self.velocity.length() > 0.8:
            self.rotation = atan2(self.velocity.y,self.velocity.x)
        # Constrains position to limits of screen 
        self.location = constrain(self.location,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.acceleration *= 0

        # Memory of positions to draw Track
        self.memory_location.append((self.location.x,self.location.y))
        # size of track 
        if len(self.memory_location) > SIZE_TRACK:
            self.memory_location.pop(0)

    def applyForce(self, force):
        """
            Applies vetor force to Drone 
            Newton's second law -> F=m.a
            You can divide by mass
        """
        self.acceleration += force/MASS 

    def seek(self, target):
        """
            Seek Steering force Algorithm
        """
        self.desired  = ((target - self.location[0]) / SCREEN_WIDTH) * self.max_speed
        # Calculates steering force
        steer = self.desired  - self.velocity
        # Limit the magnitude of the steering force.
        steer = limit(steer,self.max_force)
        # Applies steering force to drone
        self.applyForce(steer)
    
    def arrive_new(self, target):
        """
            Arrive using potential fields 
        """
        # Calculates vector desired 
        velocity_attract = pygame.math.Vector2(0,0)
        velocity_repulsion= pygame.math.Vector2(0,0)

        velocity_attract = derivativeBivariate(.05,.05,[target, SCREEN_HEIGHT//2],self.location)

        desired_velocity = (velocity_attract - velocity_repulsion) 
        error = (desired_velocity - self.velocity) / SAMPLE_TIME 
        
        accelerate = limit(error, self.max_force)
        self.applyForce(accelerate)

    def arrive(self, target):
        """
            Arrive Steering Behavior
        """
        # Calculates vector desired 
        self.desired = pygame.math.Vector2([target - self.location[0], 0])
        # get the distance to the target
        d = self.desired.magnitude() 

        try:
            dist = copy.deepcopy(self.desired.normalize()) # obtem direção
        except: # If the magnitude of desired is zero it cant be normalized
            dist = copy.deepcopy(self.desired)
        
        # Modulates the force
        if d < THRESHOLD_TARGET : # close to target it will reduce velocty till stops
            # interpolation
            dist *= self.max_speed*(1 + 1/THRESHOLD_TARGET*(d-THRESHOLD_TARGET))
        else:
            dist *= self.max_speed

        # Steering force
        steer = dist - self.velocity
        #Limit the magnitude of the steering force.
        steer = limit(steer, self.max_force)
        # apply force to the Drone
        self.applyForce(steer)
        # Simulates Wind - random Noise
        wind = pygame.math.Vector2(random.uniform(-0.15,0.15) , random.uniform(-0.15,0.15)  )
        self.applyForce(wind)

    def seek_around(self, center, radius_target = THRESHOLD_TARGET):
        """
           Drone Behavior - it will orbit a given target (center) with prevision 

           :param center: position of target to  orbite
           :param radius_target: distance till center, default = RADIUS_TARGET from constants
        """
        # Calculating the max speed
        self.angular_speed = FORWARD_SPEED / radius_target

        # future positiom
        hop_ahead = HOP_AHEAD #o quanto se ve a frente
        fut_pos = self.velocity.normalize()*(hop_ahead)
        fut_pos += self.location

        #print(f'center: {center}')
        posToCenter = center - fut_pos
        
        # se o veiculo se encontra mais longue q o raio de rotaçao
        if posToCenter.length() > radius_target:
            self.seek(center)
            #self.target =copy.deepcopy(center) 
        else: # se ele esta dentro do raio de rotaçao
            # reinicia forças
            centerToPerimeter = posToCenter.normalize()*(-1*radius_target)
            
            # new target is on the radius
            # theta is the angle of the vector center to perimeter
            self.theta = atan2(centerToPerimeter.y, centerToPerimeter.x)
            self.theta += self.angular_speed
            new_target = pygame.math.Vector2(0,0)

            # new target
            new_target.x += radius_target * cos(self.theta)
            new_target.y += radius_target * sin(self.theta)
            new_target += center
            self.seek(new_target)

    def mission_accomplished(self):
        if self.target :
            return self.location.x == self.target.x and self.location.y == self.target.y
        else:    
            return False

    def get_position(self):
        return self.location

    def set_target(self, target):
        self.target = target
    
    def get_target(self):
        try:
            return self.target
        except: 
            return None

    def collision_avoidance(self, all_positions, index):
        """
         This method avoids collisions with other drones
         During simulation it receives all the positions from all drones 
         index: is the current id of drone being checked 
        """
        # gets all positions of simultaneos drones
        aux = 0 
        soma = pygame.math.Vector2(0,0) # sums up all directions of close drones
        count = 0 # counts the number of drones that are close
        for p in all_positions:
        # compares current position to all the drones
        # aux != index -> avoids the auto-collision check
            d = (self.location - p.location).magnitude()
            separation_factor = 2.2
            if ( (d > 0) and (d < AVOID_DISTANCE*separation_factor) and (aux != index) ) :
                diff = (self.location - p.location).normalize()
                diff = diff/d # proporcional to the distance. The closer the stronger needs to be
                soma += diff
                count += 1 # p drone is close 
            aux+=1
            
        if count > 0:
            media = soma / count
            media = media.normalize()
            media *= self.max_speed
            steer = (media - self.velocity)
            steer = limit(steer,self.max_force)
            #----
            #----
            self.applyForce(steer)
                  
    def draw(self, window):

        """
            Defines shape of Drone and draw it to screen
        """
        # usar sprite para desenhar drone
        pygame.draw.circle(window, BLUE, self.location, radius=RADIUS_OBSTACLES//4, width=20)

    def check_collision(self, positions_drones , pos_obstacles , index):
        """
            Not working yet, it should detect obstacles and collision with other drones
        """
        # check drones
        f = 1
        aux = 0 
        for p in positions_drones:
            d = (self.location - p.location).length()
            factor_distance = 2
            dist_avoid = AVOID_DISTANCE*factor_distance
            if ( d < dist_avoid )  and (aux != index):
                #f = (self.velocity - self.velocity.normalize()*self.max_speed )/ SAMPLE_TIME
                #f = limit(f,self.max_force)
                #self.velocity *= d/(AVOID_DISTANCE*factor_distance)
                f_repulsion = derivativeBivariate(0.001,.001, p.location , self.location )/SAMPLE_TIME
                #print(f_repulsion)
                f_repulsion = limit(f_repulsion,self.max_force*1.8)

                self.applyForce(-f_repulsion)
                #print(f'Alerta de colisão drone {index} com drone {aux}')
                break
            aux +=1

        # --- Repulsion obstacles 
        for p in pos_obstacles:
            d = (self.location - p).length()
            factor_repulsion = 0.005
            dist_avoid = RADIUS_OBSTACLES*1.6 + AVOID_DISTANCE
            if ( d < dist_avoid ) :
                f_repulsion = derivativeBivariate(factor_repulsion,factor_repulsion, p, self.location )/SAMPLE_TIME
                #print(f_repulsion)
                f_repulsion = limit(f_repulsion,self.max_force*1.8)
             #----
                # This condition checks if drone collided with wall
                # if collided, this avoids that the drone goes over the obstacle
                if (d < RADIUS_OBSTACLES + SIZE_DRONE):
                    self.velocity *= -1

                self.applyForce(-f_repulsion)

class AgentState:
    def __init__(self, x, y, local_robustness, local_connectivity, drones_impulse, obstacles_impulse):
        self._x = x
        self._y = y
        self._local_robustness = local_robustness
        self._local_connectivity = local_connectivity
        self._drones_impulse = drones_impulse
        self._obstacles_impulse = obstacles_impulse

    def get_state(self):
        state = {
            "x": self._x, 
            "y": self._y, 
            "local_robustness": self._local_robustness, 
            "local_connectivity": self._local_connectivity, 
            "drones_impulse": self._drones_impulse, 
            "obstacles_impulse": self._obstacles_impulse 
        }
        return state

    def get_position(self):
        return (self._x, self._y)

    def get_robustness(self):
        return self._local_robustness

    def get_connectivity(self):
        return self._local_connectivity

    def get_drones_impulse(self):
        return self._drones_impulse

    def get_obstacles_impulse(self):
        return self._obstacles_impulse

    def update_position(self, x, y):
        self._x = x
        self._y = y 

    def update_robustness(self):
        pass

    def update_connectivity(self):
        pass

    def update_drones_impulse(self):
            pass

    def update_obstacles_impulse(self):
            pass