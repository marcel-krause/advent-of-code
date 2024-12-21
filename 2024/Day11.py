import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

number_cache = {}

def change_stone(stone):
    if stone == 0:
        return [1]
    elif len(str(stone))%2 == 0:
        stone_string = str(stone)
        return [int(stone_string[:len(stone_string)//2]), int(stone_string[len(stone_string)//2:])]
    else:
        return [2024*stone]

def count_stones_after_blinks(blinks, stone):
    if blinks == 0:
        stone_count = 1
        number_cache[(0, stone)] = stone_count
        return stone_count
    
    next_numbers = change_stone(stone)
    total_stone_count = 0
    for n in next_numbers:
        if (blinks-1, n) in number_cache:
            stone_count = number_cache[(blinks-1, n)]
        else:
            stone_count = count_stones_after_blinks(blinks - 1, n)
            number_cache[(blinks-1, n)] = stone_count
        total_stone_count += stone_count

    return total_stone_count


# Solution to part 1
def part_1():
    result = 0

    MAX_BLINK = 25

    stones = list(map(lambda x: int(x), data_lines[0].split()))

    for stone in stones:
        result += count_stones_after_blinks(MAX_BLINK, stone)

    return result

# Solution to part 2
def part_2():
    result = 0

    MAX_BLINK = 75

    stones = list(map(lambda x: int(x), data_lines[0].split()))

    for stone in stones:
        result += count_stones_after_blinks(MAX_BLINK, stone)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
