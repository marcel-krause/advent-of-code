import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    result = 0

    for line in data_lines:
        seen = set()
        words = line.split()
        for word in words:
            if word in seen:
                break
            seen.add(word)
        else:
            result += 1

    return result

# Solution to part 2
def part_2():
    result = 0

    for line in data_lines:
        seen = set()
        words = line.split()
        for word in words:
            sorted_word = ''.join(sorted(word))
            if sorted_word in seen:
                break
            seen.add(sorted_word)
        else:
            result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
