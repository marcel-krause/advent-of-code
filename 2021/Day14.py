import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import numpy as np

def get_polymer_template_and_replacements(data_lines):
    polymer_template = data_lines[0]
    replacements = [data_lines[i] for i in range(2, len(data_lines))]

    return polymer_template, replacements

def get_molecules(replacements):
    rep = {}

    for i in replacements:
        key, val = i.split(' -> ')
        rep[key] = key[0] + val + key[1]

    molecules = list(rep.keys())

    return molecules, rep

def compute_replacement_matrix(molecules, replacement_map, STEPS):
    replacement_matrix_T = []

    for val in replacement_map.values():
        replacements = [val[:2], val[1:]]
        curr_row = [1 if i in replacements else 0 for i in molecules.copy()]
        replacement_matrix_T.append(curr_row)

    replacement_matrix = np.array(replacement_matrix_T, dtype='int64').transpose()
    replacement_matrix_exponentiated = np.linalg.matrix_power(replacement_matrix, STEPS)

    return replacement_matrix_exponentiated

def convert_polymer(polymer_template, molecules, replacement_map, STEPS):
    replacement_matrix_exponentiated = compute_replacement_matrix(molecules, replacement_map, STEPS)
    polymer_template_vector = np.array([1 if i in polymer_template else 0 for i in molecules], dtype='int64')
    final_polymer_vector = replacement_matrix_exponentiated.dot(polymer_template_vector).tolist()

    return final_polymer_vector

def count_elements(polymer_template, molecules, final_polymer_vector):
    element_count = {polymer_template[0]: 1}

    for i in range(len(final_polymer_vector)):
        if molecules[i][1] in element_count.keys():
            element_count[molecules[i][1]] += final_polymer_vector[i]
        else:
            element_count[molecules[i][1]] = final_polymer_vector[i]
    
    return element_count


# Solution to part 1
def part_1():
    result = 0

    STEPS = 10

    polymer_template, replacements = get_polymer_template_and_replacements(data_lines)
    molecules, replacement_map = get_molecules(replacements)

    final_polymer_vector = convert_polymer(polymer_template, molecules, replacement_map, STEPS)
    element_count = count_elements(polymer_template, molecules, final_polymer_vector)

    result = max(element_count.values()) - min(element_count.values())

    return result

# Solution to part 2
def part_2():
    result = 0
    
    STEPS = 40

    polymer_template, replacements = get_polymer_template_and_replacements(data_lines)
    molecules, replacement_map = get_molecules(replacements)

    final_polymer_vector = convert_polymer(polymer_template, molecules, replacement_map, STEPS)
    element_count = count_elements(polymer_template, molecules, final_polymer_vector)
    
    result = max(element_count.values()) - min(element_count.values())

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
