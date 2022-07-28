from constants import *

class TargetScan:
    def to_string(self) -> str:
        return 'TargetScan'

    def scan(self, simulation, list_obst):
        index = 0 # index is used to track current drone in the simulation list
        for drone in simulation.swarm:
            # checks if drones colided with eachother

            ## collision avoindance is not implemented yet
            drone.collision_avoidance(simulation.swarm, index)
            drone.check_collision(simulation.swarm,list_obst,index) 
            drone.update()
            # index to keep track of  drone in the list
            index += 1
            # writes drone id
            img = simulation.screenSimulation.font20.render(f'Drone {index}', True, BLACK)
            simulation.screenSimulation.screen.blit(img, drone.get_position()+(0,20))
            # writes drone current behavior
            img = simulation.screenSimulation.font20.render(drone.behavior.get_current_state(), True, BLUE)
            simulation.screenSimulation.screen.blit(img, drone.get_position()+(0,35))
            # writes drone current position in column and row
            p = drone.get_position()
            col = p.x // RESOLUTION + 1
            row = p.y // RESOLUTION + 1
            img = simulation.screenSimulation.font20.render(f'Pos:{col},{row}', True, BLUE)
            simulation.screenSimulation.screen.blit(img, drone.get_position()+(0,50))
            # Print if drone reached destination
            if drone.reached_goal(simulation.target_simulation):
                print(f"Drone {index} reached target")
