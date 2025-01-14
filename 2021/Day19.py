import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def find_overlaps(ref_list, list_2) -> tuple[list, set]:
    permutations = {
        (0,1,2): 1,
        (1,2,0): 1,
        (2,0,1): 1,
        (2,1,0): -1,
        (1,0,2): -1,
        (0,2,1): -1
    }

    # Consider all rotations and coordinate transformations without changing the handedness of the coordinate system (i.e. no mirroring)
    for x in range(1,-2,-2):
        for y in range(1,-2,-2):
            for z in range(1,-2,-2):
                for permutation, parity in permutations.items():
                    # In case the parity does not match, consider the next coordinate transformation
                    if x*y*z*parity != 1:
                        continue

                    # Transform the coordinates of the second list
                    curr_scanner_result_list = []
                    for point in list_2:
                        new_point = [0,0,0]
                        multiplicator = [x,y,z]
                        for i in range(len(point)):
                            new_point[permutation[i]] = point[i]*multiplicator[i]
                        curr_scanner_result_list.append(new_point)

                    # Move any point in the transformed second list to any point in the reference list
                    for point in curr_scanner_result_list:
                        for ref_point in ref_list:
                            scanner_position = []
                            for i in range(len(point)):
                                scanner_position.append(ref_point[i] - point[i])

                            # Move the points to the current reference point
                            match_count = 0
                            transformed_points = set()
                            for old_point in curr_scanner_result_list:
                                new_point = []
                                for i in range(len(old_point)):
                                    new_point.append(old_point[i] + scanner_position[i])
                                new_point = tuple(new_point)
                                transformed_points.add(new_point)
                                if new_point in ref_list:
                                    match_count += 1
                            
                            # In case we find 12 overlapping points in this transformed system, we actually found two scanners that are in reach of each other
                            if match_count == 12:
                                return scanner_position, transformed_points
    return [], []


def get_squared_euclidean_distance(coordinates1: list[int], coordinates2: list[int]) -> int:
    return sum([(coordinates1[i] - coordinates2[i])**2 for i in range(len(coordinates1))])


def get_manhattan_distance(coordinates1: list, coordinates2: list) -> int:
    return sum([abs(coordinates1[i] - coordinates2[i]) for i in range(len(coordinates1))])

def get_scanner_result_list(data_lines):
    scanner_result_list = {}
    curr_scanner = None

    for line in data_lines:
        if "scanner" in line:
            curr_scanner = int(line.replace("--- scanner ", "").split()[0])
            scanner_result_list[curr_scanner] = set()
        elif "," in line:
            scanner_result_list[curr_scanner].add(tuple(map(lambda x: int(x), line.split(","))))
    
    return scanner_result_list

def calculate_scanner_distances(scanner_result_list):
    scanner_result_list_distances = {}
    for key, val in scanner_result_list.items():
        all_distances = set()
        for point1 in val:
            for point2 in val:
                if point1 == point2:
                    continue
                all_distances.add(get_squared_euclidean_distance(point1, point2))
        scanner_result_list_distances[key] = all_distances

    return scanner_result_list_distances

def find_likely_pairs(scanner_result_list_distances):
    scanner_pair_mapping = {}

    for i in range(len(scanner_result_list_distances)):
        for j in range(1, len(scanner_result_list_distances)):
            if i == j:
                continue
            if len(scanner_result_list_distances[i].intersection(scanner_result_list_distances[j])) >= 66:
                if i in scanner_pair_mapping:
                    scanner_pair_mapping[i].append(j)
                else:
                    scanner_pair_mapping[i] = [j]
    
    return scanner_pair_mapping

def create_scanner_queue(scanner_result_list, scanner_pair_mapping):
    remaining_scanners = set(range(1, len(scanner_result_list))) - set(scanner_pair_mapping[0])
    scanner_queue = {0: scanner_pair_mapping[0]}
    next_scanners_to_consider = scanner_pair_mapping[0].copy()

    while len(next_scanners_to_consider) > 0:
        temp_next_scanners = []
        for next_scanner_to_consider in next_scanners_to_consider:
            temp = []
            for scanner in scanner_pair_mapping[next_scanner_to_consider]:
                if scanner in remaining_scanners:
                    temp.append(scanner)
                    remaining_scanners.remove(scanner)
            if len(temp) > 0:
                scanner_queue[next_scanner_to_consider] = temp[:]
            temp_next_scanners += temp
        next_scanners_to_consider = temp_next_scanners.copy()
    
    return scanner_queue

def compute_beacon_and_scanner_positions(scanner_queue, scanner_result_list):
    scanner_positions = {0: [0,0,0]}
    beacon_positions = set()
    for beacon_position in scanner_result_list[0]:
        beacon_positions.add(tuple(beacon_position))

    # Check the scanner queue for actual overlapping scanners
    for scanner1 in scanner_queue.keys():
        for scanner2 in scanner_queue[scanner1]:

            # Search for overlaps between the two scanners
            scanner_positions[scanner2], transformed_points = find_overlaps(scanner_result_list[scanner1], scanner_result_list[scanner2])

            # No overlaps found
            if len(scanner_positions[scanner2]) == 0:
                continue

            # Save the beacon and scanner positions
            scanner_result_list[scanner2] = transformed_points
            for beacon_position in transformed_points:
                beacon_positions.add(tuple(beacon_position))
    
    return beacon_positions, scanner_positions

def compute_maximum_manhattan_distance(scanner_positions, scanner_result_list):
    max_manhattan_distance = 0

    for scanner1 in range(len(scanner_result_list)):
        for scanner2 in range(scanner1+1, len(scanner_result_list)):
            curr_manhattan_distance = get_manhattan_distance(scanner_positions[scanner1], scanner_positions[scanner2])
            if curr_manhattan_distance > max_manhattan_distance:
                max_manhattan_distance = curr_manhattan_distance

    return max_manhattan_distance

# Solution to part 1
def part_1():
    result = 0

    scanner_result_list = get_scanner_result_list(data_lines)
    scanner_result_list_distances = calculate_scanner_distances(scanner_result_list)
    scanner_pair_mapping = find_likely_pairs(scanner_result_list_distances)

    scanner_queue = create_scanner_queue(scanner_result_list, scanner_pair_mapping)
    beacon_positions, _ = compute_beacon_and_scanner_positions(scanner_queue, scanner_result_list)

    result = len(beacon_positions)

    return result

# Solution to part 2
def part_2():
    result = 0

    scanner_result_list = get_scanner_result_list(data_lines)
    scanner_result_list_distances = calculate_scanner_distances(scanner_result_list)
    scanner_pair_mapping = find_likely_pairs(scanner_result_list_distances)

    scanner_queue = create_scanner_queue(scanner_result_list, scanner_pair_mapping)
    _, scanner_positions = compute_beacon_and_scanner_positions(scanner_queue, scanner_result_list)

    result = compute_maximum_manhattan_distance(scanner_positions, scanner_result_list)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
