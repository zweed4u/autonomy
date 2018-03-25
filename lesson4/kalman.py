#!/usr/bin/python3
from math import *

def f(mu, sigma_squared, x):
    # return normalized gaussian function
    normalizizer = 1 / sqrt(2 * pi * sigma_squared)
    return normalizizer * e ** (-1 / 2) * ((x - mu) ** 2)/ sigma_squared

# To find maximum set x = mu
print(f(10.0, 4.0, 8.0))

class Kalman_1D:
    def update(self, mean1, var1, mean2, var2):
        new_mean = ((var2 * mean1) + (var1 * mean2)) / (var1 + var2)
        new_var = 1 / ((1 / var1) + (1 / var2))
        return [new_mean, new_var]

    def predict(self, mean1, var1, mean2, var2):
        new_mean = mean1 + mean2
        new_var = var1 + var2
        return [new_mean, new_var]

print(Kalman_1D().update(10.0, 8.0, 13.0, 2.0))
print(Kalman_1D().predict(10.0, 4.0, 12.0, 4.0))


# 1D Kalman Filter for sequence
measurements = [5.0, 6.0, 7.0, 9.0, 10.0]
motion = [1.0, 1.0, 2.0, 1.0, 1.0]

measurement_sig = 4.0  # measurement ncertainty
motion_sig = 2.0  # motion uncertainty
mu = 0.0  # initial mu
sig = 10000.0  # uncertainty

for i in range(len(measurements)):
    [mu, sig] = Kalman_1D().update(mu, sig, measurements[i], measurement_sig)
    print(f'update: {[mu, sig]}')

    [mu, sig] = Kalman_1D().predict(mu, sig, motion[i], motion_sig)
    print(f'predict: {[mu, sig]}')

print([mu, sig])