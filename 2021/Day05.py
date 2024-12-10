import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_all_coordinates(data_lines):
    all_coordinates = []
    max_coordinate = 0

    for line in data_lines:
        coord_pair = line.rstrip('\n').split(' -> ')
        x1, y1 = list(map(lambda x: int(x), coord_pair[0].split(',')))
        x2, y2 = list(map(lambda x: int(x), coord_pair[1].split(',')))
        all_coordinates.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})

        pot_max = max([x1, x2, y1, y2]) + 1
        if pot_max > max_coordinate:
            max_coordinate = pot_max
    
    return all_coordinates, max_coordinate

def create_grid(max_coord):
    return [ [0 for _ in range(max_coord)] for _ in range(max_coord) ]

def put_vents_into_grid(grid, all_coordinates, consider_verticals=False):
    for curr_coord in all_coordinates:
        x1, x2, y1, y2 = curr_coord['x1'], curr_coord['x2'], curr_coord['y1'], curr_coord['y2']

        if x1 == x2:
            y_min, y_max = min(y1, y2), max(y1, y2)

            for y in range(y_min, y_max+1):
                grid[y][x1] += 1
        elif y1 == y2:
            x_min, x_max = min(x1, x2), max(x1, x2)
            
            for x in range(x_min, x_max+1):
                grid[y1][x] += 1
        elif consider_verticals and abs(x2 - x1) == abs(y2 - y1):
            x_range = range(x1, x2+1) if x2 >= x1 else range(x1, x2-1, -1)
            y_range = range(y1, y2+1) if y2 >= y1 else range(y1, y2-1, -1)
            target_points = list(zip(x_range, y_range))

            for coord_pair in target_points:
                grid[coord_pair[1]][coord_pair[0]] += 1
    return grid

def count_overlapping_vents(grid):
    num_overlapping_vents = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] > 1:
                num_overlapping_vents += 1

    return num_overlapping_vents

# Solution to part 1
def part_1():
    all_coordinates, max_coordinate = get_all_coordinates(data_lines)
    grid = create_grid(max_coordinate)
    grid_with_vents = put_vents_into_grid(grid, all_coordinates, consider_verticals=False)

    result = count_overlapping_vents(grid_with_vents)

    return result

# Solution to part 2
def part_2():
    all_coordinates, max_coordinate = get_all_coordinates(data_lines)
    grid = create_grid(max_coordinate)
    grid_with_vents = put_vents_into_grid(grid, all_coordinates, consider_verticals=True)

    result = count_overlapping_vents(grid_with_vents)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
