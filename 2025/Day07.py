import sys
from typing import List, Set, Tuple
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_splitter_and_start_positions(data_lines) -> Tuple[List[Set[int]], int]:
    splitter_positions = []
    starting_position = -1

    for line in data_lines:
        if 'S' in line:
            starting_position = line.index('S')
        if '^' not in line:
            continue
        indices = set([i for i, x in enumerate(line) if x == "^"])
        splitter_positions.append(indices)
    
    return splitter_positions, starting_position

# Solution to part 1
def part_1():
    result = 0

    splitter_positions, starting_position = get_splitter_and_start_positions(data_lines)
    beam_positions = set([starting_position])

    for splitter_line in splitter_positions:
        splitters_hit = splitter_line.intersection(beam_positions)

        result += len(splitters_hit)

        new_beam_positions = set()
        for splitter in splitters_hit:
            new_beam_positions.add(splitter-1)
            new_beam_positions.add(splitter+1)
        
        beam_positions = beam_positions - splitters_hit
        beam_positions.update(new_beam_positions)

    return result

# Solution to part 2
def part_2():
    result = 0
    
    splitter_positions, starting_position = get_splitter_and_start_positions(data_lines)
    beam_positions = set([starting_position])

    beam_multiplicities = defaultdict(int)
    beam_multiplicities[starting_position] = 1

    for splitter_line in splitter_positions:
        splitters_hit = splitter_line.intersection(beam_positions)

        new_beam_positions = set()
        for splitter in splitters_hit:
            multiplicity = beam_multiplicities[splitter]
            beam_multiplicities[splitter] = 0

            new_beam_positions.add(splitter-1)
            new_beam_positions.add(splitter+1)

            beam_multiplicities[splitter-1] += multiplicity
            beam_multiplicities[splitter+1] += multiplicity
        
        beam_positions = beam_positions - splitters_hit
        beam_positions.update(new_beam_positions)

    for multiplicity in beam_multiplicities.values():
        result += multiplicity

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
