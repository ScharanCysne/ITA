import numpy
import math
import vpython as vs
import matplotlib.pyplot as plt
from vpython import box, color, cylinder

# Variable Mass in L Shape Pendullum

vs.scene.width = vs.scene.height = 800
vs.scene.range = 1.8
vs.scene.title = "Variable Mass in L Shape Pendullum"

# Entries for graph plotting

period_int_entry = []
x_position_entry = []
time_frame_entry = []

# Constants for calculus use

g = 9.81            # Gravity (m/s²)
FREQUENCY = 60      # Time Rate (Hz)
dt = 1/FREQUENCY    # Time Elapsed in One Loop
t = 0               # Begin Time
Tlimit = 2.58       # Time that all ater flows out of pipe
M1 = 0.195          # Upper Pipe Mass (kg)
M2 = 0.097          # Lower Pipe Mass (kg)
Mo = 0.615          # Initial Mass of Liquid
Rext = 0.03191      # External Radius (m)
Rint = 0.02828      # Internal Radius (m)
Rf = 0.01           # Bottom Hole Radius (m)
L1 = 0.60314        # Physical Length of Upper Assembly
L2 = 0.31415        # Physical Length of Lower Assembly
Lm = (L1+L2)/2      # Medium Physical Length
p = 1000            # Water density (kg/m³)
Vo = math.pi*(L1+L2)*Rint*Rint  # Initial volume of water

thetazero = -math.pi/12  # Simulation Initial Angle
theta = -math.pi/12      # initial upper angle (from vertical)
thetadot = 0            # initial rate of change of theta
thetadotdot = 0         # Initial rate of change of thetadot

# Constants for design use

d = 0.03                                # radius of each pipe
offset = 4*d                            # from center of pedestal to center of origin
L1display = L1+d                        # show upper assembly a bit longer than physical, to overlap axle
L2display = L2+d/2                      # show lower bar a bit longer than physical, to overlap axle
hpedestal = 1.3*(L1 + offset)           # height of pedestal
wpedestal = 2*d                         # width of pedestal
tbase = 0.02                            # thickness of base
wbase = 8*d                             # width of base
pedestal_top = vs.vec(0,hpedestal/2,0)  # top of inner bar of U-shaped upper assembly

# Functions Definitions for Physics Laws

def H(t):
    if t < Tlimit:
        A = math.sqrt(2*g/((math.pow(Rint,4)/math.pow(Rf,4)) - 1))
        return pow(math.sqrt(2*Lm) - p*A*t/2, 2)
    else:
        return 0

def L(t):
    return 2*Lm - H(t)

def Z(t):
    if t < Tlimit:
        return math.pi*Rf*Rf*math.sqrt(2*g*H(t)/(1 - ((math.pow(Rf,4)/math.pow(Rint,4)))))
    else:
        return 0

def W(t):

    K = math.pi*Rf*Rf*math.sqrt(2*g/((1 - math.pow(Rf,4)/math.pow(Rint,4))))
    A = p*math.sqrt(2*g/((math.pow(Rint,4)/math.pow(Rf,4)) - 1))/2

    return p*Vo - p*K*math.sqrt(2*Lm)*t + p*A*t*t/2

def M(t):
    if t < Tlimit:
        return (M1 + M2) + W(t)
    else:
        return (M1 + M2)

def Za(t):
    return (2*Lm - L(t))*(2*Lm - L(t))/(2*(3*Lm - L(t)))

def Ya(t):
    return (Lm*Lm)/(2*(3*Lm - L(t)))

def ZCM(t):
    return ((M(t) - (M1 + M2))*Za(t) + (M1 + M2)*Lm)/M(t)

def YCM(t):
    return ((M(t) - (M1 + M2))*Ya(t) + (M1 + M2)*Lm/2)/M(t)

def X(t):
    return math.sqrt((2*Lm - ZCM(t))*(2*Lm - ZCM(t)) + YCM(t)*YCM(t))

def Iz(t):
    return ((M1 + M2)*(math.pow(Rint,2) + math.pow(Rext,2)) + W(t)*math.pow(Rint,2))/2

def Iv(t):
    A = (Lm + (Z(t)*t)/(2*math.pi*math.pow(Rint,2)))*(Lm + (Z(t)*t)/(2*math.pi*math.pow(Rint,2)))
    return Iz(t)/2 + (M1 + M2)*Lm*Lm + W(t)*A

def Ih(t):
    return (4*Lm*Lm/3)*((M1 + M2)/3 + p*math.pi*Rint*Rint*Lm)

def I(t):
    return Iv(t) + Ih(t)

def Tdotdot(theta):
    return -(M(t)*g*X(t)*theta)/I(t)

def period (t):
    return 2*math.pi*math.sqrt(I(t)/(M(t)*g*X(t)))