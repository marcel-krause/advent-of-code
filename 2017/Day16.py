import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

# Solution to part 1
def part_1():
    START_POSITION = 'abcdefghijklmnop'
    positions = list(START_POSITION)
    instructions = data_lines[0].split(',')

    for instruction in instructions:
        if instruction[0] == 's':
            delta = int(instruction[1:])
            positions = positions[-delta:] + positions[:-delta]
        elif instruction[0] == 'x':
            a, b = list(map(lambda x: int(x), instruction[1:].split('/')))
            positions[a], positions[b] = positions[b], positions[a]
        else:
            a, b = instruction[1:].split('/')
            a, b = positions.index(a), positions.index(b)
            positions[a], positions[b] = positions[b], positions[a]
            pass

    return ''.join(positions)

# Solution to part 2
def part_2():
    result = 0
    
    START_POSITION = 'abcdefghijklmnop'
    MAX_ITERATIONS = 1000000000
    positions = list(START_POSITION)
    instructions = data_lines[0].split(',')

    final_positions = {
        START_POSITION: 0
    }
    cycle_length = 1
    for i in range(1, 1001):
        for instruction in instructions:
            if instruction[0] == 's':
                delta = int(instruction[1:])
                positions = positions[-delta:] + positions[:-delta]
            elif instruction[0] == 'x':
                a, b = list(map(lambda x: int(x), instruction[1:].split('/')))
                positions[a], positions[b] = positions[b], positions[a]
            else:
                a, b = instruction[1:].split('/')
                a, b = positions.index(a), positions.index(b)
                positions[a], positions[b] = positions[b], positions[a]
                pass

        if ''.join(positions) in final_positions:
            cycle_length = i
            break
        else:
            final_positions[''.join(positions)] = i

    residual = MAX_ITERATIONS % cycle_length

    for key, val in final_positions.items():
        if val == residual:
            result = key
            break

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
