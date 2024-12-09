import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_all_sequence_variants(difference_sequence):
    all_variants = [difference_sequence[1:]]
    for i in range(1, len(difference_sequence)):
        all_variants.append(difference_sequence[:i-1] + [difference_sequence[i-1] + difference_sequence[i]] + difference_sequence[i+1:])
    all_variants.append(difference_sequence[:-1])
    return all_variants

def get_difference_sequence(numbers_in_line):
    return [numbers_in_line[i+1] - numbers_in_line[i] for i in range(len(numbers_in_line)-1)]

def is_sequence_valid(difference_sequence):
    return (max(difference_sequence) <= 3 and min(difference_sequence) >= 1) or (max(difference_sequence) <= -1 and min(difference_sequence) >= -3)

# Solution to part 1
def part_1():
    result = 0

    for line in data_lines:
        numbers_in_line = list(map(lambda x: int(x), line.split()))
        difference_sequence = get_difference_sequence(numbers_in_line)
        result += is_sequence_valid(difference_sequence)

    return result

# Solution to part 2
def part_2():
    result = 0

    for line in data_lines:
        numbers_in_line = list(map(lambda x: int(x), line.split()))
        difference_sequence = get_difference_sequence(numbers_in_line)
        sequence_variants = get_all_sequence_variants(difference_sequence)

        for sequence_variant in sequence_variants:
            if is_sequence_valid(sequence_variant):
                result += 1
                break

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
