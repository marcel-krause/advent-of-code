import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import heapq
from collections import defaultdict

def get_grid(data_lines):
    grid = set()

    for y in range(len(data_lines)):
        for x in range(len(data_lines[y])):
            if data_lines[y][x] == '.':
                grid.add((x,y))
            elif data_lines[y][x] == 'S':
                SOURCE = (x,y)
            elif data_lines[y][x] == 'E':
                TARGET = (x,y)
    
    return grid, SOURCE, TARGET

def get_adjacent_nodes(grid, node, orientation, TARGET):
    x, y = node

    change_map = {
        (0, -1): {
            'single_change': ['l', 'r'],
            'new_orientation': 'u'
        },
        (1, 0): {
            'single_change': ['u', 'd'],
            'new_orientation': 'r'
        },
        (0, 1): {
            'single_change': ['l', 'r'],
            'new_orientation': 'd'
        },
        (-1, 0): {
            'single_change': ['u', 'd'],
            'new_orientation': 'l'
        },
    }

    adjacent_nodes = []

    for key, val in change_map.items():
        dx, dy = key
        new_node = (x+dx, y+dy)
        if new_node in grid:
            cost = 1
            if orientation in val['single_change']:
                cost += 1000
            new_orientation = val['new_orientation']
            adjacent_nodes.append((cost, new_node, new_orientation))

    return adjacent_nodes

def dijkstra_algorithm(initial_grid, SOURCE, TARGET, START_ORIENTATION):
    grid = initial_grid.copy()
    grid.add(TARGET)
    queue = [(0, SOURCE, START_ORIENTATION)]

    distances = {f"{key},{orientation}": float("Inf") for key in grid for orientation in ['u', 'd', 'l', 'r']}
    for orientation in ['u', 'd', 'l', 'r']:
        distances[f"{SOURCE},{orientation}"] = 0
    previous = defaultdict(set)

    while queue:
        _, current_node, current_orientation = heapq.heappop(queue)

        for cost, next_node, new_orientation in get_adjacent_nodes(grid, current_node, current_orientation, TARGET):
            if distances[f"{next_node},{new_orientation}"] >= distances[f"{current_node},{current_orientation}"] + cost:
                distances[f"{next_node},{new_orientation}"] = distances[f"{current_node},{current_orientation}"] + cost
                if (distances[f"{next_node},{new_orientation}"], next_node, new_orientation) not in queue:
                    heapq.heappush(queue, (distances[f"{next_node},{new_orientation}"], next_node, new_orientation))
                previous[f"{next_node},{new_orientation}"].add(f"{current_node},{current_orientation}")
        
    return distances, previous

def convert_node_with_orientation_to_node(node):
    return tuple(map(lambda x: int(x), node.replace('(','').replace(')','')[:-2].split(', ')))

def get_optimal_paths(distances, previous, minimum_nodes, SOURCE):
    optimal_paths = {convert_node_with_orientation_to_node(minimum_node) for minimum_node in minimum_nodes}
    optimal_paths.add(SOURCE)
    next_nodes = set()
    for target_node in minimum_nodes:
        next_nodes = next_nodes.union(previous[target_node])

    while len(next_nodes) > 0:
        new_next_nodes = set()
        for next_node in next_nodes:
            if next_node not in previous:
                continue
            optimal_paths.add(convert_node_with_orientation_to_node(next_node))
            new_next_nodes = new_next_nodes.union(previous[next_node])
        next_nodes = new_next_nodes.copy()

    return optimal_paths

def plot_grid(grid, previous, SOURCE, TARGET, X_MAX, Y_MAX):
    for y in range(Y_MAX):
        line = ''
        for x in range(X_MAX):
            node = (x,y)
            if node in previous:
                line += 'O'
            elif node == SOURCE:
                line += 'S'
            elif node == TARGET:
                line += 'E'
            elif node in grid:
                line += '.'
            else:
                line += '#'
        print(line)
    print()

def get_minimum_distance(distances, TARGET):
    minimum_distance = float("Inf")
    minimum_nodes = defaultdict(set)

    for orientation in ['u', 'r', 'd', 'l']:
        if distances[f"{TARGET},{orientation}"] <= minimum_distance:
            minimum_distance = distances[f"{TARGET},{orientation}"]
            minimum_nodes[minimum_distance].add(f"{TARGET},{orientation}")

    return minimum_distance, minimum_nodes[minimum_distance]


# Solution to part 1
def part_1():
    result = 0

    grid, SOURCE, TARGET = get_grid(data_lines)
    START_ORIENTATION = 'r'

    distances, _ = dijkstra_algorithm(grid, SOURCE, TARGET, START_ORIENTATION)
    result, _ = get_minimum_distance(distances, TARGET)

    return result

# Solution to part 2
def part_2():
    result = 0

    grid, SOURCE, TARGET = get_grid(data_lines)
    START_ORIENTATION = 'r'

    distances, previous = dijkstra_algorithm(grid, SOURCE, TARGET, START_ORIENTATION)
    _, minimum_nodes = get_minimum_distance(distances, TARGET)
    optimal_paths = get_optimal_paths(distances, previous, minimum_nodes, SOURCE)
    result = len(optimal_paths)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
