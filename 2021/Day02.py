import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    horizontal_position = 0
    depth = 0
    for line in data_lines:
        curr_pos_change = int(line.split()[1])
        
        if 'forward' in line:
            horizontal_position += curr_pos_change
        if 'down' in line:
            depth += curr_pos_change
        if 'up' in line:
            depth -= curr_pos_change
    result = horizontal_position*depth

    return result

# Solution to part 2
def part_2():
    horizontal_position = 0
    aim = 0
    depth = 0
    for line in data_lines:
        curr_pos_change = int(line.split()[1])

        if 'forward' in line:
            horizontal_position += curr_pos_change
            depth += aim*curr_pos_change
        if 'down' in line:
            aim += curr_pos_change
        if 'up' in line:
            aim -= curr_pos_change
    result = horizontal_position*depth

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
