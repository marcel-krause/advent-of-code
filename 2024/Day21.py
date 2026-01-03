import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

shortest_paths_directional_keyboard = {
    'AA': 'A',
    'A^': '<A',
    'A>': 'vA',
    'Av': '<vA',
    'A<': 'v<<A',
    '^A': '>A',
    '^^': 'A',
    '^>': 'v>A',
    '^v': 'vA',
    '^<': 'v<A',
    '>A': '^A',
    '>^': '<^A',
    '>>': 'A',
    '>v': '<A',
    '><': '<<A',
    'vA': '^>A',
    'v^': '^A',
    'v>': '>A',
    'vv': 'A',
    'v<': '<A',
    '<A': '>>^A',
    '<^': '>^A',
    '<>': '>>A',
    '<v': '>A',
    '<<': 'A',
}
shortest_paths_directional_keyboard_lengths = { key: len(val) for key, val in shortest_paths_directional_keyboard.items() }

def create_numerical_keyboard(key_positions):
    keyboard = []

    for y in range(6):
        line = []
        for x in range(5):
            if (y, x) not in key_positions.values():
                line.append('X')
            else:
                for key, val in key_positions.items():
                    if val == (y, x):
                        line.append(key)
                        break

        keyboard.append(line)

    return keyboard

def convert_paths_to_arrows(paths):
    arrow_map = {
        '32': 'v',
        '23': '>',
        '21': '<',
        '12': '^',
    }

    converted_paths = []

    for path in paths:

        arrow_path = []

        for i in range(len(path)-1):
            ay, ax = path[i]
            by, bx = path[i+1]

            arrow_path.append(arrow_map[str(10*(by - ay + 2) + bx - ax + 2)])
        
        arrow_path.append('A')

        converted_paths.append(''.join(arrow_path))

    return converted_paths

def select_shortest_arrow_path(arrow_paths):
    path_length = float('inf')
    shortest_path = ''

    for arrow_path in arrow_paths:
        arrow_path_list = list(arrow_path)
        current_path_length = sum([ shortest_paths_directional_keyboard_lengths[arrow_path_list[i] + arrow_path_list[i+1]] for i in range(len(arrow_path_list)-1) ])

        if current_path_length < path_length:
            path_length = current_path_length
            shortest_path = arrow_path

    return shortest_path

def filter_arrow_paths(arrow_paths):
    punishing_points = float('inf')

    punishing_path_points = {}

    for arrow_path in arrow_paths:
        arrow_path_list = list(arrow_path)
        current_punishing_points = 0

        for i in range(len(arrow_path_list)-1):
            if arrow_path_list[i] != arrow_path_list[i+1]:
                current_punishing_points += 1

        punishing_path_points[arrow_path] = current_punishing_points

        if current_punishing_points < punishing_points:
            punishing_points = current_punishing_points

    filtered_paths = []

    for key, val in punishing_path_points.items():
        if val == punishing_points:
            filtered_paths.append(key)

    return select_shortest_arrow_path(filtered_paths)

def get_shortest_path_numerical_keyboard(source_coordinate, target_coordinate, keyboard):
    visited_coordinates = {source_coordinate}
    
    next_paths = [ [source_coordinate] ]
    shortest_paths = []

    while len(next_paths) > 0 and len(shortest_paths) == 0:
        new_next_paths = []

        for next_path in next_paths:
            sy, sx = next_path[-1]

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == dy == 0 or abs(dx) == abs(dy) == 1:
                        continue

                    new_coordinate = (sy + dy, sx + dx)

                    if new_coordinate == target_coordinate:
                        shortest_paths.append(next_path + [target_coordinate])

                    if keyboard[new_coordinate[0]][new_coordinate[1]] == 'X':
                        continue

                    new_next_paths.append(next_path + [new_coordinate])
                    visited_coordinates.add(new_coordinate)

        next_paths = new_next_paths[:]

    arrow_paths = convert_paths_to_arrows(shortest_paths)

    return filter_arrow_paths(arrow_paths)

def create_shortest_paths_numerical_keyboard():
    key_positions = {
        '7': (1, 1),
        '8': (1, 2),
        '9': (1, 3),
        '4': (2, 1),
        '5': (2, 2),
        '6': (2, 3),
        '1': (3, 1),
        '2': (3, 2),
        '3': (3, 3),
        '0': (4, 2),
        'A': (4, 3),
    }
    
    keyboard = create_numerical_keyboard(key_positions)
    shortest_paths_numerical_keyboard = {}

    for source in key_positions.keys():
        for target in key_positions.keys():
            if source == target:
                shortest_paths_numerical_keyboard[source + target] = 'A'
            else:
                shortest_paths_numerical_keyboard[source + target] = get_shortest_path_numerical_keyboard(key_positions[source], key_positions[target], keyboard)

    return shortest_paths_numerical_keyboard

key_presses_cache = {}
def keypad_presses(source: str, target: str, level: int) -> int:
    key = source + target

    if level == 0:
        return shortest_paths_directional_keyboard_lengths[key]
    else:
        new_paths = ['A'] + list(shortest_paths_directional_keyboard[key])

        num_presses = 0
        for i in range(len(new_paths)-1):
            source, target = new_paths[i], new_paths[i+1]

            if source + target + str(level-1) in key_presses_cache:
                current_num_presses = key_presses_cache[source + target + str(level-1)]
            else:
                current_num_presses = keypad_presses(source, target, level-1)
                key_presses_cache[source + target + str(level-1)] = current_num_presses

            num_presses += current_num_presses

        return num_presses

def get_numeric_part_of_code(code):
    return int(code.replace('A', ''))

def compute_complexity(LEVEL):
    complexity = 0

    shortest_paths_numerical_keyboard = create_shortest_paths_numerical_keyboard()

    for code in data_lines:
        code_steps = ['A'] + list(code)
        code_directional_path = ''

        for i in range(len(code_steps)-1):
            code_directional_path += shortest_paths_numerical_keyboard[code_steps[i] + code_steps[i+1]]

        new_paths = ['A'] + list(code_directional_path)

        num_presses = 0
        for i in range(len(new_paths)-1):
            source, target = new_paths[i], new_paths[i+1]
            num_presses += keypad_presses(source, target, LEVEL-1)

        complexity += get_numeric_part_of_code(code) * num_presses

    return complexity


# Solution to part 1
def part_1():
    LEVEL = 2

    return compute_complexity(LEVEL)

# Solution to part 2
def part_2():
    LEVEL = 25

    return compute_complexity(LEVEL)

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
