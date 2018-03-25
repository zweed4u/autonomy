#!/usr/bin/python3
import json

def initial_belief():
    n = 5
    p = [1 / float(n) for index in range(0, 5)]
    print(f'Original cells: {p}')
    return p


def next_belief():
    # layout green, red, red, green, green
    # robot sees red
    initial_array = initial_belief()
    belief_dict = {
        'green': [
            initial_array[0],
            initial_array[3],
            initial_array[4]
        ],
        'red': [
            initial_array[1],
            initial_array[2]
        ]
    }
    # 3 times likely to be in the red cell than green cell
    factors = {
        'red': .6,
        'green': .2
    }

    updated_belief_dict = {
        'green': [],
        'red': []
    }
    for factor_color in factors:
        for cell in belief_dict[factor_color]:
            updated_belief_dict[factor_color].append(cell * factors[factor_color])
    print(json.dumps(updated_belief_dict, indent=4))
    print(f'But the sum of the probability is not 1.0.\nIt is: {sum(list(updated_belief_dict.values())[0])+sum(list(updated_belief_dict.values())[1])}')
    print('Therefore it is not a valid distribution')


    # Divide by sum to get back into probability distribution
    new_array = [.04, .12, .12, .04, .04]
    new_array_sum = sum(new_array)
    new_array_prob_fixed = []

    # Normalizing
    for prob in new_array:
        print(prob/float(new_array_sum))
        new_array_prob_fixed.append(prob/float(new_array_sum))
    print(new_array_prob_fixed)
    print(sum(new_array_prob_fixed))
    assert sum(new_array_prob_fixed) == 1.0, 'Probability distribution array still does not sum to 1.0 after normalization'


def pHit_pMiss():
    # Write code that outputs p after multiplying each entry
    # by pHit or pMiss at the appropriate places. Remember that
    # the red cells 1 and 2 are hits and the other green cells
    # are misses.

    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    pHit = 0.6
    pMiss = 0.2

    # Enter code here
    for i in range(0, len(p)):
        if i == 0 or i == 3 or i == 4:
            p[i] *= pMiss
        else:
            p[i] *= pHit
    print(p)
    print(sum(p))


def elegant_calc():
    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    world = ['green', 'red', 'red', 'green', 'green']
    # what the robot sees
    Z = 'red'
    pHit = 0.6
    pMiss = 0.2

    def sense(p, Z):
        q = []
        for i in range(0, len(p)):
            if world[i] == Z:
                q.append(p[i] * pHit)
            else:
                q.append(p[i] * pMiss)
        return q
    return sense(p, Z)


def elegant_normalize():
    # Modify your code so that it normalizes the output for
    # the function sense. This means that the entries in q
    # should sum to one.

    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    world = ['green', 'red', 'red', 'green', 'green']
    Z = 'green'
    pHit = 0.6
    pMiss = 0.2

    def sense(p, Z):
        q = []
        for i in range(len(p)):
            hit = (Z == world[i])
            q.append(p[i] * (hit * pHit + (1 - hit) * pMiss))

        # Measurement update
        unnormalized_sum = sum(q)
        for i in range(0, len(q)):
            q[i]/=float(unnormalized_sum)
        return q
    return sense(p, Z)


def multiple_measurements():
    # Modify the code so that it updates the probability twice
    # and gives the posterior distribution after both
    # measurements are incorporated. Make sure that your code
    # allows for any sequence of measurement of any length.

    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    world = ['green', 'red', 'red', 'green', 'green']
    measurements = ['red', 'green']
    pHit = 0.6
    pMiss = 0.2

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
    for measurement in measurements:
        p = sense(p, measurement)
    print(p)


multiple_measurements()
#print(elegant_normalize())
# print(elegant_calc())
# next_belief()
# pHit_pMiss()