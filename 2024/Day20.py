import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_waypoints(data_lines):
    waypoints = set()

    for y in range(len(data_lines)):
        for x in range(len(data_lines[y])):
            if data_lines[y][x] == '.':
                waypoints.add((x,y))
            elif data_lines[y][x] == 'S':
                START = (x,y)
            elif data_lines[y][x] == 'E':
                TARGET = (x,y)
    
    return waypoints, START, TARGET

def get_neighbors(node):
    x, y = node
    neighbors = set()

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) == abs(dy):
                continue
            neighbors.add((x+dx, y+dy))

    return neighbors

def get_diamond_neighbors(node, N, waypoint_distances):
    x, y = node
    neighbors = set()

    for dx in range(-N, N+1):
        for dy in {-(N-abs(dx)), (N-abs(dx))}:
            new_node = (x+dx, y+dy)
            if new_node in waypoint_distances and waypoint_distances[node] > waypoint_distances[new_node]:
                neighbors.add(new_node)
    
    return neighbors

def compute_distances_to_target(waypoints, START, TARGET):
    unvisited_waypoints = waypoints.copy()
    unvisited_waypoints.add(START)
    node = TARGET
    waypoint_distances = {}

    distance = 1
    while True:
        neighbors = get_neighbors(node)
        next_node = neighbors.intersection(unvisited_waypoints).pop()
        unvisited_waypoints.remove(next_node)
        waypoint_distances[next_node] = distance

        if next_node == START:
            break

        node = next_node
        distance += 1

    waypoint_distances[TARGET] = 0
    
    return waypoint_distances

def check_cheats(waypoint_distances, SAVINGS_TARGET, CHEAT_LENGTH):
    valid_cheats = 0
    
    for cheat_start_node in waypoint_distances.keys():

        cheat_end_nodes = set()
        for N in range(2, CHEAT_LENGTH+1):
            for cheat_end_node in get_diamond_neighbors(cheat_start_node, N, waypoint_distances):
                if cheat_end_node not in cheat_end_nodes and waypoint_distances[cheat_start_node] - waypoint_distances[cheat_end_node] - N >= SAVINGS_TARGET:
                    cheat_end_nodes.add(cheat_end_node)
                    valid_cheats += 1
    
    return valid_cheats


# Solution to part 1
def part_1():
    result = 0

    SAVINGS_TARGET = 100
    CHEAT_LENGTH = 2

    waypoints, START, TARGET = get_waypoints(data_lines)
    waypoint_distances = compute_distances_to_target(waypoints, START, TARGET)

    result = check_cheats(waypoint_distances, SAVINGS_TARGET, CHEAT_LENGTH)

    return result

# Solution to part 2
def part_2():
    result = 0

    SAVINGS_TARGET = 100
    CHEAT_LENGTH = 20

    waypoints, START, TARGET = get_waypoints(data_lines)
    waypoint_distances = compute_distances_to_target(waypoints, START, TARGET)

    result = check_cheats(waypoint_distances, SAVINGS_TARGET, CHEAT_LENGTH)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
