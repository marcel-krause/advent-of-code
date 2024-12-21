import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_grid_and_movements(data_lines, double_size=False):
    grid = []
    movements = []
    for y in range(len(data_lines)):
        if '#' in data_lines[y]:
            if double_size:
                line = []
                for i in list(data_lines[y]):
                    if i=='#' or i=='.':
                        line += [i, i]
                    elif i=='O':
                        line += ['[', ']']
                    else:
                        line += ['@', '.']
                grid.append(line)
            else:
                grid.append(list(data_lines[y]))

            if '@' in data_lines[y]:
                robot_position = (grid[-1].index('@'), y)
        elif data_lines[y] == '':
            continue
        else:
            movements += list(data_lines[y])
    
    return grid, movements, robot_position

def get_dx_dy(movement):
    if movement == '<':
        dx, dy = (-1, 0)
    elif movement == '>':
        dx, dy = (1, 0)
    elif movement == '^':
        dx, dy = (0, -1)
    elif movement == 'v':
        dx, dy = (0, 1)
    return dx, dy

def print_grid(grid, i, movement):
    print(f"After {i} movements (latest: '{movement}'):")
    for line in grid:
        print(''.join(line))
    print()

def get_connected_boxes(grid, robot_position, direction):
    boxes = []
    dx, dy = get_dx_dy(direction)

    next_checks = [(robot_position[0], robot_position[1])]

    while len(next_checks) > 0:
        new_next_check = []
        for next_check in next_checks:
            x, y = next_check
            next_box = None
            if grid[y+dy][x+dx] == 'O':
                next_box = ((x+dx, y+dy),)
            elif grid[y+dy][x+dx] == '#':
                return []
            elif direction in ['^', 'v']:
                if grid[y+dy][x] == '[':
                    next_box = ((x, y+dy), (x+1, y+dy))
                elif grid[y+dy][x] == ']':
                    next_box = ((x-1, y+dy), (x, y+dy))
            elif direction == '>' and grid[y][x+dx] == '[':
                next_box = ((x+dx, y), (x+dx+1, y))
            elif direction == '<' and grid[y][x+dx] == ']':
                next_box = ((x+dx-1, y), (x+dx, y))

            if next_box is not None:
                boxes.append(next_box)
                new_next_check += [next_box[0], next_box[1]] if len(next_box) == 2 else [next_box[0]]
        next_checks = new_next_check[:]

    return boxes

def move_connected_boxes(grid, connected_boxes, direction):
    dx, dy = get_dx_dy(direction)
    
    for i in range(len(connected_boxes)-1, -1, -1):
        if len(connected_boxes[i]) == 1:
            left_part = connected_boxes[i][0]
            new_left_part = (left_part[0] + dx, left_part[1] + dy)
            grid[left_part[1]][left_part[0]] = '.'
            grid[new_left_part[1]][new_left_part[0]] = 'O'
        else:
            left_part, right_part = connected_boxes[i]
            new_left_part = (left_part[0] + dx, left_part[1] + dy)
            new_right_part = (right_part[0] + dx, right_part[1] + dy)
            grid[left_part[1]][left_part[0]] = '.'
            grid[right_part[1]][right_part[0]] = '.'
            grid[new_left_part[1]][new_left_part[0]] = '['
            grid[new_right_part[1]][new_right_part[0]] = ']'

def move_robot(grid, robot_position, movement):
    x, y = robot_position
    dx, dy = get_dx_dy(movement)

    if grid[y+dy][x+dx] == '.':
        grid[y][x] = '.'
        grid[y+dy][x+dx] = '@'
    else:
        connected_boxes = get_connected_boxes(grid, robot_position, movement)

        if len(connected_boxes) == 0:
            return robot_position
        
        move_connected_boxes(grid, connected_boxes, movement)

        grid[y][x] = '.'
        grid[robot_position[1]+dy][robot_position[0]+dx] = '@'

    return (robot_position[0]+dx, robot_position[1]+dy)

def get_coordinate_sum(grid):
    grid_sum = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in ['O', '[']:
                grid_sum += 100*y + x

    return grid_sum


# Solution to part 1
def part_1():
    result = 0

    grid, movements, robot_position = get_grid_and_movements(data_lines, double_size=False)

    for i in range(len(movements)):
        robot_position = move_robot(grid, robot_position, movements[i])

    result = get_coordinate_sum(grid)

    return result

# Solution to part 2
def part_2():
    result = 0

    grid, movements, robot_position = get_grid_and_movements(data_lines, double_size=True)

    for i in range(len(movements)):
        robot_position = move_robot(grid, robot_position, movements[i])

    result = get_coordinate_sum(grid)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
