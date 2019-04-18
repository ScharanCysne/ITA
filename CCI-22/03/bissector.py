# Nicholas Scharan Cysne
# T22.1 
#
# CCI-22 Professor: Johnny
# Zero de Funções
# Método da Bissecção

import random

def bissector(parameters, calculate):

    interval = parameters[0]
    epsilon = parameters[1]  
    polinom = parameters[2]
    counter = 0

    if interval[1] - interval[0] < epsilon:
        return random.uniform(interval[0], interval[1]), counter

    k = 1

    while True:

        counter += 1
        M = calculate(polinom, interval[0])
        x = (interval[0] + interval[1])/2

        if M*calculate(polinom, x) > 0:
            interval[0] = x
        else:
            interval[1] = x

        if interval[1] - interval[0] < epsilon:
            return random.uniform(interval[0], interval[1]), counter
        k += 1
