import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    result = 0

    for i in range(1, len(data_lines_int)):
        if data_lines_int[i] > data_lines_int[i-1]:
            result += 1

    return result

# Solution to part 2
def part_2():
    result = 0

    for i in range(1, len(data_lines_int)-2):
        if sum(data_lines_int[i:i+3]) > sum(data_lines_int[i-1:i+2]):
            result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
