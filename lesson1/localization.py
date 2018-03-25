#!/usr/bin/python3
# Localization for 2D world

colors = [['red', 'green', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green', 'green', 'green']

# still, right, down, down, right (sense to start at 1,2 end at 3,4)
motions = [[0 ,0],
           [0, 1],
           [1, 0],
           [1, 0],
           [0, 1]]

sensor_right = .7
p_move = .8

sensor_wrong = 1.0 - sensor_right
p_stay = 1.0 - p_move

def sense(p, colors, measurement):
    # Probability distribution
    # World map
    # Measurement (red or green)

    # Construct new posterior distribution - initialize to 0s
    aux = [[0.0 for row in range(len(p[0]))] for col in range(len(p))] 
    s = 0.0
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (measurement == colors[i][j])
            # Non normalized posterior
            aux[i][j] = p[i][j] * (hit * sensor_right + (1 - hit) * sensor_wrong)
            s += aux[i][j]
    for i in range(len(aux)):
        for j in range(len(p[i])):
            # Normalizing aux
            aux[i][j] /= s
    return aux


def move(p, motion):
    # Probability distribution
    # Motion vector

    # Construct next distribution and initialize to 0s
    aux = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    for i in range(len(p)):
        for j in range(len(p[i])):
            # Collect possible cells that we could have come from
            # Prior coordinate i - motion[0] (backwards in time - '%' signals cyclic array), same for j (other axis), p_stay * p[i][j] for if we didn't move 
            aux[i][j] = (p_move * p[(i - motion[0]) % len(p)][(j - motion[1]) % len(p[i])]) + (p_stay * p[i][j])
    # No nomralization needed because not Baye's Rule - return posterior distribution
    return aux

def show(p):
    for i in range(len(p)):
        print(p[i])


if len(measurements) != len(motions):
    raise ValueError('Error in size of measurement or motion vector')

# Give initial uniform distribution
p_init = 1.0 / float(len(colors)) / float(len(colors[0]))
p = [[p_init for row in range(len(colors[0]))] for col in range(len(colors))]

# Iterate
for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, colors, measurements[k])

show(p)
