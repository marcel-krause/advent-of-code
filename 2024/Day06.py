import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import copy

def create_grid(data_lines, visited_positions):
    grid = []
    for y in range(len(data_lines)):
        line = []
        for x in range(len(data_lines[y])):
            if data_lines[y][x] == '^':
                current_position = (x, y)
                current_direction = 0
                line.append('.')
                visited_positions.add(current_position)
            else:
                line.append(data_lines[y][x])
        grid.append(line)
    return (grid, current_position, current_direction)

def get_visited_positions(grid, starting_position, starting_direction, visited_positions):
    current_position = starting_position
    current_direction = starting_direction
    while True:
        dx, dy = get_dx_dy(current_direction)
        
        next_position = (current_position[0] + dx, current_position[1] + dy)

        if next_position[0] < 0 or next_position[1] < 0 or next_position[0] >= len(grid) or next_position[1] >= len(grid[0]):
            break

        if grid[next_position[1]][next_position[0]] == '#':
            current_direction = (current_direction + 1)%4
        else:
            current_position = next_position
            visited_positions.add(current_position)

def get_obstruction_configurations(current_grid, starting_position, starting_direction, visited_configurations):
    current_position = starting_position
    current_direction = starting_direction
    number_of_obstruction_positions = 0
    while True:
        dx, dy = get_dx_dy(current_direction)
        
        next_position = (current_position[0] + dx, current_position[1] + dy)

        if (next_position[0], next_position[1], current_direction) in visited_configurations:
            number_of_obstruction_positions += 1
            break

        if next_position[0] < 0 or next_position[1] < 0 or next_position[0] >= len(current_grid) or next_position[1] >= len(current_grid[0]):
            break

        if current_grid[next_position[1]][next_position[0]] == '#':
            current_direction = (current_direction + 1)%4
        else:
            current_position = next_position
        visited_configurations.add((current_position[0], current_position[1], current_direction))
    
    return number_of_obstruction_positions

def get_dx_dy(current_direction):
    if current_direction == 0:
        dx = 0
        dy = -1
    elif current_direction == 1:
        dx = 1
        dy = 0
    elif current_direction == 2:
        dx = 0
        dy = 1
    elif current_direction == 3:
        dx = -1
        dy = 0
    return (dx, dy)

# Solution to part 1
def part_1():
    result = 0

    visited_positions = set()

    grid, current_position, current_direction = create_grid(data_lines, visited_positions)
    
    get_visited_positions(grid, current_position, current_direction, visited_positions)
    
    result = len(visited_positions)

    return result

# Solution to part 2
def part_2():
    result = 0

    visited_positions = set()

    grid, current_position, current_direction = create_grid(data_lines, visited_positions)
    initial_position = current_position
    initial_direction = current_direction
    
    get_visited_positions(grid, current_position, current_direction, visited_positions)
    
    for visited_position in visited_positions:
        visited_configurations = set()
        if visited_position == initial_position:
            continue
        current_position = initial_position
        current_direction = initial_direction
        visited_configurations.add((current_position[0], current_position[1], current_direction))
        current_grid = copy.deepcopy(grid)
        current_grid[visited_position[1]][visited_position[0]] = '#'

        result += get_obstruction_configurations(current_grid, current_position, current_direction, visited_configurations)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
