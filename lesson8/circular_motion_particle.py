#!/usr/bin/python3

from math import *
import random

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

class robot:

    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    # --------
    # set: 
    #   sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    # --------
    # set_noise: 
    #   sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # sense:
    #   obtains bearings from positions
    #
    
    def sense(self, add_noise=1):
        Z = []
        for i in range(len(landmarks)):
            bearing = atan2(landmarks[i][0] - self.y, landmarks[i][1] - self.x) - self.orientation
            if add_noise:
                bearing += random.gauss(0., self.bearing_noise)
            bearing %= 2. * pi
            Z.append(bearing)
        return Z
    
    def move(self, motion, tolerance=.001):

        steering = motion[0]
        distance = motion[1]
        # abs steering must be less than max steering angle
        # distance must be greater than 0

        # make a new copy
        res = robot()
        res.length = self.length
        res.bearing_noise = self.bearing_noise
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # execute motion
        turn = tan(steering2) * distance2 / res.length
        if abs(turn) < tolerance:
            # approximate by straight line motion
            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2. * pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2. * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res # make sure your move function returns an instance
                      # of the robot class with the correct coordinates.

## --------
## TEST CASE:
## 
## 1) The following code should print:
##       Robot:     [x=0.0 y=0.0 orient=0.0]
##       Robot:     [x=10.0 y=0.0 orient=0.0]
##       Robot:     [x=19.861 y=1.4333 orient=0.2886]
##       Robot:     [x=39.034 y=7.1270 orient=0.2886]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]

T = len(motions)

print(f'Robot:    {myrobot}')
for t in range(T):
   myrobot = myrobot.move(motions[t])
   print(f'Robot:    {myrobot}')


print('\n'*5)

    
## 2) The following code should print:
##      Robot:     [x=0.0 y=0.0 orient=0.0]
##      Robot:     [x=9.9828 y=0.5063 orient=0.1013]
##      Robot:     [x=19.863 y=2.0201 orient=0.2027]
##      Robot:     [x=29.539 y=4.5259 orient=0.3040]
##      Robot:     [x=38.913 y=7.9979 orient=0.4054]
##      Robot:     [x=47.887 y=12.400 orient=0.5067]
##      Robot:     [x=56.369 y=17.688 orient=0.6081]
##      Robot:     [x=64.273 y=23.807 orient=0.7094]
##      Robot:     [x=71.517 y=30.695 orient=0.8108]
##      Robot:     [x=78.027 y=38.280 orient=0.9121]
##      Robot:     [x=83.736 y=46.485 orient=1.0135]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

motions = [[0.2, 10.] for row in range(10)]

T = len(motions)

print(f'Robot:    {myrobot}')
for t in range(T):
   myrobot = myrobot.move(motions[t])
   print(f'Robot:    {myrobot}')


##
## 3) The following code should print the list [6.004885648174475, 3.7295952571373605, 1.9295669970654687, 0.8519663271732721]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print('Robot:        ', myrobot)
print('Measurements: ', myrobot.sense())


## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## sense function with randomized initial robot coordinates.
    

##
## 4) The following code should print the list [5.376567117456516, 3.101276726419402, 1.3012484663475101, 0.22364779645531352]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, pi / 5.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print('Robot:        ', myrobot)
print('Measurements: ', myrobot.sense())

