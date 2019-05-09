#   Laboratório 4 - Interpolação
#
#   Nicholas Scharan Cysne      T22.1
#   Professor: Johnny
#   Data: 02/05/2019
#
#   Interpolação

import numpy as np
import matplotlib.pyplot as plt

# Size of interpolation
size = 100

# Vetor de [0, 1] com 100 valores equidistantes
vector = np.linspace(-1, 0, size)

# Hardcoded function f(x) = x^10 - 3x^2 - 2
function1 = [1, 0, 0, 0, 0, 0, 0, 0, -3, 0, -2]

# Hardcoded function f(x) = -1.004x^2 + 0.996x - 2 
function2 = [-1.004, 0.966, -2]

# Vector of function f(x) = x^10 - 3x^2 - 2 applied in vector
vector_f1 = np.polyval(function1, vector)

# Vector of function f(x) = -1.004x^2 + 0.996x - 2 applied in vector
vector_f2 = np.polyval(function2, vector)

# Function p(x) of degree 2 for polifit vector and f(vector)
function1_fitted = np.polyfit(vector, vector_f1, 2)
vector_f1f = np.polyval(function1_fitted, vector)
print("Polinom p(x) fitted in vector: {}".format(function1_fitted))

# Maximum absolute error between f(x) and g(x)
error_vector = np.abs(vector_f1 - vector_f2)
error_vector.sort()
error = error_vector[size - 1]
print("Maximum Absolute Error Between f(x) and g(x): {}".format(error))

# Maximum absolute error between f(x) and p(x)
error_vector = np.abs(vector_f1 - vector_f1f)
error_vector.sort()
error = error_vector[size - 1]
print("Maximum Absolute Error Between f(x) and p(x): {}".format(error))

# Plotting
fig_format = 'png'
plt.figure()
plt.plot(vector, vector_f1)
plt.plot(vector, vector_f2)
plt.plot(vector, vector_f1f)
plt.legend(['f(x)', 'g(x)', 'p(x)'])
plt.xlabel('X - Axis')
plt.ylabel('Y - Axis')
plt.title('Functions Plotting')
plt.grid()
plt.savefig('plotting.%s' % fig_format, format=fig_format)
plt.show()
