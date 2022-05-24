'''
Input: Lista de preferências de par de cada homem e cada mulher, 
Output: Lista de pares resultantes.

A ideia é seguir o algoritmo de Gale-Shapley, em que iteramos sobre todos os homens disponíveis. Para cada homem, o homem verifica cada uma das mulheres da lista em ordem, se a mulher está disponível eles entram em acordo de casamento, se não a mulher pode escolher entre o par atual e o novo par proposto, isso depende de sua ordem de preferência. 

Complexidade do algoritmo: O(n²).  N número de homens ou mulheres.

Pseudo-código:

// Inicializa-se todos os homens e mulheres disponíveis
while exists free man:
     for woman in man's preference list order:
          if woman is free:
                 create pair (man, woman)
          else:
                  if woman prefers man over current pair:
                         delete pair (man', woman)
                         create pair (man, woman)
                   else:
                          continue
return pairs
'''

import numpy as np
import matplotlib.pyplot as plt

from time import time

# Generate random preferences
def sampleGenerator(n):
    mpref = []
    wpref = []

    for _ in range(n):
        mpref.append(np.random.choice(np.arange(0, n), replace=False, size=n))
        wpref.append(np.random.choice(np.arange(0, n), replace=False, size=n))

    # Create array of pairs
    ms = [-1] * n
    ws = [-1] * n

    return ms, ws, mpref, wpref


# Logs the final pairs and preferences
def logger(ms, ws, mpref, wpref):
    print("Men's preferences: " + str(mpref))
    print("Women's preferences: " + str(wpref))
    print("Final Pairs (men): " + str(ms))
    print("Final Pairs (women): " + str(ws))


# Stable Marriage Algorithm
def stableMarriage(n, log=False):
    ms, ws, mpref, wpref = sampleGenerator(n)
    while -1 in ms:
        man = ms.index(-1)
        for woman in mpref[man]:
            if ws[woman] == -1:
                ws[woman] = man
                ms[man] = woman
                break
            else:
                if np.where(wpref[woman] == man) < np.where(wpref[woman] == ws[woman]):
                    ms[ws[woman]] = -1
                    ws[woman] = man
                    ms[man] = woman
                    break
                else:
                    continue
    if log:
        logger(ms, ws, mpref, wpref)

# Average case calculation
ts = np.ndarray(98)
for i in range(3,101):
    print(str(i-2) + "th iteration.")
    t = 0
    for j in range(100 * i):
        t1 = time()   
        stableMarriage(i)
        t2 = time()
        t += (t2-t1)
    ts[i-3] = t/(100 * i)

# Fit curve to ts
coef = np.polyfit(range(3,101), ts, 2)
print("Fitted Curve: t(s) = " + str(coef[0]) + " s^2 + " + str(coef[1]) + " s + " + str(coef[2]))
# Fitted Curve: t(s) = 7.553e-07 s^2 + 8.967e-05 s - 0.0003

# Plot average time and fitted curve
plt.figure()
plt.plot(range(3,101),ts * 1000)
plt.title("Average Case Estimation - Stable Marriage")
plt.ylabel("Time (ms)")
plt.xlabel("Size")
plt.show()
