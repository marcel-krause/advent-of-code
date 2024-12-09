import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_antenna_positions(data_lines):
    antenna_positions = defaultdict(list)

    for y in range(len(data_lines)):
        for x in range(len(data_lines[y])):
            if data_lines[y][x] != '.':
                antenna_positions[data_lines[y][x]].append((x, y))

    return antenna_positions

def get_antenna_pairings(antenna_positions):
    antenna_pairings = defaultdict(list)

    for frequency, positions in antenna_positions.items():
        if len(positions) <= 1:
            continue
        for i in range(len(positions)-1):
            for j in range(i+1, len(positions)):
                antenna_pairings[frequency].append((positions[i], positions[j]))

    return antenna_pairings

def is_in_map(position, x_boundaries, y_boundaries):
    return position[0] in x_boundaries and position[1] in y_boundaries

def get_antinode_positions(antenna_pairings, x_boundaries, y_boundaries, collinear_mode=False):
    antinode_positions = set()

    for pairings in antenna_pairings.values():
        for pairing in pairings:
            first_location, second_location = pairing
            (dx, dy) = (first_location[0] - second_location[0], first_location[1] - second_location[1])
            
            if collinear_mode:
                i = 0
                while True:
                    antinode_position_candidate = (first_location[0] + i*dx, first_location[1] + i*dy)
                    if is_in_map(antinode_position_candidate, x_boundaries, y_boundaries):
                        antinode_positions.add(antinode_position_candidate)
                        i += 1
                        continue
                    break
                i = 0
                while True:
                    antinode_position_candidate = (second_location[0] - i*dx, second_location[1] - i*dy)
                    if is_in_map(antinode_position_candidate, x_boundaries, y_boundaries):
                        antinode_positions.add(antinode_position_candidate)
                        i += 1
                        continue
                    break
            else:
                antinode_position_candidates = [
                    (first_location[0] + dx, first_location[1] + dy),
                    (second_location[0] - dx, second_location[1] - dy)
                ]

                for antinode_position_candidate in antinode_position_candidates:
                    if is_in_map(antinode_position_candidate, x_boundaries, y_boundaries):
                        antinode_positions.add(antinode_position_candidate)
    
    return antinode_positions

# Solution to part 1
def part_1():
    result = 0

    x_boundaries, y_boundaries = range(len(data_lines[0])), range(len(data_lines))

    antenna_positions = get_antenna_positions(data_lines)
    antenna_pairings = get_antenna_pairings(antenna_positions)
    antinode_positions = get_antinode_positions(antenna_pairings, x_boundaries, y_boundaries, collinear_mode=False)

    result = len(antinode_positions)

    return result

# Solution to part 2
def part_2():
    result = 0

    x_boundaries, y_boundaries = range(len(data_lines[0])), range(len(data_lines))

    antenna_positions = get_antenna_positions(data_lines)
    antenna_pairings = get_antenna_pairings(antenna_positions)
    antinode_positions = get_antinode_positions(antenna_pairings, x_boundaries, y_boundaries, collinear_mode=True)

    result = len(antinode_positions)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
