import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def bit_criteria_filter(bit_list: list, filter_criterium: int) -> int:
    filter_list = bit_list
    j = 0
    while True:
        counter = [0 for _ in range(len(filter_list[0]))]
        for curr in filter_list:
            for i in range(len(curr)):
                counter[i] += int(curr[i])

        filter_criterium_list = list(map(lambda x: '0' if x < len(filter_list)/2 else '1', counter)) if filter_criterium == 0 else list(map(lambda x: '1' if x < len(filter_list)/2 else '0', counter))

        filter_list = [line for line in filter_list if line[j] == filter_criterium_list[j]]
        if len(filter_list) == 1:
            target_binary = ''.join(filter_list)
            return int(target_binary, 2)

        j += 1

# Solution to part 1
def part_1():
    counter = [0 for _ in range(len(data_lines[0]))]
    for curr in data_lines:
        for i in range(len(curr)):
            counter[i] += int(curr[i])
    most_common_bits = ''.join(list(map(lambda x: '0' if x < len(data_lines)/2 else '1', counter)))
    least_common_bits = ''.join(list(map(lambda x: '1' if x < len(data_lines)/2 else '0', counter)))

    gamma_rate = int(most_common_bits, 2)
    epsilon_rate = int(least_common_bits, 2)
    result = gamma_rate * epsilon_rate

    return result

# Solution to part 2
def part_2():
    oxygen_rating = bit_criteria_filter(data_lines, 0)
    co2_rating = bit_criteria_filter(data_lines, 1)
    result = oxygen_rating * co2_rating

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
