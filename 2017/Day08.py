import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def perform_operation(a, b, operator):
    if operator == '==':
        return a==b
    elif operator == '!=':
        return a!=b
    elif operator == '<':
        return a<b
    elif operator == '>':
        return a>b
    elif operator == '<=':
        return a<=b
    elif operator == '>=':
        return a>=b

# Solution to part 1
def part_1():
    result = 0
    registers = defaultdict(int)

    for line in data_lines:
        instruction_part, condition_part = line.split(' if ')
        condition_part = condition_part.split()
        a = registers[condition_part[0]]
        b = int(condition_part[2])
        condition_operator = condition_part[1]

        register, operator, value = instruction_part.split()
        value = int(value)
        operator = -1 if operator == 'dec' else 1

        if perform_operation(a, b, condition_operator):
            registers[register] += operator * value

    result = max(registers.values())

    return result

# Solution to part 2
def part_2():
    result = 0
    registers = defaultdict(int)

    highest_value = -float("inf")

    for line in data_lines:
        instruction_part, condition_part = line.split(' if ')
        condition_part = condition_part.split()
        a = registers[condition_part[0]]
        b = int(condition_part[2])
        condition_operator = condition_part[1]

        register, operator, value = instruction_part.split()
        value = int(value)
        operator = -1 if operator == 'dec' else 1

        if perform_operation(a, b, condition_operator):
            registers[register] += operator * value

            highest_value = max(list(registers.values()) + [highest_value])

    result = highest_value

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
