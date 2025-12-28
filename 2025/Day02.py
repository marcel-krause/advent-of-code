import sys
from typing import Generator
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_string_chunks(string: str, length: int) -> Generator[str, None, None]:
    return (string[0+i:length+i] for i in range(0, len(string), length))

# Solution to part 1
def part_1():
    ranges = data_lines[0].split(',')
    invalid_ids = []

    for r in ranges:
        lower, upper = list(map(lambda x: int(x), r.split('-')))

        for i in range(lower, upper+1):
            str_i = str(i)
            if len(str_i)%2 == 0:
                left_part, right_part = str_i[:len(str_i)//2], str_i[len(str_i)//2:]
            else:
                continue
            
            if left_part == right_part:
                invalid_ids.append(i)

    return sum(invalid_ids)

# Solution to part 2
def part_2():
    ranges = data_lines[0].split(',')
    invalid_ids = []

    for r in ranges:
        lower, upper = list(map(lambda x: int(x), r.split('-')))

        for i in range(lower, upper+1):
            str_i = str(i)

            for l in range(1, len(str_i)//2+1):
                chunk_set = set(get_string_chunks(str_i, l))
                
                if len(chunk_set) == 1:
                    invalid_ids.append(i)
                    break

    return sum(invalid_ids)

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
