import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    numbers = []
    operators = []
    for y in range(len(data_lines)):
        current_line = (' '.join(data_lines[y].split())).split()
        
        if y < len(data_lines)-1:
            current_line = list(map(lambda x: int(x), current_line))
            numbers.append(current_line)
        else:
            operators = current_line
    
    results = []
    for x in range(len(numbers[0])):
        current_result = 0 if operators[x] == '+' else 1

        for y in range(len(numbers)):
            if operators[x] == '+':
                current_result += numbers[y][x]
            else:
                current_result *= numbers[y][x]
        
        results.append(current_result)

    return sum(results)

# Solution to part 2
def part_2():
    reversed_input = [data_lines[y][::-1] for y in range(len(data_lines))]

    results = []
    block_numbers = []
    next_block = False
    for x in range(len(reversed_input[0])):
        if next_block:
            block_numbers = []
            next_block = False
            continue

        current_number = ''
        for y in range(len(reversed_input)):
            current_number += reversed_input[y][x]

        block_numbers.append(int(current_number.replace('+','').replace('*','')))

        if current_number[-1] == '+':
            results.append(sum(block_numbers))
            next_block = True
        elif current_number[-1] == '*':
            product = 1
            for num in block_numbers:
                product *= num
            results.append(product)
            next_block = True

    return sum(results)

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
