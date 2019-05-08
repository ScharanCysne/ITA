# Nicholas Scharan Cysne
# T22.1 
#
# CCI-22 Professor: Johnny
# Zero de Funções

from bissector import *
from falsePosition import *
from fixedPoint import *

def calculate(coef, a):
    
    result = 0
    exp = len(coef) - 1
    
    for c in coef:
       
        result += c*math.pow(a, exp)
        exp -= 1
    
    return result

interval = [1, 2]           # Interval of search
epsilon = 1e-3              # Acceptable error
polinom = [1, 0, -1, -1]    # x³ - x - 1

parameters = [[1, 2], epsilon, polinom]
print(" Raiz utilizando o Método da Bissecção:      {}".format(bissector(parameters, calculate)))
parameters = [[1, 2], epsilon, polinom]
print(" Raiz utilizando o Método da Falsa Posição:  {}".format(falsePosition(parameters, calculate)))
parameters = [[1, 2], epsilon, polinom]
print(" Raiz utilizando o Método do Newton-Raphson: {}".format(newtonRaphson(parameters, calculate)))