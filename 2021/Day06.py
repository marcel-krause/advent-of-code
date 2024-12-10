import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def initialize_lanternfish_configuration(all_starting_times):
    all_lanternfish = {day: 0 for day in range(9)}

    for starting_time in all_starting_times:
        all_lanternfish[starting_time] += 1

    return all_lanternfish

def iterate_over_days(all_lanternfish, TARGET_DAYS):
    for _ in range(1, TARGET_DAYS+1):
        newly_created_fish = all_lanternfish[0]
        for timer in all_lanternfish.keys():
            if timer < 8:
                all_lanternfish[timer] = all_lanternfish[timer+1]
        all_lanternfish[6] += newly_created_fish
        all_lanternfish[8] = newly_created_fish
    return all_lanternfish

# Solution to part 1
def part_1():
    TARGET_DAYS = 80

    all_starting_times = list(map(lambda x: int(x), data_lines[0].split(',')))
    all_lanternfish = initialize_lanternfish_configuration(all_starting_times)
    all_lanternfish_after_days = iterate_over_days(all_lanternfish, TARGET_DAYS)
    
    result = sum(all_lanternfish_after_days.values())

    return result

# Solution to part 2
def part_2():
    TARGET_DAYS = 256

    all_starting_times = list(map(lambda x: int(x), data_lines[0].split(',')))
    all_lanternfish = initialize_lanternfish_configuration(all_starting_times)
    all_lanternfish_after_days = iterate_over_days(all_lanternfish, TARGET_DAYS)

    result = sum(all_lanternfish_after_days.values())

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
