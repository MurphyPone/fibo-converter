#imports
import sys
import time
from visualize import *

# Constants
km_per_mi = 1.60934
mi_per_km = 0.621371

# Generate fibonacci numbers
def fib(n):
    if n <= 0:
        print("Invalid input")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def load_fib():
    list = [0]
    with open('fib.csv') as fp:
        line = fp.readline()
        cnt = 1
        while line and cnt < 1000:
            line = fp.readline().strip()
            list.append(float(line))
            cnt += 1

    return list

# Convert km to mi
def km_to_mi(km):
    return km * mi_per_km

# Convert mi to km
def mi_to_km(mi):
    return mi * km_per_mi

# calculate the %error between the  fib #
# and the actual conversion number using fib(n), fib(n+1)
def loss(n, list):
    mi = list[n]
    fib_km = list[n+1]

    actual_km = mi_to_km(mi)

    return abs((actual_km - fib_km) / actual_km) * 100


fib = load_fib()

i = 1
while(i < len(fib)):
    e = loss(i, fib)
    plot_error(i, e, 'Error', 'fibonacci index')
    plot(i, fib[i], 'fibonacci index', 'Distance', 'mi', '#6d39fa')
    plot(i, fib[i+1], 'fibonacci index', 'Distance', 'km', '#fa395c')

    time.sleep(0.2)
    i += 1
