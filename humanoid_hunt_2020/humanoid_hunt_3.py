import numpy as np
import matplotlib.pyplot as plt
import time
# helper functions


def move_left(x,y):
    return x-1, y


def move_right(x,y):
    return x+1, y


def move_up(x,y):
    return x, y-1


def move_down(x,y):
    return x, y+1


def solve_maze(maze, x, y, stack_locations, stack_movements):
    if maze[move_right(x, y)] > 0:
        stack_locations.append(move_right(x, y))
        stack_movements.append('R')
        #print('moving right')
    elif maze[move_down(x, y)] > 0:
        stack_locations.append(move_down(x, y))
        stack_movements.append('D')
        #print('moving down')
    elif maze[move_left(x, y)] > 0:
        stack_locations.append(move_left(x, y))
        stack_movements.append('L')
        #print('moving left')
    elif maze[move_up(x, y)] > 0:
        stack_locations.append(move_up(x, y))
        stack_movements.append('U')
        #print('moving up')
    else:
        stack_locations.pop()
        stack_movements.pop()
        #print('backing up')
    if not stack_locations:
        return "Unable to find solution"
    else:
        x, y = stack_locations[-1]
        if maze[x, y] != 5:
            maze[x, y] = -1
        return maze, x, y, stack_locations, stack_movements

# get start time to see how long this takes
start = time.time()

#initialise an array that is hopefully big enough
paths = np.zeros((130,130))

with open('/Users/juusu53/PycharmProjects/untitled1/task_3.txt', 'r') as fp:
    lines = fp.readlines()

for j, line in enumerate(lines):
    # get initial location
    if ' ' in line:
        indices, movements = line.split()
        x, y = [int(j) for j in indices.split(',')]
        # transform movements to indices
        curr_x = x
        curr_y = y
        all_moves = movements.split(',')
        for i, next_move in enumerate(all_moves):
            if next_move in ['L','R','U','D']:
                paths[curr_x, curr_y] = 1
                if next_move == 'L':
                    curr_x, curr_y = move_left(curr_x, curr_y)
                elif next_move == 'R':
                    curr_x, curr_y = move_right(curr_x, curr_y)
                elif next_move == 'U':
                    curr_x, curr_y = move_up(curr_x, curr_y)
                elif next_move == 'D':
                    curr_x, curr_y = move_down(curr_x, curr_y)
            elif next_move == 'X':
                paths[curr_x, curr_y] = -2
            elif next_move == 'S':
                paths[curr_x, curr_y] = 3
            elif next_move == 'F':
                paths[curr_x, curr_y] = 5
            else:
                print('mystery letter ' + next_move + ' at line ' + str(j) + ' location ' + str(i))

# make all non-paths walls
paths[paths==0] = -2
# keep a copy of the path just in case
orig_paths = paths.copy()

plt.imshow(paths)
plt.colorbar()
plt.show()

# search for a path
start_location = np.where(paths==3)
stack_movements = []
stack_locations = []

x = start_location[0][0]
y = start_location[1][0]

while paths[x,y] < 5:
    #print(paths[x,y])
    paths, x, y, stack_locations, stack_movements = solve_maze(paths, x, y, stack_locations, stack_movements)

print(stack_locations)
print(stack_movements)

plt.imshow(paths)
plt.colorbar()
plt.savefig('maze_path.png')

movement_string = ",".join(stack_movements)

with open('/Users/juusu53/PycharmProjects/untitled1/task_3_solution.txt', 'w') as outfile:
    outfile.writelines(movement_string)

end = time.time()
print("Runtime of the program is " + str(end - start))