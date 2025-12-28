import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    result = 0

    fresh_ranges = []
    ingredient_ids = []
    for line in data_lines:
        if '-' in line:
            lower, upper  = list(map(lambda x: int(x), line.split('-')))
            fresh_ranges.append(range(lower, upper+1))
        elif len(line) > 0:
            ingredient_ids.append(int(line))

    for ingredient_id in ingredient_ids:
        for current_range in fresh_ranges:
            if ingredient_id in current_range:
                result += 1
                break

    return result

# Solution to part 2
def part_2():
    result = 0
    
    unmerged_intervals = []
    merged_intervals = []
    for line in data_lines:
        if '-' in line:
            lower, upper  = list(map(lambda x: int(x), line.split('-')))
            unmerged_intervals.append((lower, upper))

    unmerged_intervals.sort(key=lambda x: x[0])
    merged_intervals.append(unmerged_intervals.pop(0))

    while len(unmerged_intervals) > 0:
        current_interval = unmerged_intervals.pop(0)
        last_interval = merged_intervals[-1]

        if current_interval[0] <= last_interval[1]:
            new_interval = (last_interval[0], max(last_interval[1], current_interval[1]))
            merged_intervals[-1] = new_interval
        else:
            merged_intervals.append(current_interval)
    
    for merged_interval in merged_intervals:
        result += merged_interval[1] - merged_interval[0] + 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
