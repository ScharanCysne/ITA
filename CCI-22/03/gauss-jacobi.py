#   Laboratório 3 - Sistemas Lineares
#
#   Nicholas Scharan Cysne      T22.1
#   Professor: Johnny
#   Data: 29/04/2019
#
#   Método de Gauss-Jacobi

import numpy as np
import math

# Identificação dos Parâmetros

print("Digite a ordem do sistema linear:")

order = int(input())                            # Ordem do Sistema Linear
A_coef = np.identity(order)                     # Matriz de Coeficientes A
C_coef = np.identity(order)                     # Matriz de Coeficientes C
X_vector = np.zeros(np.shape(A_coef[0]))        # Vetor X
X1_vector = np.zeros(np.shape(A_coef[0]))       # Vetor X1
dx_vector = np.zeros(np.shape(A_coef[0]))       # Vetor dx
b_vector = np.zeros(np.shape(A_coef[0]))        # Vetor b
g_vector = np.zeros(np.shape(A_coef[0]))        # Vetor g

while True:
    print("Digite, por linhas, os coeficientes da matriz de coeficientes:")
    for i in range (order):
        A_coef[i] = input().split()             # Ler N linhas de coeficientes
    
    print("Matrix de coeficientes:")           # Verificação do Usuário se a matriz está correta
    print(A_coef)
    print("A matriz está correta? (S/N)")
    answer = input()                            # Resposta dada pelo Usuário

    if answer == "S":
        break

while True:
    print("Digite o vetor X inicial:") 
    X_vector = input().split()                  # Vetor X

    if np.size(X_vector) != order:
        print("O tamanho do vetor está errada. Digite Novamente:")
    else:
        for i in range (np.size(X_vector)):
            X_vector[i] = float(X_vector[i])
        print("Vetor inicial X:")
        print(X_vector)
        print("O vetor está correto? (S/N)")
        answer = input()                        # Resposta dada pelo Usuário

        if answer == "S":
            break

while True:
    print("Digite o vetor b dos termos independentes:") 
    b_vector = input().split()                  # Vetor de Termos Independentes

    if np.size(b_vector) != order:
        print("O tamanho do vetor está errada. Digite Novamente:")
    else:    
        for i in range (np.size(b_vector)):
            b_vector[i] = float(b_vector[i])
        print("Vetor de termos independentes b:")
        print(b_vector)
        print("O vetor está correto? (S/N)")
        answer = input()                        # Resposta dada pelo Usuário

        if answer == "S":
            break

while True:
    print("Digite a precisão:") 
    epsilon = float(input())                    # Precisão da Aproximação

    print("Precisão de Aproximação:")
    print(epsilon)
    print("O valor está correto? (S/N)")
    answer = input()                            # Resposta dada pelo Usuário

    if answer == "S":
        break

# Aproximações Lineares

counter_k = 1                                   # Contador de iterações k

for i in range (order):
    for j in range (order):
        if i == j:
            C_coef[i][j] = 0
            g_vector[i] = b_vector[i]/A_coef[i][j]
        else:
            C_coef[i][j] = -A_coef[i][j]/A_coef[i][i]

while True:
    
    X1_vector = np.dot(C_coef, X_vector) + g_vector
    dx_vector = np.abs(X1_vector - X_vector)
    dr1 = math.fabs(np.sort(X1_vector)[0])
    dr2 = math.fabs(np.sort(dx_vector)[0])

    if dr1 != 0 and (dr2/dr1) < epsilon:
        break
    
    X_vector = np.copy(X1_vector)
    counter_k += 1

print("Número de iterações: {}".format(counter_k))
print("Solução do sistema: {}".format(X1_vector))
print("Precisão da Aproximação: {}".format(dr2/dr1))