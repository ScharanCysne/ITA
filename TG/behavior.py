from constants import *

class Behavior:
    """
        Drone will seek target  
    """
    def __init__(self, target):
        self.time_executing = 0  
        self.finished = False
        self.target = target

    def execute(self, agent):
        agent.arrive(self.target)
        self.time_executing +=1
        
        if (self.target - agent.location[0]) < THRESHOLD_TARGET and self.time_executing < 300:
            self.finished = True