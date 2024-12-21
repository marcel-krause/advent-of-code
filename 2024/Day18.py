import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def corrupt_memory(data_lines, MAX_SIZE, MAX_INPUT):
    corrupted_memory = set()

    for i in range(MAX_INPUT):
        x, y = list(map(lambda x: int(x)+1, data_lines[i].split(',')))
        corrupted_memory.add((x,y))
    
    for i in range(MAX_SIZE+3):
        for j in [0, MAX_SIZE+2]:
            corrupted_memory.add((j, i))
            corrupted_memory.add((i, j))
    
    return corrupted_memory

def plot_memory(corrupted_memory, MAX_SIZE):
    for y in range(MAX_SIZE+3):
        line = ''
        for x in range(MAX_SIZE+3):
            line += '#' if (x,y) in corrupted_memory else '.'
        print(line)

def plot_memory_with_visited(corrupted_memory, visited_nodes, step, MAX_SIZE):
    print(f"After step {step}:")
    for y in range(MAX_SIZE+3):
        line = ''
        for x in range(MAX_SIZE+3):
            line += '#' if (x,y) in corrupted_memory else '0' if (x,y) in visited_nodes else '.'
        print(line)
    print()

def get_neighbors(current_node):
    neighbors = set()
    x, y = current_node

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) == abs(dy):
                continue
            neighbors.add((x+dx, y+dy))
    
    return neighbors

def bfs(corrupted_memory, STARTING_POINT, TARGET_POINT, MAX_SIZE):
    visited_nodes = {STARTING_POINT}

    next_nodes = {STARTING_POINT}

    # print("TARGET: ", TARGET_POINT)

    steps = 0
    while len(next_nodes) > 0:
        new_next_nodes = set()
        for current_node in next_nodes:
            if current_node == TARGET_POINT:
                return steps
            neighbors = get_neighbors(current_node).difference(corrupted_memory).difference(visited_nodes)
            visited_nodes.add(current_node)
            new_next_nodes = new_next_nodes.union(neighbors)
        next_nodes = new_next_nodes.copy()
        # print("next_nodes: ", next_nodes)
        # plot_memory_with_visited(corrupted_memory, visited_nodes, steps, MAX_SIZE)
        steps += 1

def half_interval(lower_limit, upper_limit):
    return upper_limit if upper_limit-lower_limit==1 else lower_limit + (upper_limit - lower_limit)//2

# Solution to part 1
def part_1():
    result = 0

    MAX_SIZE = 6 if input_type == 'sample' else 70
    MAX_INPUT = 12 if input_type == 'sample' else 1024
    STARTING_POINT = (1, 1)
    TARGET_POINT = (MAX_SIZE+1, MAX_SIZE+1)

    corrupted_memory = corrupt_memory(data_lines, MAX_SIZE, MAX_INPUT)
    result = bfs(corrupted_memory, STARTING_POINT, TARGET_POINT, MAX_SIZE)

    return result

# Solution to part 2
def part_2():
    result = 0

    MAX_SIZE = 6 if input_type == 'sample' else 70
    MAX_INPUT_START = 12 if input_type == 'sample' else 1024
    STARTING_POINT = (1, 1)
    TARGET_POINT = (MAX_SIZE+1, MAX_SIZE+1)

    lower_limit = MAX_INPUT_START
    upper_limit = len(data_lines)

    while True:
        max_input = half_interval(lower_limit, upper_limit)

        if upper_limit - lower_limit == 1:
            result = data_lines[max_input-1]
            break
        
        corrupted_memory = corrupt_memory(data_lines, MAX_SIZE, max_input)
        target_steps = bfs(corrupted_memory, STARTING_POINT, TARGET_POINT, MAX_SIZE)

        if target_steps:
            lower_limit = max_input
            pass
        else:
            upper_limit = max_input
            pass
    
    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
