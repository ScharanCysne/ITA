import copy 
import pygame 

from utils     import limit, constrain, derivativeBivariate
from constants import *

class Drone():
    def __init__(self, x, y, index):
        """
            Idealized class representing a drone
            :param x and y: represents inicial position 
        """
        # Variables used to move drone 
        self.location = pygame.math.Vector2(x,y) 
        self.velocity = pygame.math.Vector2(0,0) 
        self.acceleration = pygame.math.Vector2(0,0)
        self.target = SCREEN_WIDTH
        self.radius = SIZE_DRONE            
        self.desired = pygame.math.Vector2()
        self.reached = False
        self.alive = True

        # Arbitrary values
        self.max_speed = FORWARD_SPEED
        self.max_force = SEEK_FORCE
        self.angular_speed = ANGULAR_SPEED

        # Variables related to State Machine
        self.theta = 0 # variavel para o eight somada no seek_around
        self.count = 0
        self.id = index
        self.name = "Drone " + str(index)
        self.time_executing = 0  
        self.finished = False

        # State variables
        self.agent_state = State()


    def reached_goal(self, target):
        self.reached = target - self.location[0] <= THRESHOLD_TARGET
        return self.reached


    def execute(self):
        self.arrive(self.target)
        self.time_executing +=1
        
        if (self.target - self.location[0]) < THRESHOLD_TARGET and self.time_executing < 300:
            self.finished = True


    def update(self):
        """
            Standart Euler integration
            Updates bahavior tree
        """
        # updates behavior in machine state
        self.execute()
        # Updates velocity at every step and limits it to max_speed
        self.velocity += self.acceleration * 1 
        self.velocity = limit(self.velocity, self.max_speed) 
        # updates position
        self.location += self.velocity 
        # Constrains position to limits of screen 
        self.location = constrain(self.location,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.acceleration *= 0


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


    def collision_avoidance(self, positions):
        """
         This method avoids collisions with other drones
         During training it receives all the positions from all drones 
         During evaluation it receives only the positions inside observable area 
        """
        # gets all positions of simultaneos drones
        aux = 0 
        soma = pygame.math.Vector2(0,0) # sums up all directions of close drones
        count = 0 # counts the number of drones that are close
        for p in positions:
        # compares current position to all the drones
        # aux != index -> avoids the auto-collision check
            d = (self.location - p.location).magnitude()
            separation_factor = 2.2
            if d > 0 and d < AVOID_DISTANCE * separation_factor and aux != self.id:
                diff = (self.location - p.location).normalize() # returns vector with same direction but length one
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
            self.applyForce(steer)
                  

    def check_collision(self, positions_drones, pos_obstacles):
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
            if ( d < dist_avoid )  and (aux != self.id):
                #f = (self.velocity - self.velocity.normalize()*self.max_speed )/ SAMPLE_TIME
                #f = limit(f,self.max_force)
                #self.velocity *= d/(AVOID_DISTANCE*factor_distance)
                f_repulsion = derivativeBivariate(0.001,.001, p.location , self.location )/SAMPLE_TIME
                #print(f_repulsion)
                f_repulsion = limit(f_repulsion, self.max_force*1.8)

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


    def get_position(self):
        return self.location


    def get_state(self):
        return [
            self.agent_state.get_position(),
            self.agent_state.get_vulnerability_level(),
            self.agent_state.get_connectivity_level(),
            self.agent_state.get_obstacles_potential(),
            self.agent_state.get_neighbors_potential()
        ]
            

    def draw(self, window):
        """
            Defines shape of Drone and draw it to screen
        """
        # usar sprite para desenhar drone
        pygame.draw.circle(window, BLUE, self.location, radius=RADIUS_OBSTACLES//4, width=20)


class State:
    def __init__(self):
        self.pos_x = None
        self.pos_y = None
        self.vulnerability_level = None
        self.connectivity_level = None
        self.obstacles_potential_x = None
        self.obstacles_potential_y = None
        self.neighbors_potential_x = None
        self.neighbors_potential_y = None

    def get_position(self):
        return self._x, self._y

    def get_vulnerability_level(self):
        return self.vulnerability_level

    def get_connectivity_level(self):
        return self.connectivity_level

    def get_neighbors_potential(self):
        return self.neighbors_potential_x, self.neighbors_potential_y

    def get_obstacles_potential(self):
        return self.obstacles_potential_x, self.obstacles_potential_y

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        
    def set_vulnerability_level(self, level):
        self.vulnerability_level = level

    def set_connectivity_level(self, level):
        self.connectivity_level = level

    def set_neighbors_potential(self, potential):
        self.neighbors_potential_x = potential[0]
        self.neighbors_potential_y = potential[1]

    def set_obstacles_potential(self, potential):
        self.obstacles_potential_x = potential[0]
        self.obstacles_potential_y = potential[1]