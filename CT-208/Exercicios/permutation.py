import random

import numpy             as np
import matplotlib.pyplot as plt

from time   import time
from math   import factorial
from random import randrange

random.seed(1)
np.random.seed(1)

# Returns canonical definition of permutation pi
def canonicalNotation(pi):
    def findMinimum(n, cycles):          
        pos = [i for i in range(n)]     
        for i in range(n):
            for cycle in cycles:
                if i in cycle:
                    pos.remove(i)
        return pos[0] if pos else None
        
    if not pi:
        return ""

    n = len(pi)
    cycles = []             

    newCycle = [0]          
    start = 0               
    idx = 0

    while True:
        idx = pi[idx]       # 2
        if idx == start:    # False
            if idx not in newCycle:
                newCycle.append(idx)
            cycles.append(newCycle.copy())
            newCycle = []
            start = findMinimum(n, cycles)
            idx = start
            if not start:
                break 
        else:
            newCycle.append(idx)
    
    cycles = [",".join([str(e) for e in cycle]) for cycle in cycles]

    return "(" + ")(".join(cycles[::-1]) + ")", cycles


# Execute permutation pi
def executePermutation(L, pi):
    n = len(L)
    for i in range(n):
        k = pi[i]
        while k > i:
            k = pi[k]
        if k == i:
            y = L[i]            
            l = pi[k]           
            while l != i:        
                L[k] = L[l]
                k = l
                l = pi[k]
            L[k] = y            
    return L
        

# Generate single permutation of size n
def generatePermutation(items):
    ''' Fisher-Yates shuffle '''
    n = len(items)
    for i in range(n-1):
        j = randrange(i,n) 
        items[j], items[i] = items[i], items[j]


# Generates list of all permutations of size n
def generatePermutations(n):
    permutations = []
    m = factorial(n)
    newList = [i for i in range(n)][::-1]
    while len(permutations) != m:
        nextPermutation(newList)
        permutations.append(newList.copy())
    
    for permutation in permutations:
        yield permutation


# Generates next lexicographic permutation
def nextPermutation(nums):
    i = len(nums)-2
    while i > -1 and nums[i] >= nums[i+1]:
        i -= 1
    if i < 0:
        nums[:] = reversed(nums)
        return 
    
    # find next bigger
    j = len(nums)-1
    while j >= 0 and nums[j] <= nums[i]:
        j -= 1

    # swap
    nums[j], nums[i] = nums[i], nums[j]
    # sort remaining values
    nums[i+1:] = reversed(nums[i+1:])


##########################################################################################
########################           PERMUTATION EXERCISE            #######################
##########################################################################################

# Iterate over m diferent sizes of array and plot runtime in function of m
m = 11
permutation_time = []
cycles_number = []
cycles_length = []

# iterate from 1 to 11
for i in range(1,m+1):
    print("Calculating results for " + str(i) + "th size")

    # Initialize average variables
    k = 1
    avgtime = 0
    avg_cycle_number = 0
    avg_cycle_length = 0
    # for each permutation of size i
    for pi in generatePermutations(i):
        # Initilize sorted list
        L = [i+1 for i in range(i)]
        # Calculate time to execute permutation
        start = time()
        L = executePermutation(L, pi)
        end = time()
        
        # generate canonical representation
        canonical, cycles = canonicalNotation(pi)
        
        # average time to execute permutation
        avgtime = (avgtime*(k-1) + (end-start))/k
        # average number of leaders
        avg_cycle_number = (avg_cycle_number*(k-1) + len(cycles))/k
        # average size of cycles
        avg_cycle_length = (avg_cycle_length*(k-1) + np.average([len(cycle) for cycle in cycles]))/k
        # update k
        k += 1

    # Add averages to array
    permutation_time.append(avgtime)
    cycles_number.append(avg_cycle_number)
    cycles_length.append(avg_cycle_length)
        
    # Print results
    print("Permutation execution average time: " + str(avgtime))
    print("Average cycle number for m=" + str(i) +": " + str(avg_cycle_number))
    print("Average cycle length for m=" + str(i) +": " + str(avg_cycle_length))

# Plot average permutation execution time from m=1 to m=11
plt.figure()
plt.plot(permutation_time)
plt.title("Permutation Time from m=1 to m=11")
plt.show()

# Plot average permutation execution time from m=1 to m=11
plt.figure()
plt.plot(cycles_number)
plt.title("Average number of leaders from m=1 to m=11")
plt.show()

# Plot average permutation execution time from m=1 to m=11
plt.figure()
plt.plot(cycles_length)
plt.title("Average length of cycles from m=1 to m=11")
plt.show()

# Print results
print("Permutation execution average time: " + str(permutation_time))
print("Average cycle number for m=1 to 11: " + str(cycles_number))
print("Average cycle length for m=1 to 11: " + str(cycles_length))

#Permutation execution average time: [1.430511474609375e-06, 1.3113021850585938e-06, 1.1920928955078125e-06, 1.4106432596842449e-06, 1.8378098805745442e-06, 2.178549766540528e-06, 2.2214556497240787e-06, 2.2694291103453973e-06, 3.540619051435412e-06, 3.839564662446023e-06, 5.992358618818991e-06]
#Average cycle number for m=1 to 11: [1.0, 1.5, 1.8333333333333333, 2.0833333333333335, 2.2833333333333323, 2.449999999999998, 2.592857142857147, 2.7178571428571217, 2.828968253968253, 2.9289682539681543, 3.01987734487731]
#Average cycle length for m=1 to 11: [1.0, 2.0, 2.8333333333333335, 3.5833333333333335, 4.2805555555555515, 4.940277777777778, 5.571461640211731, 6.179910714286918, 6.769646715169738, 7.343597608116218, 8.308703019394152]