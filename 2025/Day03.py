import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    jolts = []

    for line in data_lines:
        batteries = list(map(lambda x: int(x), list(line)))
        
        max_left_val = max(batteries[:-1])
        max_left_val_idx = batteries.index(max_left_val)
        max_right_val = max(batteries[max_left_val_idx+1:])

        jolts.append(10*max_left_val + max_right_val)

    return sum(jolts)

# Solution to part 2
def part_2():
    jolts = []

    for line in data_lines:
        batteries = list(map(lambda x: int(x), list(line)))
        
        current_jolt = 0
        max_val_idx = -1
        for residuals in range(-11, 1):
            search_interval = batteries if residuals == 0 else batteries[:residuals]
            residual_interval = batteries[residuals:]

            max_val = max(search_interval)
            max_val_idx = search_interval.index(max_val)
            current_jolt += 10**abs(residuals) * max_val

            batteries = search_interval[max_val_idx+1:] + residual_interval


        jolts.append(current_jolt)

    return sum(jolts)

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
