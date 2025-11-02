import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    data = int(data_lines[0])

    # Find the two squares between which the input data lies
    n = 1
    while True:
        sq_lower = (2 * (n - 1) + 1) ** 2
        sq_upper = (2 * n + 1) ** 2
        if sq_lower <= data <= sq_upper:
            break
        n += 1

    # Define min, max and starting values for Manhattan distance calculation
    min_dist = n
    max_dist = 2 * n
    curr_dist = 2 * n - 1
    start_val = (2 * (n - 1) + 1) ** 2 + 1
    val_diff = data - start_val
    add = -1

    # Iterate over the Manhattan distances that are possible
    for _ in range(val_diff):
        if curr_dist == min_dist:
            add = 1
        if curr_dist == max_dist:
            add = -1
        curr_dist += add

    result = curr_dist

    return result

# Solution to part 2
def part_2():
    data = int(data_lines[0])
    
    row = 0
    col = 0
    n = 0
    values = {}

    while True:
        adder = 0
        key = f"{col},{row}"
        if not values:
            values[key] = 1
            adder = 1
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    neighbor_key = f"{col + i},{row + j}"
                    if neighbor_key in values:
                        adder += values[neighbor_key]
            values[key] = adder

        if adder > data:
            break

        # Determine next position in the spiral
        if (row == 0 and col == 0) or (row == -n and col == n):
            n += 1
            col += 1
        elif col == n and row < n:
            row += 1
        elif row == n and col > -n:
            col -= 1
        elif col == -n and row > -n:
            row -= 1
        elif row == -n and col < n:
            col += 1

    result = adder

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
