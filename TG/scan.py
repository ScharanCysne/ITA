from constants import *

class TargetScan:
    def to_string(self) -> str:
        return 'TargetScan'

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
