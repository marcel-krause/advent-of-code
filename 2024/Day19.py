import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_towels_and_designs(data_lines):
    towels = set(data_lines[0].split(', '))
    designs = data_lines[2:]

    towels_max_length = 0
    for towel in towels:
        towels_max_length = max(towels_max_length, len(towel))

    return towels, towels_max_length, designs

validated_designs = {}

def valid_designs(towels, towels_max_length, design):
    valid = 0

    for i in range(1, min(towels_max_length, len(design))+1):
        if design[:i] in towels:
            if len(design[i:]) == 0:
                valid += 1
            else:
                valid += valid_designs(towels, towels_max_length, design[i:]) if design[i:] not in validated_designs else validated_designs[design[i:]]
    
    validated_designs[design] = valid

    return valid


# Solution to part 1
def part_1():
    result = 0

    towels, towels_max_length, designs = get_towels_and_designs(data_lines)
    result = sum([1 if valid_designs(towels, towels_max_length, design) > 0 else 0 for design in designs])

    return result

# Solution to part 2
def part_2():
    result = 0

    towels, towels_max_length, designs = get_towels_and_designs(data_lines)
    result = sum([valid_designs(towels, towels_max_length, design) for design in designs])

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
