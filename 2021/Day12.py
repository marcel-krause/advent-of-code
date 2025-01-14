import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_possible_directions(data_lines):
    directions = {}

    for line in data_lines:
        curr_directions = line.split('-')
        for i in range(2):
            start, end = curr_directions[i], curr_directions[1-i]
            if start in directions.keys():
                directions[start].append(end)
            else:
                directions[start] = [end]
    
    return directions

def filter_paths(possible_paths):
    return [line for line in possible_paths if line[-1] == "end"]


# Solution to part 1
def part_1():
    result = 0

    directions = get_possible_directions(data_lines)

    possible_paths = [["start"]]
    for curr_path in possible_paths:
        if curr_path[-1] == "end":
            continue
        next_points = directions[curr_path[-1]]
        for next_point in next_points:
            if next_point == "start" or (next_point != "end" and 97 <= ord(next_point[0]) <= 122 and next_point in curr_path):
                continue
            possible_paths.append(curr_path + [next_point])

    result = len(filter_paths(possible_paths))

    return result

# Solution to part 2
def part_2():
    result = 0
    
    directions = get_possible_directions(data_lines)

    possible_paths = [["start"]]
    small_caves = set()
    for curr_path in possible_paths:
        if curr_path[-1] == "end":
            continue
        next_points = directions[curr_path[-1]]
        for next_point in next_points:
            if next_point == "start":
                continue
            if next_point != "end" and 97 <= ord(next_point[0]) <= 122:
                small_caves.add(next_point)
                cave_visited_twice = False
                invalid_path = False
                for small_cave in small_caves:
                    if (curr_path + [next_point]).count(small_cave) > 2:
                        invalid_path = True
                        break

                    elif (curr_path + [next_point]).count(small_cave) == 2:
                        if cave_visited_twice:
                            invalid_path = True
                            break
                        else:
                            cave_visited_twice = True
                if invalid_path:
                    continue
            possible_paths.append(curr_path + [next_point])

    result = len(filter_paths(possible_paths))

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
