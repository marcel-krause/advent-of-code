import sys
from typing import List
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def extend_grid(data_lines: List[str]) -> List[List[str]]:
    extended_grid = []

    extended_grid.append(['.']*(len(data_lines)+2))

    for line in data_lines:
        extended_grid.append(['.'] + list(line) + ['.'])

    extended_grid.append(['.']*(len(data_lines)+2))

    return extended_grid

def count_adjacent(extended_grid: List[List[str]], x: int, y: int) -> int:
    counter = 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx==dy==0:
                continue
            if extended_grid[y+dy][x+dx] == '@':
                counter += 1

    return counter

# Solution to part 1
def part_1():
    result = 0

    extended_grid = extend_grid(data_lines)
    
    for y in range(1, len(extended_grid)-1):
        for x in range(1, len(extended_grid[y])-1):
            if extended_grid[y][x] == '@' and count_adjacent(extended_grid, x, y) < 4:
                result += 1

    return result

# Solution to part 2
def part_2():
    result = 0

    extended_grid = extend_grid(data_lines)
    
    while True:
        movable_rolls = []
        for y in range(1, len(extended_grid)-1):
            for x in range(1, len(extended_grid[y])-1):
                if extended_grid[y][x] == '@' and count_adjacent(extended_grid, x, y) < 4:
                    result += 1
                    movable_rolls.append((x, y))
        
        if len(movable_rolls) == 0:
            break

        for movable in movable_rolls:
            x, y = movable
            extended_grid[y][x] = '.'

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
