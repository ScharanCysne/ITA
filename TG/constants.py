# Simulation Parameters
PIX2M = 0.01                    # factor to convert from pixels to meters
M2PIX = 100.0                   # factor to convert from meters to pixels
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
NUM_DRONES = 20                 # Number of simultaneous drones
SIZE_DRONE = 18
SIZE_TRACK = 100
RESOLUTION = 10                 # of grid
NUM_OBSTACLES = 20
RADIUS_OBSTACLES = 40
TIME_MAX_SIMULATION = 20        # Time to stop simulation in case the conditions are not completed

# Sample Time Parameters
FREQUENCY   = 60.0              # simulation frequency
SAMPLE_TIME = 1.0 / FREQUENCY   # simulation sample time

# Behavior Parameters
FORWARD_SPEED = 2               # default linear speed when going forward
ANGULAR_SPEED = 1.5             # default angular speed
SEEK_FORCE = 0.5                # max seek force
THRESHOLD_TARGET = 100 
MASS = 10                       # Drone Mass, used to calculate force
HOP_AHEAD = 60                  # distance of prevision
AVOID_DISTANCE = 30             # distance to avoid collision

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
LIGHT_GRAY = (232, 232, 232)

# keys
MOUSE_LEFT = 0
MOUSE_RIGHT = 2