import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    STEPS = int(data_lines[0])
    buffer = [0]
    idx = 0

    for counter in range(1, 2018):
        idx = (idx + STEPS)%len(buffer) + 1
        buffer = buffer[:idx] + [counter] + buffer[idx:]

    return buffer[(idx+1)%len(buffer)]

# Solution to part 2
def part_2():
    STEPS = int(data_lines[0])
    idx = 0
    value_after_zero = None

    for counter in range(1, 50000001):
        idx = (idx + STEPS)%counter
    
        if idx == 0:
            value_after_zero = counter

        idx += 1

    return value_after_zero

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
