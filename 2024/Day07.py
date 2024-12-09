import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import itertools

def get_target_and_equation_numbers(line):
    target_number, equation_numbers = line.split(': ')
    target_number = int(target_number)
    equation_numbers = list(map(lambda x: int(x), equation_numbers.split(' ')))
    return target_number, equation_numbers

def combine_two_numbers(number_one, number_two, operator):
    if operator == '+':
        return number_one + number_two
    elif operator == '*':
        return number_one * number_two
    elif operator == '|':
        return int(f'{number_one}{number_two}')
    
def check_valid_combinations(target_number, equation_numbers, operator_combinations):
    result = 0
    for operator_combination in operator_combinations:
        target_reached = False
        current_number = equation_numbers[0]
        for i in range(len(operator_combination)):
            current_number = combine_two_numbers(current_number, equation_numbers[i+1], operator_combination[i])
            if current_number > target_number:
                break
        if current_number == target_number:
            result += target_number
            break
    return result

# Solution to part 1
def part_1():
    result = 0

    for line in data_lines:
        target_number, equation_numbers = get_target_and_equation_numbers(line)
        operator_combinations = list(itertools.product('+*', repeat=len(equation_numbers)-1))

        result += check_valid_combinations(target_number, equation_numbers, operator_combinations)

    return result

# Solution to part 2
def part_2():
    result = 0

    for line in data_lines:
        target_number, equation_numbers = get_target_and_equation_numbers(line)
        operator_combinations = list(itertools.product('+*|', repeat=len(equation_numbers)-1))

        current_result = check_valid_combinations(target_number, equation_numbers, operator_combinations)
        result += current_result

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
