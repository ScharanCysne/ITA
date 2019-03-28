# Nicholas Scharan Cysne
# T22.1 
#
# CCI-22 Professor: Johnny
# Zero de Funções
# Método do Ponto Fixo

import random
import math

def createPhi(polinom):
    
    phi = [0]*len(polinom)
    for i in range(len(polinom)):
        phi[i] -= polinom[i]
        phi[i] /= polinom[len(phi) - 2]

    phi[len(phi) - 2] = 0
    return phi
    

def fixedPoint(parameters, calculate):

    interval = parameters[0]
    epsilon = parameters[1]  
    polinom = parameters[2]

    phi = createPhi(polinom)

    x = interval[0]
    if calculate(polinom, x) < epsilon:
        return interval[0]

    while True:

        x_back = x
        x = calculate(phi, x_back)

        if calculate(polinom, x) < epsilon:
            return x
        if math.fabs(x - x_back) < epsilon:
            return x