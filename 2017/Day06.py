import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    result = 0

    blocks = list(map(int, data_raw.strip().split()))
    block_configs = {','.join(map(str, blocks))}

    while True:
        max_val = max(blocks)
        max_idx = blocks.index(max_val)

        blocks[max_idx] = 0
        i = (max_idx + 1) % len(blocks)
        for _ in range(max_val):
            blocks[i] += 1
            i = (i + 1) % len(blocks)

        new_state = ','.join(map(str, blocks))
        result += 1
        if new_state in block_configs:
            break
        block_configs.add(new_state)

    return result

# Solution to part 2
def part_2():
    blocks = list(map(int, data_raw.strip().split()))
    iterations = 0
    block_configs = {','.join(map(str, blocks))}
    block_first_pass = False
    second_iterations = 0
    first_pass_state = ''

    while True:
        max_val = max(blocks)
        max_idx = blocks.index(max_val)

        blocks[max_idx] = 0
        i = (max_idx + 1) % len(blocks)
        for _ in range(max_val):
            blocks[i] += 1
            i = (i + 1) % len(blocks)

        new_state = ','.join(map(str, blocks))
        iterations += 1

        if block_first_pass:
            second_iterations += 1
            if new_state == first_pass_state:
                break
        else:
            if new_state in block_configs:
                block_first_pass = True
                first_pass_state = new_state
            else:
                block_configs.add(new_state)

    return second_iterations

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
