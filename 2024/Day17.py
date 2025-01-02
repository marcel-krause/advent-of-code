import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_initial_state_and_program(data_lines):
    registers = {}

    for line in data_lines:
        if "Register" in line:
            register, value = line.replace('Register ', '').split(': ')
            registers[register] = int(value)
        elif "Program" in line:
            programs = list(map(lambda x: int(x), line.replace('Program: ', '').split(',')))
    
    return registers, programs

def get_combo_operand(operand, registers):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    else:
        print("ERROR: combo operand 7 is reserved and does not appear in a valid program!")
        return None
    
def perform_operation(opcode, operand, registers, pointer):
    output = None

    if opcode == 0:     # adv instruction
        registers['A'] //= ( 2**get_combo_operand(operand, registers) )
    elif opcode == 1:   # bxl instruction
        registers['B'] ^= operand
    elif opcode == 2:
        registers['B'] = get_combo_operand(operand, registers) % 8
    elif opcode == 3:   # jnz instruction
        if registers['A'] != 0:
            return operand, output
    elif opcode == 4:   # bxc instruction
        registers['B'] ^= registers['C']
    elif opcode == 5:  # out instruction
        output = get_combo_operand(operand, registers) % 8
    elif opcode == 6:   # bdv instruction
        registers['B'] = registers['A'] // ( 2**get_combo_operand(operand, registers) )
    elif opcode == 7:   # cdv instruction
        registers['C'] = registers['A'] // ( 2**get_combo_operand(operand, registers) )

    return pointer+2, output

def run_programs(registers, programs):
    outputs = []

    pointer = 0
    while True:
        if pointer > len(programs) - 2:
            break

        opcode = programs[pointer]
        operand = programs[pointer+1]
        pointer, output = perform_operation(opcode, operand, registers, pointer)

        if output is not None:
            outputs.append(output)

    return ','.join(map(lambda x: str(x), outputs))


# Solution to part 1
def part_1():
    result = 0

    registers, programs = get_initial_state_and_program(data_lines)
    result = run_programs(registers, programs)

    return result

# Solution to part 2
def part_2():
    # An analysis of the program for my input shows that given the registers A and C, the output for each "round" is calculated as follows:
    # C = A // 2**( (A%8)^1 )
    # OUT = (A%8)^(C%8)^5
    # A = A//8
    # The program terminates once the pointer reaches the opcode 3 near the end of the program and A equals 0.
    # By considering the most significant 3-bit number of A first and matching it with the desired output, the valid values for register A
    # can be computed 3-bit by 3-bit. In the end, the lowest valid number is picked.
    result = 0

    _, programs = get_initial_state_and_program(data_lines)
    register_a_buildups = {''}

    for target_out in programs[::-1]:
        next_register_a_buildups = set()
        for register_a in register_a_buildups:
            for aa in range(8):
                a = int(register_a+str(aa), 8)
                c = a//(2**((a%8)^1))
                out = (a%8)^(c%8)^5

                if target_out == out:
                    next_register_a_buildups.add(register_a+str(aa))

        register_a_buildups = next_register_a_buildups.copy()
        
    result = min([int(x, 8) for x in register_a_buildups])

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
