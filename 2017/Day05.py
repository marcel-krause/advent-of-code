import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    result = 0

    curr_idx = 0

    while curr_idx < len(data_lines_int):
        data_lines_int[curr_idx] += 1
        curr_idx += data_lines_int[curr_idx] - 1
        result += 1

    return result

# Solution to part 2
def part_2():
    result = 0
    
    curr_idx = 0

    while curr_idx < len(data_lines_int):
        if data_lines_int[curr_idx] >= 3:
            data_lines_int[curr_idx] -= 1
            curr_idx += data_lines_int[curr_idx] + 1
        else:
            data_lines_int[curr_idx] += 1
            curr_idx += data_lines_int[curr_idx] - 1
        result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
