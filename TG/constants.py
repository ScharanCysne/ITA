# Simulation Parameters
PIX2M = 0.01                    # factor to convert from pixels to meters
M2PIX = 100.0                   # factor to convert from meters to pixels
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
NUM_DRONES = 10                 # Number of simultaneous drones
SIZE_DRONE = 10
SIZE_TRACK = 100
RESOLUTION = 30                 # of grid
NUM_OBSTACLES = 20
RADIUS_OBSTACLES = 20
TIME_MAX_SIMULATION = 20        # Time to stop simulation in case the conditions are not completed
OBSERVABLE_RADIUS = 200
AVOID_DISTANCE = 20

# Sample Time Parameters
FREQUENCY = 60.0                # simulation frequency
MAX_FREQUENCY = 1000.0          # simulation frequency to be used in intel oneAPI
SAMPLE_TIME = 1.0 / FREQUENCY   # simulation sample time

# Behavior Parameters
FORWARD_SPEED = 2               # default linear speed when going forward
ANGULAR_SPEED = 1.5             # default angular speed
SEEK_FORCE = 0.5                # max seek force
THRESHOLD_TARGET = SCREEN_WIDTH*0.1 
MASS = 10                       # Drone Mass, used to calculate force

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
LIGHT_RED = (250,255,114)
LIGHT_GRAY = (232, 232, 232)
LIGHT_YELLOW = (255,255,102)

# keys
MOUSE_LEFT = 0
MOUSE_RIGHT = 2

# Rewards
REWARD_STEP = -1
REWARD_DISCONNECTED = -100
TIMESTEPS_PER_ITERATION = 1200