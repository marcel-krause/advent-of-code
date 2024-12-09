import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import re

# Solution to part 1
def part_1():
    result = 0

    regex_pattern = r'mul\(\d{1,3},\d{1,3}\)'

    for line in data_lines:
        matches = re.findall(regex_pattern, line)

        for match in matches:
            match_numbers = list(map(lambda x: int(x), match.replace('mul(', '').replace(')', '').split(',')))
            result += match_numbers[0] * match_numbers[1]

    return result

# Solution to part 2
def part_2():
    result = 0

    regex_pattern = r'(?:do\(\)|don\'t\(\)|mul\(\d{1,3},\d{1,3}\))'

    multiply_is_active = True
    for line in data_lines:
        matches = re.findall(regex_pattern, line)

        for match in matches:
            if "don't()" in match and multiply_is_active:
                multiply_is_active = False
                continue
            elif "do()" in match and not multiply_is_active:
                multiply_is_active = True
                continue
            if "do" not in match and multiply_is_active:
                match_numbers = list(map(lambda x: int(x), match.replace('mul(', '').replace(')', '').split(',')))
                result += match_numbers[0] * match_numbers[1]

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
