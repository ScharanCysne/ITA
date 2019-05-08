# Nicholas Scharan Cysne
# T22.1 
#
# CCI-22 Professor: Johnny
# Zero de Funções
# Método de Newton-Raphson

import random
import math
    
def newtonRaphson(parameters, calculate):

    interval = parameters[0]
    epsilon = parameters[1]  
    polinom = parameters[2]
    counter = 0
    
    x = interval[0]
    if math.fabs(calculate(polinom, x)) < epsilon:
        return interval[0], counter

    while True:

        counter += 1
        x_back = x
        x = x - calculate(polinom, x)/calculate([0, 3, 0, 1],x)
        if math.fabs(calculate(polinom, x)) < epsilon:
            return x, counter
        if math.fabs(x - x_back) < epsilon:
            return x, counter