#!/usr/bin/python3

# Optimal policies for all cells given the goal
# Value computation - similar to heuristic grid but considers blocked paths/walls - uses neighboring successful cells - start at goal (value = 0)
# Calculate value function

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost_step):
    # same size as world and large value for placeholder
    value = [[ 99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change is True:
        change = False
        # update - go through all grid cells
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                # is it the goal?
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True
                # not goal cell
                elif grid[x][y] == 0:
                    # go through all actions
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        # x2 and y2 are legitimate states and inside the grid and that its a navigable cell
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost_step

                            # value is better than the value we havce already
                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
    for i in range(len(value)):
        print(value[i])

compute_value(grid, goal, cost)