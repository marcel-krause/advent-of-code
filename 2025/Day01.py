import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    result = 0

    d = 50

    for line in data_lines:
        sign = -1 if line[0] == 'L' else 1
        d = (d + sign*int(line[1:]))%100

        if d == 0:
            result += 1

    return result

# Solution to part 2
def part_2():
    result = 0
    
    d = 50
    for line in data_lines:
        sign = -1 if line[0] == 'L' else 1

        if sign == -1 and d == 0:
            result -= 1

        d += sign*int(line[1:])

        result += abs(d//100)

        d %= 100

        if d == 0 and sign == -1:
            result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
