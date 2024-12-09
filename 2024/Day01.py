import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import Counter

def get_lists():
    left_list = []
    right_list = []
    for line in data_lines:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))
    return left_list, right_list

# Solution to part 1
def part_1():
    result = 0

    left_list, right_list = get_lists()
    left_list.sort()
    right_list.sort()

    difference_list = [abs(left_list[i] - right_list[i]) for i in range(len(left_list))]
    result = sum(difference_list)

    return result

# Solution to part 2
def part_2():
    result = 0

    left_list, right_list = get_lists()

    left_list_counter = dict(Counter(left_list))
    right_list_counter = dict(Counter(right_list))

    for key, val in left_list_counter.items():
        if key not in right_list_counter.keys():
            continue
        result += right_list_counter[key]*key*val

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
