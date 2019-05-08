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
    counter = 0
  
    if interval[1] - interval[0] < epsilon:
        return random.uniform(interval[0], interval[1]), counter
    if math.fabs(calculate(polinom, interval[0])) < epsilon:
        return interval[0], counter
    if math.fabs(calculate(polinom, interval[1])) < epsilon:
        return interval[1], counter

    while True:
        
        counter += 1
        fa = calculate(polinom, interval[0])
        fb = calculate(polinom, interval[1])
        x = (interval[0]*fb - interval[1]*fa)/(fb - fa)
        M = fa

        if math.fabs(calculate(polinom, x)) < epsilon:
            return x, counter

        if M*calculate(polinom, x) > 0:
            interval[0] = x
        else:
            interval[1] = x

        if interval[1] - interval[0] < epsilon:
            return random.uniform(interval[0], interval[1]), counter
