import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_all_points(data_lines):
    points = []

    for line in data_lines:
        points.append(tuple(map(lambda x: int(x), line.split(','))))
    
    return points

def euclidean_squared_distance(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2

def get_closest_pairs(points, N=1000):
    distances_to_points = {}
    distances = []

    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            current_distance = euclidean_squared_distance(points[i], points[j])
            distances.append(current_distance)
            distances_to_points[current_distance] = (points[i], points[j])
    
    distances.sort()

    return [distances_to_points[dist] for dist in distances[:N]]

def create_grid(closest_pairs):
    grid = defaultdict(list)

    for pair in closest_pairs:
        grid[pair[0]].append(pair[1])
        grid[pair[1]].append(pair[0])

    return grid

def count_circuits(grid):
    circuit_sizes = []
    visited_points = set()

    while True:
        starting_points = list(p for p in grid.keys() if p not in visited_points)

        if len(starting_points) == 0:
            break

        circuit_size = 1
        initial_point = starting_points.pop()
        visited_points.add(initial_point)

        next_points = set([initial_point])

        while len(next_points) > 0:
            next_to_visit = []
            for next_point in next_points:
                next_to_visit += grid[next_point]

            next_points = set([p for p in next_to_visit if p not in visited_points])
            circuit_size += len(next_points)
            visited_points.update(next_points)

        circuit_sizes.append(circuit_size)


    circuit_sizes.sort(reverse=True)

    return circuit_sizes

def get_closest_pair_connections(closest_pairs):
    closest_pair_connections = set()
    for closest_pair in closest_pairs:
        closest_pair_connections.add(
            (closest_pair[0], closest_pair[1])
        )
        closest_pair_connections.add(
            (closest_pair[1], closest_pair[0])
        )
    return closest_pair_connections


# Solution to part 1
def part_1():
    N = 1000 if input_type == 'real' else 10

    result = 1

    points = get_all_points(data_lines)
    closest_pairs = get_closest_pairs(points, N)
    grid = create_grid(closest_pairs)
    circuit_sizes = count_circuits(grid)

    for c in circuit_sizes[:3]:
        result *= c

    return result

# Solution to part 2
def part_2():
    N_upper = 1000*(1000-1)//2
    N_lower = 0
    N = N_upper//2
    N_before = N
    last_closest_pair_connections = set()

    while True:
        points = get_all_points(data_lines)
        closest_pairs = get_closest_pairs(points, N)
        grid = create_grid(closest_pairs)
        circuit_sizes = count_circuits(grid)

        if len(circuit_sizes) == 1 and circuit_sizes[0] == 1000 and abs(N_before - N) == 1:
            closest_pair_connections = get_closest_pair_connections(closest_pairs)
            break

        last_closest_pair_connections = get_closest_pair_connections(closest_pairs)
        
        if len(circuit_sizes) == 1 and circuit_sizes[0] == 1000:
            N, N_before, N_upper = (N - N_lower)//2, N, N
        else:
            N, N_before, N_lower = (N_upper + N)//2, N, N

    last_pair = list(closest_pair_connections.difference(last_closest_pair_connections))

    return last_pair[0][0][0] * last_pair[0][1][0]

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
