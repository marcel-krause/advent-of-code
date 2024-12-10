import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def generate_disk_map(input_as_list):
    disk_map = []
    for i in range(len(input_as_list)):
        if i%2 == 0:
            disk_map.append([i//2]*input_as_list[i])
        else:
            if input_as_list[i] == 0:
                disk_map.append([])
            else:
                disk_map.append(['.']*input_as_list[i])
    return disk_map

def flatten_disk_map(disk_map):
    return [x for xs in disk_map for x in xs]

def convert_disk_map_to_string(disk_map):
    flattened_disk_map = flatten_disk_map(disk_map)
    return ''.join(map(lambda x: str(x), flattened_disk_map))

def format_disk_map(disk_map):
    next_free_slot = 1
    while True:
        last_array = disk_map.pop()

        if last_array == []:
            continue

        current_number = last_array[0]
        array_length = len(last_array)
        original_array_length = array_length

        if current_number == '.':
            continue

        while True:
            if next_free_slot >= len(disk_map):
                flattened_disk_map = flatten_disk_map(disk_map)
                flattened_disk_map = flattened_disk_map + [current_number]*(original_array_length - flattened_disk_map.count(current_number))
                return flattened_disk_map
            remaining_space = disk_map[next_free_slot].count('.')
            sub_disk_map = disk_map[next_free_slot][:(len(disk_map[next_free_slot]) - remaining_space)]
            if array_length == remaining_space:
                disk_map[next_free_slot] = sub_disk_map + [current_number]*array_length
                next_free_slot += 2
                break
            elif array_length < remaining_space:
                disk_map[next_free_slot] = sub_disk_map + [current_number]*array_length + ['.']*(remaining_space - array_length)
                break
            else:
                disk_map[next_free_slot] = sub_disk_map + [current_number]*remaining_space
                array_length -= remaining_space
                next_free_slot += 2

def format_disk_map_file_based(disk_map):
    for i in range(len(disk_map)-1, -1, -2):
        disk_map_part = disk_map[i]
        part_length = len(disk_map_part)

        if part_length == 0:
            continue

        for j in range(1, i+1, 2):
            free_space_indices = [x for x,target in enumerate(disk_map[j]) if target=='.']
            if len(free_space_indices) < part_length:
                continue
            length_before = len(disk_map[j])
            disk_map[j] = disk_map[j][:free_space_indices[0]] + disk_map_part
            disk_map[j] += ['.']*(length_before - len(disk_map[j]))
            disk_map[i] = ['.']*part_length
            break
    formatted_disk_map = list(map(lambda x: 0 if x=='.' else x, flatten_disk_map(disk_map)))
    return formatted_disk_map

def calculate_checksum(formatted_disk_map):
    return sum([formatted_disk_map[i]*i for i in range(len(formatted_disk_map))])

# Solution to part 1
def part_1():
    result = 0

    input_as_list = list(map(lambda x: int(x), list(data_lines[0])))

    disk_map = generate_disk_map(input_as_list)
    formatted_disk_map = format_disk_map(disk_map)

    result = calculate_checksum(formatted_disk_map)

    return result

# Solution to part 2
def part_2():
    result = 0

    input_as_list = list(map(lambda x: int(x), list(data_lines[0])))

    disk_map = generate_disk_map(input_as_list)
    formatted_disk_map = format_disk_map_file_based(disk_map)

    result = calculate_checksum(formatted_disk_map)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
