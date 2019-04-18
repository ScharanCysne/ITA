import math

def f(x):
    return x*x*x - x - 1

while True:

    x1, x0 = input().split()
    x1 = float(x1)
    x0 = float(x0)

    x = x1 - (f(x1)*(x1 - x0))/(f(x1) - f(x0))
    
    print(x)
    print(f(x))    