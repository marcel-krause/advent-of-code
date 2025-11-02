import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    result = 0

    # Add the first character to the end of the string
    data = data_raw.strip()
    s = data + data[0]

    # Find the numbers which occur multiple times and add their values
    for i in range(1, len(s)):
        curr = s[i]
        prev = s[i - 1]
        if curr == prev:
            result += int(curr)

    return result

# Solution to part 2
def part_2():
    result = 0

    data = data_raw.strip()
    step_size = len(data) // 2

    # Add the first half of the string to the end of the string
    s = data + data[:step_size]

    # Find the numbers which match the one halfway around the list
    for i in range(len(data)):
        curr = s[i]
        match = s[i + step_size]
        if curr == match:
            result += int(curr)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
