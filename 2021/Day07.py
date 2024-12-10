import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_minimum_fuel(crab_positions, min_val, max_val, constant_burn_rate=True):
    min_fuel = float('Inf')

    for i in range(min_val, max_val+1):
        fuel = 0
        for j in crab_positions:
            fuel += abs(i-j) if constant_burn_rate else ((i-j)**2+abs(i-j))//2
        if fuel < min_fuel:
            min_fuel = fuel

    return min_fuel


# Solution to part 1
def part_1():
    crab_positions = list(map(lambda x: int(x), data_lines[0].split(',')))
    min_val, max_val = min(crab_positions), max(crab_positions)
    result = get_minimum_fuel(crab_positions, min_val, max_val, constant_burn_rate=True)

    return result

# Solution to part 2
def part_2():
    crab_positions = list(map(lambda x: int(x), data_lines[0].split(',')))
    min_val, max_val = min(crab_positions), max(crab_positions)
    result = get_minimum_fuel(crab_positions, min_val, max_val, constant_burn_rate=False)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
