import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import re

def simplify_alu(alu_instructions: list[str]) -> tuple[str, str]:
    replacements = {}
    for line in alu_instructions:
        lhs = line.split("=", 1)[0].strip()
        rhs = line.split("=", 1)[1].strip()

        if lhs not in replacements.keys():
            replacements[lhs] = rhs
        else:
            replacements[lhs] = "({})".format(rhs.replace(lhs, replacements[lhs])) if "+" in rhs.replace(lhs, replacements[lhs]) else rhs.replace(lhs, replacements[lhs])
            if lhs == "z" and "y" in replacements.keys():
                replacements[lhs] = "({})".format(replacements[lhs].replace("y", replacements["y"])) if "+" in replacements[lhs].replace("y", replacements["y"]) else replacements[lhs].replace("y", replacements["y"])
    pattern = r"int\( \((.*==.*\))\) == 0"
    search_result = re.search(pattern, replacements["x"].lstrip("(").rstrip(")"))
    simplified_alu = "x[i] = " + search_result.group(1).replace("==", "!=").replace("z", "z[i-1]").replace("c[0]", "c[0][i]").replace("c[1]", "c[1][i]").replace("c[2]", "c[2][i]")
    simplified_alu += "\nz[i] = " + replacements["z"].lstrip("(((").rstrip(")))").replace("((", "(").replace("))", ")").replace("z", "z[i-1]").replace("x", "x[i]").replace("c[0]", "c[0][i]").replace("c[1]", "c[1][i]").replace("c[2]", "c[2][i]")
    return '\n'.join(alu_instructions), simplified_alu

def decompile_alu(alu_instructions: list[str]) -> tuple[str, str]:
    decompiled_instructions = ""
    line_is_initialize = False
    initialize_variable = ""
    for line in alu_instructions:
    
        pattern = r'[add|mul|div|mod|eql] ([0-9xyzw]) (\-?[0-9cxyzw]{1,2}\[?\d*\]?)'
        search_result = re.search(pattern, line)

        if "add " in line:
            if line_is_initialize and initialize_variable != "" and search_result.group(1) == initialize_variable:
                decompiled_instructions += "{0} = {1}\n".format(search_result.group(1), search_result.group(2))
                line_is_initialize = False
                initialize_variable = ""
            else:
                decompiled_instructions += "{0} = {0} + {1}\n".format(search_result.group(1), search_result.group(2))

        if "mul " in line:
            if search_result.group(2) == "0":
                line_is_initialize = True
                initialize_variable = search_result.group(1)
            else:
                decompiled_instructions += "{0} = {0} * {1}\n".format(search_result.group(1), search_result.group(2))

        if "div " in line:
            decompiled_instructions += "{0} = {0}//{1}\n".format(search_result.group(1), search_result.group(2))

        if "mod " in line:
            decompiled_instructions += "{0} = {0}%{1}\n".format(search_result.group(1), search_result.group(2))

        if "eql " in line:
            decompiled_instructions += "{0} = int( {0} == {1} )\n".format(search_result.group(1), search_result.group(2))

    return simplify_alu(decompiled_instructions.replace("w", "w[i]").rstrip("\n").split("\n"))

def compare_alus(all_alu_instructions: list[str]) -> tuple[str, str, str, list[list[int]]]:
    aggregated_alu_instructions = []
    parameter_index = 0
    diff_strings = {}

    for i in range(len(all_alu_instructions[0])):
        compare_line = ""
        for alu_instruction in all_alu_instructions:
            if compare_line == "":
                compare_line = alu_instruction[i]
            elif compare_line != alu_instruction[i]:
                replaced_alu_string = alu_instruction[i]
                for j in set(alu_instruction[i].split()) - set(compare_line.split()):
                    replaced_alu_string = replaced_alu_string.replace(j, "")
                compare_line = "{}c[{}]".format(replaced_alu_string, parameter_index)
                diff_strings[i] = replaced_alu_string
                parameter_index += 1
                break
        aggregated_alu_instructions.append(compare_line)

    c = []
    for i, intersect in diff_strings.items():
        c.append([int(alu_instruction[i].replace(intersect, "")) for alu_instruction in all_alu_instructions])
    
    decompiled_alu = decompile_alu(aggregated_alu_instructions)
    return '\n'.join(aggregated_alu_instructions).replace("w", "w[i]"), decompiled_alu[0], decompiled_alu[1], c

def find_v_constraints(c: list[list[int]]) -> tuple[dict, str]:
    queue = []
    c_mapping = {}
    for i in range(len(c[0])):
        if c[0][i] == 1:
            queue.append(i)
        else:
            j = queue.pop()
            c_mapping[j] = i
    c_mapping = dict(sorted(c_mapping.items()))

    constraints = "\n".join(["w[{1}] = w[{0}] + c[1][{1}] + c[2][{0}]".format(key, val) for key, val in c_mapping.items()])

    return c_mapping, constraints

