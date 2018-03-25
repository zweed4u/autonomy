#!/usr/bin/python3

"""
Grid format:
0 = navigable space
1 = occupied space (wall block)
"""
#(r,c)
# Start 0,0 top left
# Goal 5,6 bottom right
grid = [[0 ,0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
start = [0, 0]
goal = [len(grid)-1, len(grid[0]) -1]

delta_actions = [[-1,0], # up
                 [0,-1], # left
                 [1,0], # down
                 [0,1]] # right
delta_names = ['^', '<', 'v', '>']
cost = 1

# gvalue (expansion from initial), x, y
def search(grid, start, goal, cost):
    # checked cells
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[start[0]][start[1]] = 1

    x = start[0]
    y = start[1]
    g = 0
    open = [[g, x, y]]

    found = False # flag for when search/expansion complete
    resign = False # flag if we cant expand for failing case
    
    # print('initial open list:')
    # for i in range(len(open)):
    #     print('   ', open[i])
    # print('----')

    while found is False and resign is False:
        # check is we still have elements in the open list - nothing left to expand
        if len(open) == 0:
            resign = True
            print('Fail')
            print('###### Search terminated without success')
        else:
            # remove node from list with smallest g value
            open.sort()
            open.reverse()
            next = open.pop()
            # print('take list item')
            # print(next)
            x = next[1]
            y = next[2]
            g = next[0]

            # check if we are done
            if x == goal[0] and y == goal[1]:
                found = True
                # print(next)
                print('##### Search successful')
                return next
            else:
                # expand winning element and add to new open list
                for i in range(len(delta_actions)):
                    # Go through all possible actions and apply to x and y
                    x2 = x + delta_actions[i][0]
                    y2 = y + delta_actions[i][1]

                    # if they fall into grid
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        
                        # if they are not yet checked
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            # print('append list item')
                            # print([g2, x2, y2])
                            closed[x2][y2] = 1

print(search(grid, start, goal, cost))