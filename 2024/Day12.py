import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def create_grid(data_lines):
    grid = [['.']*(len(data_lines[0])+2)]

    for y in range(len(data_lines)):
        line = ['.']
        for x in range(len(data_lines[y])):
            line.append(data_lines[y][x])
        line.append('.')
        grid.append(line)
    grid.append(['.']*(len(data_lines[0])+2))

    return grid

def get_neighbors(point):
    x, y = point
    neighbors = set()

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) == abs(dy):
                continue
            neighbors.add((x+dx, y+dy))
    
    return neighbors

def bfs(grid, unscanned_points, starting_point):
    starting_point_value = grid[starting_point[1]][starting_point[0]]
    visited_nodes = {starting_point}

    next_neighbors = {starting_point}
    boundaries = set()
    boundary_index = defaultdict(list)

    while len(next_neighbors) > 0:
        new_neighbors = set()
        for next_neighbor in next_neighbors:
            new_neighbor_candidates = get_neighbors(next_neighbor)

            for neighbor_candidate in new_neighbor_candidates:
                x, y = neighbor_candidate
                if grid[y][x] == starting_point_value:
                    if neighbor_candidate in visited_nodes:
                        continue
                    new_neighbors.add(neighbor_candidate)
                    visited_nodes.add(neighbor_candidate)
                else:
                    boundary = get_boundary(next_neighbor, neighbor_candidate)
                    boundaries.add(boundary)
                    boundary_index[boundary[0]].append(boundary)
                    boundary_index[boundary[1]].append(boundary)
        next_neighbors = new_neighbors.copy()
    
    area = len(visited_nodes)
    unscanned_points = unscanned_points.difference(visited_nodes)

    return starting_point_value, area, unscanned_points, boundaries, boundary_index

def get_boundary(current_point, neighbor_point):
    difference = (neighbor_point[0] - current_point[0], neighbor_point[1] - current_point[1])

    if difference == (-1, 0):
        dx = (-0.5, -0.5)
        dy = (-0.5, 0.5)
        boundary_type = 'v'
    elif difference == (0, -1):
        dx = (-0.5, 0.5)
        dy = (-0.5, -0.5)
        boundary_type = 'h'
    elif difference == (1, 0):
        dx = (0.5, 0.5)
        dy = (-0.5, 0.5)
        boundary_type = 'v'
    elif difference == (0, 1):
        dx = (-0.5, 0.5)
        dy = (0.5, 0.5)
        boundary_type = 'h'

    boundary = (
        (current_point[0]+dx[0], current_point[1]+dy[0]),
        (current_point[0]+dx[1], current_point[1]+dy[1]),
        boundary_type
    )

    return boundary

def calculate_cost(garden_areas, use_sides=False):
    cost = 0

    for gardens in garden_areas.values():
        for garden in gardens:
            cost_part = combine_sides(garden['boundaries'], garden['boundary_index']) if use_sides else len(garden['boundaries'])
            cost += garden['area']*cost_part
    
    return cost

def combine_sides(input_boundaries, boundary_index):
    boundaries = input_boundaries.copy()
    combined_boundaries = set()

    additional_sides = 0
    for boundary_list in boundary_index.values():
        if len(boundary_list) == 4:
            additional_sides += 2

    while len(boundaries) > 0:
        start_boundary = boundaries.pop()
        start_point, end_point, start_direction = start_boundary

        new_boundary_endpoints = set()
        new_boundary_endpoints.add(start_point[0] if start_direction == 'h' else start_point[1])

        pivot_points = [start_point, end_point]
        for i in range(len(pivot_points)):
            next_point = pivot_points[i]
            new_boundary_endpoints.add(next_point[0] if start_direction == 'h' else next_point[1])
            while True:
                for next_boundary in boundary_index[next_point]:
                    next_point_candidate = None
                    if next_boundary not in boundaries or next_boundary[2] != start_direction:
                        continue
                    next_point_candidate = next_boundary[i]
                    break
                
                if next_point_candidate is None:
                    break
                else:
                    next_point = next_point_candidate
                    boundaries.remove(next_boundary)
                    new_boundary_endpoints.add(next_point[0] if next_boundary[2] == 'h' else next_point[1])

        x1 = min(new_boundary_endpoints) if start_direction == 'h' else start_point[0]
        x2 = max(new_boundary_endpoints) if start_direction == 'h' else start_point[0]
        y1 = min(new_boundary_endpoints) if start_direction == 'v' else start_point[1]
        y2 = max(new_boundary_endpoints) if start_direction == 'v' else start_point[1]
        combined_boundaries.add(((x1, y1), (x2, y2), start_direction))

    return len(combined_boundaries) + additional_sides


# Solution to part 1
def part_1():
    result = 0

    grid = create_grid(data_lines)
    unscanned_points = {(x+1,y+1) for x in range(len(data_lines[0])) for y in range(len(data_lines))}
    garden_areas = defaultdict(list)

    while len(unscanned_points) > 0:
        starting_point_value, area, unscanned_points, boundaries, boundary_index = bfs(grid, unscanned_points, next(iter(unscanned_points)))
        garden_areas[starting_point_value].append(
            {
                'area': area,
                'boundaries': boundaries,
                'boundary_index': boundary_index
            }
        )
    
    result = calculate_cost(garden_areas, use_sides=False)

    return result

# Solution to part 2
def part_2():
    result = 0

    grid = create_grid(data_lines)
    unscanned_points = {(x+1,y+1) for x in range(len(data_lines[0])) for y in range(len(data_lines))}
    garden_areas = defaultdict(list)

    while len(unscanned_points) > 0:
        starting_point_value, area, unscanned_points, boundaries, boundary_index = bfs(grid, unscanned_points, next(iter(unscanned_points)))
        garden_areas[starting_point_value].append(
            {
                'area': area,
                'boundaries': boundaries,
                'boundary_index': boundary_index
            }
        )

    result = calculate_cost(garden_areas, use_sides=True)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
