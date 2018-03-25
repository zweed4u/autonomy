#!/usr/bin/python3

p = [0.2, 0.2, 0.2, 0.2, 0.2]
# p = [0, 1, 0, 0, 0]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
motions = [1, 1]  # right and then right again
pHit = 0.6
pMiss = 0.2
pExact = .8
pOvershoot = .1
pUndershoot = .1


def sense(p, Z):
    q = []
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1 - hit) * pMiss))

    # Measurement update
    unnormalized_sum = sum(q)
    for i in range(0, len(q)):
        q[i] /= float(unnormalized_sum)
    return q


def move(p, U):
    # U is a motion number, number of grid cells moved to right or left
    q = [0, 0, 0, 0, 0]
    for i in range(0, len(p)):
        if i+U >= len(p):
            q[(U % i)-1] = p[i]
        else:
            q[i+U] = p[i]
    return q


def elegant_move(p, U):
    # U is a motion number, number of grid cells moved to right or left
    q = []
    for i in range(0, len(p)):
        q.append(p[(i-U) % len(p)])
    return q


def shooting_move(p, U):
    # U is a motion number, number of grid cells moved to right or left
    q = []
    for i in range(0, len(p)):
        s = pExact * p[(i-U) % len(p)]
        s += pOvershoot * p[(i-U-1) % len(p)]
        s += pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q


# Many moves to show robot becomes uncertain - goes to uniform distribution
# for i in range(0, 1000):
#     p = shooting_move(p, 1)

# Entropy
for i in range(0, len(measurements)):
    p = sense(p, measurements[i])
    p = shooting_move(p, motions[i])

print(world)
print(p)
print(f'\nMost likely position after {motions} seeing {measurements}:\nPosition {p.index(max(p))+1}')
