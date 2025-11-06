import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_starting_values(data_lines):
    return int(data_lines[0].split()[-1]), int(data_lines[1].split()[-1])

# Solution to part 1
def part_1():
    result = 0

    FACTOR_A = 16807
    FACTOR_B = 48271
    DIVISOR = 2147483647
    MAX_ITERATIONS = 40000000

    next_value_a, next_value_b = get_starting_values(data_lines)

    for _ in range(MAX_ITERATIONS):
        next_value_a = (next_value_a * FACTOR_A) % DIVISOR
        next_value_b = (next_value_b * FACTOR_B) % DIVISOR

        if bin(next_value_a)[-16:] == bin(next_value_b)[-16:]:
            result += 1

    return result

# Solution to part 2
def part_2():
    result = 0

    FACTOR_A = 16807
    FACTOR_B = 48271
    DIVISOR = 2147483647
    MAX_ITERATIONS = 5000000

    values_a = []
    values_b = []

    next_value_a, next_value_b = get_starting_values(data_lines)

    while True:
        next_value_a = (next_value_a * FACTOR_A) % DIVISOR
        next_value_b = (next_value_b * FACTOR_B) % DIVISOR
        
        if next_value_a % 4 == 0:
            values_a.append(next_value_a)
        if next_value_b % 8 == 0:
            values_b.append(next_value_b)

        if len(values_a) >= MAX_ITERATIONS and len(values_b) >= MAX_ITERATIONS:
            break
    
    for i in range(MAX_ITERATIONS):
        if bin(values_a[i])[-16:] == bin(values_b[i])[-16:]:
            result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
