import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_keys_and_locks(data_lines):
    locks = []
    keys = {
        0: defaultdict(set),
        1: defaultdict(set),
        2: defaultdict(set),
        3: defaultdict(set),
        4: defaultdict(set)
    }

    for block in range(0, len(data_lines), 8):
        cols = []
        for x in range(len(data_lines[block])):
            col_count = 0
            for y in range(7):
                if data_lines[block+y][x] == '#':
                    col_count += 1
            cols.append(col_count-1)
        
        if '#' in data_lines[block]:
            locks.append(cols)
        else:
            for col in keys.keys():
                keys[col][cols[col]].add(block)
    
    return keys, locks

def find_key_lock_pairs(keys, locks):
    matching_pairs = 0
    for lock in locks:
        fitting_keys = None
        for i in range(len(lock)):
            lock_col_size = lock[i]
            fitting_key_by_col = set()
            for j in range(6-lock_col_size):
                fitting_key_by_col = fitting_key_by_col.union(keys[i][j])
            
            if fitting_keys is None and len(fitting_key_by_col) > 0:
                fitting_keys = fitting_key_by_col
            else:
                fitting_keys = fitting_keys.intersection(fitting_key_by_col)
        
        matching_pairs += len(fitting_keys)
    return matching_pairs


# Solution to part 1
def part_1():
    result = 0

    keys, locks = get_keys_and_locks(data_lines)
    result = find_key_lock_pairs(keys, locks)

    return result

# Solution to part 2
def part_2():
    result = 'Merry Christmas!'

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