def verbose_output(basic_alu_instructions: str, decompiled_alu: str, simplified_alu: str, c: list[list[int]], c_constraints: str) -> None:
    output = ( "Preliminary notes: the following explanation might only fit my puzzle input and might not work in general.\n\n"
                "The instructions in the ALU consist of {0} blocks, all of which have the following basic structure:\n\n{1}\n\n"
                "These instructions represent the following operations:\n\n{6}\n\n"
                "Here, w[i] represents the ith digit of the 14 digit model number (with 1 <= w[i] <= 9). The parameters c[0], c[1] and c[2] vary between each of the {0} blocks. They are given by:\n\nc[0] = {2}\nc[1] = {3}\nc[2] = {4}\n\n"
                "In essence, the ALU instructions can be reduced to the following operations operated on the ith block of the ALU instructions:\n\n{5}\n\n"
                "where z[-1]=0 set as the start value. Note that the value of z is carried over to the next block, while x and y are overwritten at the beginning of each block.\n\n"
                "The c[0][i] only carry two distinct values for the blocks. For each block where c[0][i]==1, we find c[1][i] >= 10. This means that x[i]==1 for all these blocks. In this case, the z[i] reduce to\n\n"
                "z[i] = 26*z[i-1] + (w[i] + c[2][i])\n\n"
                "which essentially means that for each block where c[0][i]==1, the previous value z[i-1] is moved to the next digit position in base 26 while (w[i] + c[2][i]) is added at the zeroth position in base 26.\n\n"
                "In case that c[0][i]==26, we have c[1][i] < 0. Assume that z[i-1] contains a non-zero smallest digit (w[j] + c[2][j]) in base 26. In this case, x[i]==0 can hold, which reduces the z[i] to\n\n"
                "z[i] = z[i-1]//26\n\n"
                "which essentially reduces all digit positions of z[i-1] by one in base 26 and removes the zeroth digit.\n\n"
                "There are exactly as many blocks with c[0][i]==1 in the ALU as with c[0][i]==26. Since we demand z[i]==0 for the last block in order for the model number to be valid, this means that x[i]==0 has to hold for all blocks with c[0][i]==26. From this, we find the following set of constraints for the parameters:\n\n{7}\n\n"
                "These constraints can be used to find the digits w[i] of all valid model numbers.\n"
            ).format(len(c[0]), basic_alu_instructions, c[0], c[1], c[2], simplified_alu, decompiled_alu, c_constraints)
    print(output)

def find_model_mumber_extremum(c_mapping: dict, c: list[list[int]], minimum=False) -> int:
    target_range = range(1, 10) if minimum else range(9, 0, -1)
    w = [0]*len(c[0])

    for key, val in c_mapping.items():
        for w[key] in target_range:
            w[val] = w[key] + c[1][val] + c[2][key]
            if 1 <= w[val] <= 9:
                break

    return int("".join(map(str, w)))

def get_all_alu_instructions(data_lines):
    all_alu_instructions = []
    temp = []
    for line in data_lines:
        if "inp" in line:
            if len(temp) > 0:
                all_alu_instructions.append(temp)
            temp = []
        else:
            temp.append(line)
    all_alu_instructions.append(temp)

    return all_alu_instructions


# Solution to part 1
def part_1():
    result = 0

    if input_type == 'sample':
        print("This snippet does not work as intended for the sample input. Please use your real input instead.")
        return result

    all_alu_instructions = get_all_alu_instructions(data_lines)

    # Compare the ALU instructions, simplify them and get the parameters
    basic_alu_instructions, decompiled_alu, simplified_alu, c = compare_alus(all_alu_instructions)
    c_mapping, c_constraints = find_v_constraints(c)
    verbose_output(basic_alu_instructions, decompiled_alu, simplified_alu, c, c_constraints)

    # Get the minimum valid model number
    result = find_model_mumber_extremum(c_mapping, c, minimum=False)

    return result

# Solution to part 2
def part_2():
    result = 0
    
    if input_type == 'sample':
        print("This snippet does not work as intended for the sample input. Please use your real input instead.")
        return result
    
    all_alu_instructions = get_all_alu_instructions(data_lines)

    # Compare the ALU instructions, simplify them and get the parameters
    basic_alu_instructions, decompiled_alu, simplified_alu, c = compare_alus(all_alu_instructions)
    c_mapping, c_constraints = find_v_constraints(c)
    verbose_output(basic_alu_instructions, decompiled_alu, simplified_alu, c, c_constraints)

    # Get the minimum valid model number
    result = find_model_mumber_extremum(c_mapping, c, minimum=True)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
