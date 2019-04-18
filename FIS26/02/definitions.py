import numpy
import math
import time
import vpython as vs
import matplotlib.pyplot as plt
from vpython import box, ring, curve, color, cylinder

# Variable Mass in L Shape Pendullum

vs.scene.width = vs.scene.height = 800
vs.scene.range = 1.8
vs.scene.title = "Rotating Platform for Inertial Momentum Calculus"

# Entries for graph plotting

period_int_entry = []
x_position_entry = []
time_frame_entry = []

# Constants for calculus use

g = 9.81                            # Gravity (m/s²)
FREQUENCY = 3600                    # Time Rate (Hz)
dt = 1/FREQUENCY                    # Time Elapsed in One Loop
TIME_LIMIT = 5                      # Time spent for the platform rotates 5 times
ENVIRONMENT_ROTATION = -math.pi/16   # Angular velocity of environment

t = 0                               # Begin Time
dtheta = ENVIRONMENT_ROTATION * dt  # Angle of rotation for each iteration

# Without Mass
thetadotdot_wm = 2.697901718           # Rate of change of thetadot
wire_acceleration_wm = 4.046852577   # Block Acceleration

# With Test Block
thetadotdot_tb = 2.192472411           # Rate of change of thetadot
wire_acceleration_tb = 3.288708617   # Block Acceleration

# With Evaluation Object
thetadotdot_eo = 2.469934785           # Rate of change of thetadot
wire_acceleration_eo = 3.704902178   # Block Acceleration

# Constants for design use

Y_OFFSET = 15                   # Y-OFFSET FOR VIEWING PURPOSES (CM)
BASE_WIDTH = 15                 # TRIANGLE BASE WIDTH (CM)
BASE_HEIGHT = 2                 # BASE HEIGHT (CM)
LOWER_BAR_RADIUS = 1            # LOWER BAR RADIUS (CM)
LOWER_BAR_HEIGHT = 8            # LOWER BAR HEIGHT (CM)
UPPER_BAR_RADIUS = 1            # UPPER BAR RADIUS (CM)
UPPER_BAR_HEIGHT = 8            # UPPER BAR HEIGHT (CM)
MIDDLE_MODULE_RADIUS = 2.5      # MIDDLE MODULE RADIUS (CM)
MIDDLE_MODULE_HEIGHT = 2        # MIDDLE MODULE HEIGHT (CM)
UPPER_STATION_HEIGHT = 2        # UPPER STATION HEIGHT (CM)
UPPER_STATION_WIDTH = 6         # UPPER STATION WIDTH (CM)
UPPER_STATION_LENGHT = 42       # UPPER STATION LENGHT (CM)
BLOCK_SUPPORT_HEIGHT = 2        # BLOCK SUPPORT HEIGHT (CM)
BLOCK_SUPPORT_LENGHT = 14       # BLOCK SUPPORT lENGHT (CM)
BLOCK_SUPPORT_WIDTH = 6         # BLOCK SUPPORT WIDTH (CM)
BAR_SUPPORT_RADIUS = 1.5        # BAR SUPPORT RADIUS (CM)
BAR_SUPPORT_HEIGHT = 6          # BAR SUPPORT HEIGHT (CM)
WHEEL_SUPPORT_BAR_HEIGHT = 40   # WHEEL SUPPORT BAR HEIGHT (CM)
WHEEL_SUPPORT_BAR_RADIUS = 1    # WHEEL SUPPORT BAR RADIUS (CM)
WHEEL_SUPPORT_WIDTH = 0.2       # WHEEL SUPPORT WIDTH (CM)
WHEEL_SUPPORT_INNER_SECTION = 0.5 # WHEEL SUPPORT INNER SECTION WIDTH (CM)
WHEEL_SUPPORT_HEIGHT = 1        # WHEEL SUPPORT HEIGHT (CM)
WHEEL_WIDTH = 0.8               # WHEEL EXTERNAL WIDTH (CM)
WHEEL_INNER_SECTION = 0.3       # WHEEL INNER WIDTH (CM)
WHEEL_RADIUS = 2.5              # WHEEL RADIUS (CM)
WIRE_RADIUS = 0.1               # WIRE RADIUS (CM)