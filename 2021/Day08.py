import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_configurations_and_all_characters():
    # Get the configuration of each segment and calculate the sum of all digits
    # The reference configuration for each segment is as following:
    #   aaaa
    #  b    c
    #  b    c
    #   dddd
    #  e    f
    #  e    f
    #   gggg
    all_chars = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    digit_configuration = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9'
    }

    return digit_configuration, all_chars

# Solution to part 1
def part_1():
    result = 0
    for line in data_lines:
        output = line.split(' | ')[1].split()
        for out in output:
            if len(out) == 2 or len(out) == 4 or len(out) == 3 or len(out) == 7:
                result += 1

    return result

# Solution to part 2
def part_2():
    result = 0

    digit_configuration, all_chars = get_configurations_and_all_characters()

    for line in data_lines:
        initialization_line = line.split(' | ')[0]
        configurations = initialization_line.split()
        output = line.split(' | ')[1].split()

        # Find out which segment corresponds to 'a'
        segment_configuration = {}
        for initialization_sequence in configurations:
            if len(initialization_sequence) == 2:
                digit_1 = {i for i in initialization_sequence}
            elif len(initialization_sequence) == 3:
                digit_7 = {i for i in initialization_sequence}
            elif len(initialization_sequence) == 4:
                digit_4 = {i for i in initialization_sequence}
        segment_configuration[next(iter(digit_7 - digit_1))] = 'a'
        
        # Find out all other segments apart from 'd' and 'g'
        for char in all_chars:
            char_count = initialization_line.count(char)
            if char_count == 4:
                segment_configuration[char] = 'e'
            elif char_count == 6:
                segment_configuration[char] = 'b'
            elif char_count == 8:
                if char not in segment_configuration.keys():
                    segment_configuration[char] = 'c'
            elif char_count == 9:
                segment_configuration[char] = 'f'

        # Find out the configuration for 'd' and 'g'
        segment_configuration[next(iter({i for i in digit_4 if i not in segment_configuration.keys()}))] = 'd'
        segment_configuration[next(iter(all_chars - set(segment_configuration.keys())))] = 'g'

        # Replace the output digit configuration with the original one and get the actual digits
        output_replaced = [''.join(sorted(list(map(lambda x: segment_configuration[x], output_number)))) for output_number in output]
        output_digit = int(''.join([digit_configuration[x] for x in output_replaced]))
        result += output_digit

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
