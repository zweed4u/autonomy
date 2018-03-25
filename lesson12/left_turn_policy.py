#!/usr/bin/python3

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]

policy = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
          [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
          [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
          [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]

policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

change = True
while change is True:
    change = False
    # go through all cells and calculate values
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for orientation in range(4):
                if goal[0] == x and goal[1] == y:
                    if value[orientation][x][y] > 0:
                        value[orientation][x][y] = 0
                        policy[orientation][x][y] = '*'
                        change = True

                # cell navigable
                elif grid[x][y] == 0:
                    # calculate the 3 (actions) ways to propogate value
                    for i in range(3):
                        o2 = (orientation + action[i]) % 4
                        x2 = x + forward[o2][0]
                        y2 = y + forward[o2][1]

                        # cell is inside grid and not obstacle - add value of new cell and cost
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[o2][x2][y2] + cost[i]
                            if v2 < value[orientation][x][y]:
                                change = True
                                value[orientation][x][y] = v2
                                policy[orientation][x][y] = action_name[i]
# inital state
x = init[0]
y = init[1]
orientation = init[2]

# run policy - 3d to 2d
policy2D[x][y] = policy[orientation][x][y]

# while not in the goal state
while policy[orientation][x][y] != '*':
    if policy[orientation][x][y] == '#':
        o2 = orientation
    # turn right
    elif policy[orientation][x][y] == 'R':
        o2 = (orientation - 1) % 4
    # turn left
    elif policy[orientation][x][y] == 'L':
        o2 = (orientation + 1) % 4
    # apply forward motion
    x = x + forward[o2][0]
    y = y + forward[o2][1]
    # update orientation
    orientation = o2
    
    # copy 3d symbol for poolicy to 2d array
    policy2D[x][y] = policy[orientation][x][y]

for i in range(len(policy2D)):
    print(policy2D[i])

