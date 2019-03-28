# Nicholas Scharan Cysne
# T22.1 
#
# CCI-22 Professor: Johnny
# Zero de Funções
# Método da Falsa Posição

import random
import math

def falsePosition(parameters, calculate):

    interval = parameters[0]
    epsilon = parameters[1]  
    polinom = parameters[2]

    if interval[1] - interval[0] < epsilon:
        return random.uniform(interval[0], interval[1])
    if math.fabs(calculate(polinom, interval[0])) < epsilon:
        return interval[0]
    if math.fabs(calculate(polinom, interval[1])) < epsilon:
        return interval[1]

    while True:
        
        fa = calculate(polinom, interval[0])
        fb = calculate(polinom, interval[1])
        x = (interval[0]*fb + interval[1]*fa)/(fb - fa)
        M = fa

        if calculate(polinom, x) < epsilon:
            return x

        if M*calculate(polinom, x) > 0:
            interval[0] = x
        else:
            interval[1] = x

        if interval[1] - interval[0] < epsilon:
            return random.uniform(interval[0], interval[1])
