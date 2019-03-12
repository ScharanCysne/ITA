import random
import math
from constants import *


class FiniteStateMachine(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):        # agent == roomba
        self.state.check_transition(agent, self)
        self.state.execute(agent)


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        self.timer = 0      # Begin to measure time at this State

    def check_transition(self, agent, state_machine):
        if agent.get_bumper_state():    # Check if roomba hit something
            agent.set_velocity(0, 0)    # If so, stop imeaditily and go back
            state_machine.change_state(GoBackState())
        elif self.timer > MOVE_FORWARD_TIME:    # If didn't hit anything and moved beyond time set, start spiral
            state_machine.change_state(MoveInSpiralState())
        pass

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED, 0)
        self.timer += SAMPLE_TIME
        pass


class MoveInSpiralState(State):
    def __init__(self):
        super().__init__("MoveInSpiral")
        self.timer = 0      # Begin to measure time at this State
    
    def check_transition(self, agent, state_machine):
        if agent.get_bumper_state():
            agent.set_velocity(0, 0)
            state_machine.change_state(GoBackState())
        elif self.timer > MOVE_IN_SPIRAL_TIME:
            state_machine.change_state(MoveForwardState())
        pass

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED/(INITIAL_RADIUS_SPIRAL + SPIRAL_FACTOR*self.timer))
        self.timer += SAMPLE_TIME
        pass


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        self.timer = 0      # Begin to measure time at this State

    def check_transition(self, agent, state_machine):
        if self.timer > GO_BACK_TIME:
            agent.set_velocity(0, 0)
            state_machine.change_state(RotateState())
        pass

    def execute(self, agent):
        agent.set_velocity(BACKWARD_SPEED, 0)
        self.timer += SAMPLE_TIME
        pass


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        self.timer = 0      # Begin to measure time at this State
        self.setAngle = math.pi * ((2 * random.randint(1,101)) - 101) / 99
        self.angle = 0

    def check_transition(self, agent, state_machine):
        if self.setAngle > 0 and self.angle >= self.setAngle:
            agent.set_velocity(0, 0)
            state_machine.change_state(MoveForwardState())

        if self.setAngle < 0 and self.angle <= self.setAngle:
            agent.set_velocity(0, 0)
            state_machine.change_state(MoveForwardState())
            
        pass
    
    def execute(self, agent):
        agent.set_velocity(0, ANGULAR_SPEED)
        self.timer += SAMPLE_TIME
        
        if self.setAngle > 0:
            self.angle += SAMPLE_TIME * ANGULAR_SPEED
        elif self.setAngle < 0:
            self.angle -= SAMPLE_TIME * ANGULAR_SPEED
        
        pass
