import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def create_grid(data_lines):
    FILL_NUMBER = 99
    trailheads = set()
    grid = [[FILL_NUMBER]*(len(data_lines[0])+2)]

    for y in range(len(data_lines)):
        row = [FILL_NUMBER]
        for x in range(len(data_lines[y])):
            current_number = int(data_lines[y][x])
            row.append(current_number)
            if current_number == 0:
                trailheads.add((x+1, y+1))
        row.append(FILL_NUMBER)
        grid.append(row)
    grid.append([FILL_NUMBER]*(len(data_lines[0])+2))

    return grid, trailheads

def get_next_neighbors(grid, current_node):
    x, y = current_node
    current_value = grid[y][x]
    current_next_neighbors = set()

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) == abs(dy):
                continue
            if grid[y+dy][x+dx] - current_value == 1:
                current_next_neighbors.add((x+dx, y+dy))
    
    return current_next_neighbors, current_value

def bfs(grid, starting_node, multiplicity_wanted=False):
    next_neighbors = defaultdict(int)
    next_neighbors[starting_node] += 1

    while True:
        multiplicity = defaultdict(int)
        for next_neighbor, current_multiplicity in next_neighbors.items():
            current_next_neighbors, current_value = get_next_neighbors(grid, next_neighbor)

            if current_value == 9 or len(next_neighbors) == 0:
                return sum(next_neighbors.values()) if multiplicity_wanted else len(next_neighbors)
            
            for key in current_next_neighbors:
                multiplicity[key] += current_multiplicity
            
        next_neighbors = multiplicity.copy()

# Solution to part 1
def part_1():
    result = 0

    grid, trailheads = create_grid(data_lines)

    for trailhead in trailheads:
        result += bfs(grid, trailhead, multiplicity_wanted=False)

    return result

# Solution to part 2
def part_2():
    result = 0

    grid, trailheads = create_grid(data_lines)

    for trailhead in trailheads:
        result += bfs(grid, trailhead, multiplicity_wanted=True)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
