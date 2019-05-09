#   Laboratório 4 - Interpolação
#
#   Nicholas Scharan Cysne      T22.1
#   Professor: Johnny
#   Data: 02/05/2019
#
#   Nós de Chebyshev

import math
import numpy as np
import matplotlib.pyplot as plt

# Size of interpolation
size = 100

# Vetor de [-3, 3] com 100 valores equidistantes
vector = np.linspace(-3, 3, size)

# Chebyshev Nodes for p(x) of degree 2 to 10
chebyshev = 9*[0]
for i in range (9):
    shape = np.linspace(0, i+2, i+3)
    chebyshev[i] = 3 * np.array([math.cos(a*math.pi/2) for a in shape]) 
    print("Chebyshev Nodes of degree {}: {}\n".format(i + 2, chebyshev[i]))

# Hardcoded function d(x) = 2x^2 + 5 
function_d = [2, 0, 5]

# Vector of function d(x) = 2x^2 + 5 applied in vector
vector_d = np.polyval(function_d, vector)

# Vector of function f(x) = 4/d(x) applied in vector
vector_f = 4 / vector_d

# Function p(x) of degree 2 to 10 for polifit vector and f(vector)
function_fitted = 9*[0]
vector_p = 9*[0]
for i in range (9):
    function_fitted[i] = np.polyfit(vector, vector_f, i + 2)
    vector_p[i] = np.polyval(function_fitted[i], vector)
    print("Fitted Function {}: {}".format(i+2, function_fitted[i]))

# Maximum absolute error between f(x) and p(x)
for i in range (9):
    error_vector = np.abs(vector_f - vector_p[i])
    error_vector.sort()
    error = error_vector[size - 1]
    print("Maximum Absolute Error Between f(x) and p(x) of degree {}: {}".format(i + 2, error))


# Plotting
for i in range (9):
    fig_format = 'png'
    plt.figure()
    plt.plot(vector, vector_f)
    plt.plot(vector, vector_p[i])
    plt.scatter(chebyshev[i], 4 / np.polyval(function_d, chebyshev[i]))
    plt.legend(['f(x)', 'p(x) of degree {}'.format(i + 2)])
    plt.xlabel('X - Axis')
    plt.ylabel('Y - Axis')
    plt.title('Chebychev Nodes')
    plt.grid()
    plt.savefig('plotting_{}.{}'.format(i + 2, fig_format), format=fig_format)
    plt.show()