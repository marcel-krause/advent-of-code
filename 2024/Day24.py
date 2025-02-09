import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_wires_and_gates(data_lines, wire_values):
    gates = []
    calculated_wires = set()
    sorted_gates = defaultdict(list)
    z_wires = set()
    output_map = {}

    for line in data_lines:
        if ':' in line:
            wire, value = line.split(': ')
            wire_values[wire] = int(value)
            calculated_wires.add(wire)
        elif '->' in line:
            logic_part, output_wire = line.split(' -> ')
            calculated_wires.add(output_wire)
            input1, operator, input2 = logic_part.split()

            gates.append({
                'inputs': [input1, input2],
                'operator': operator,
                'output': output_wire
            })

            input_wire_numbers = {int(input1[1:]), int(input2[1:])} if 'x' in [input1[0], input2[0]] and 'y' in [input1[0], input2[0]] else None

            output_map[output_wire] = {
                'inputs': [input1, input2],
                'operator': operator,
                'input_wire_numbers': input_wire_numbers
            }

            if output_wire[0] == 'z':
                z_wires.add(output_wire)

    for gate in gates:
        if gate['inputs'][0] in calculated_wires and gate['inputs'][1] in calculated_wires:
            sorted_gates['calculable'].append(gate)
        else:
            sorted_gates['none_inputs'].append(gate)

    return sorted_gates, z_wires, output_map

def perform_operation(input1, input2, operator):
    if operator == 'AND':
        return input1 & input2
    elif operator == 'OR':
        return input1 | input2
    elif operator == 'XOR':
        return input1 ^ input2

def get_output(wire_values):
    z_wires = {}
    max_z = 0
    output_string = ''

    for wire, value in wire_values.items():
        if wire[0] == 'z':
            z_wires[int(wire[1:])] = value
            max_z = max(max_z, int(wire[1:]))
    
    for i in range(max_z, -1, -1):
        output_string += str(z_wires[i])
    
    return int(output_string, 2)

def check_if_addition_is_present(input, z, operator):
    return input["input_wire_numbers"] is not None and z in input["input_wire_numbers"] and input["operator"] == operator

# Solution to part 1
def part_1():
    result = 0

    wire_values = defaultdict(int)

    gates, z_wires, _ = get_wires_and_gates(data_lines, wire_values)
    calculable_gate_indizes = set()

    while len(calculable_gate_indizes) < len(gates['calculable']) and len(z_wires) > 0:
        for i in range(len(gates['calculable'])):
            if i in calculable_gate_indizes:
                continue
            gate = gates['calculable'][i]
            input1, input2 = gate['inputs']
            operator = gate['operator']
            output_wire = gate['output']

            if input1 not in wire_values or input2 not in wire_values:
                continue

            wire_values[output_wire] = perform_operation(wire_values[input1], wire_values[input2], operator)
            calculable_gate_indizes.add(i)

            if output_wire in z_wires:
                z_wires.remove(output_wire)

    result = get_output(wire_values)

    return result

# Solution to part 2
def part_2():
    result = 0

    wire_values = defaultdict(int)

    _, z_wires, output_map = get_wires_and_gates(data_lines, wire_values)
    incorrect_wires = []
    incorrect_nodes = []

    for z in range(len(z_wires)):
        z_wire = f"z{str(z).zfill(2)}"
        upper_layer_operator = "OR" if z==45 else "XOR"

        if output_map[z_wire]["operator"] != upper_layer_operator:
            incorrect_wires.append((z_wire, "upper_xor", output_map[z_wire]))
            continue

        if z >= 1:
            current_addition_present = False
            previous_addition_present = False

            for input in output_map[z_wire]["inputs"]:
                addition_offset = z-1 if z==45 else z
                addition_operator = "AND" if z==45 else "XOR"
                current_addition_present |= check_if_addition_is_present(output_map[input], addition_offset, addition_operator)

                if output_map[input]["input_wire_numbers"] is None:
                    if output_map[input]["operator"] != "OR" and z<45:
                        incorrect_wires.append((input, "lower_or", output_map[input]))
                        incorrect_nodes.append(input)
                    elif output_map[input]["operator"] != "AND" and z==45:
                        incorrect_wires.append((input, "lower_or", output_map[input]))
                    else:
                        for next_input in output_map[input]["inputs"]:
                            previous_operator = "XOR" if z==45 else "AND"
                            previous_addition_present |= check_if_addition_is_present(output_map[next_input], z-1, previous_operator)
                elif z == 1:
                    previous_addition_present |= check_if_addition_is_present(output_map[input], z, "XOR")
                    previous_addition_present |= check_if_addition_is_present(output_map[input], z-1, "AND")
                
            if not current_addition_present:
                incorrect_wires.append((z_wire, "new_add", output_map[z_wire]))
            if not previous_addition_present:
                incorrect_wires.append((z_wire, "prev_add", output_map[z_wire]))

    for inc in incorrect_wires:
        if inc[1] == 'upper_xor':
            incorrect_nodes.append(inc[0])
            if inc[2]['operator'] == 'AND' and inc[2]['inputs'][0][0] not in ['x', 'y']:
                search_wires = ','.join(sorted(inc[2]['inputs']))
                for key, val in output_map.items():
                    if search_wires == ','.join(sorted(val['inputs'])) and key != inc[0]:
                        incorrect_nodes.append(key)
            continue
        if inc[1] == 'prev_add':
            for new_inp in inc[2]["inputs"]:
                if output_map[new_inp]['operator'] != 'OR':
                    continue
                
                for another_new_inp in output_map[new_inp]["inputs"]:
                    if output_map[another_new_inp]['operator'] == 'XOR':
                        incorrect_nodes.append(another_new_inp)
        if inc[1] == 'new_add':
            for new_inp in inc[2]["inputs"]:
                if output_map[new_inp]['operator'] == 'AND':
                    incorrect_nodes.append(new_inp)

    result = ','.join(sorted(incorrect_nodes))

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
