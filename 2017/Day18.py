import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict
from collections import deque

def is_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def run_program(program_state) -> dict:
    i, registers, receive_queue = program_state['index'], program_state['registers'], program_state['receive_queue']
    send_queue = []

    while True:
        instructions = data_lines[i].split()

        second_operand = 0
        if len(instructions) == 3:
            second_operand = registers[instructions[2]] if not is_int(instructions[2]) else int(instructions[2])

        if instructions[0] == 'snd':
            send_queue.append(registers[instructions[1]] if not is_int(instructions[1]) else int(instructions[1]))
        elif instructions[0] == 'set':
            registers[instructions[1]] = second_operand
        elif instructions[0] == 'add':
            registers[instructions[1]] += second_operand
        elif instructions[0] == 'mul':
            registers[instructions[1]] *= second_operand
        elif instructions[0] == 'mod':
            registers[instructions[1]] %= second_operand
        elif instructions[0] == 'rcv':
            if len(receive_queue) == 0:
                return {
                    'registers': registers,
                    'index': i,
                    'send_queue': send_queue,
                    'receive_queue': receive_queue,
                }
            else:
                registers[instructions[1]] = receive_queue.popleft()
        elif instructions[0] == 'jgz':
            if (registers[instructions[1]] if not is_int(instructions[1]) else int(instructions[1])) > 0:
                i += second_operand - 1
        i += 1

        if i not in range(len(data_lines)):
            return {
                'registers': registers,
                'index': i,
                'send_queue': [],
                'receive_queue': deque([]),
            }

# Solution to part 1
def part_1():
    program_states = {
        0: {
            'registers': defaultdict(int),
            'index': 0,
            'send_queue': [],
            'receive_queue': deque([]),
        }
    }

    program_states[0] = run_program(program_states[0])

    return program_states[0]['send_queue'][-1]

# Solution to part 2
def part_2():
    result = 0

    program_states = {
        0: {
            'registers': defaultdict(int),
            'index': 0,
            'send_queue': [],
            'receive_queue': deque([]),
        },
        1: {
            'registers': defaultdict(int),
            'index': 0,
            'send_queue': [],
            'receive_queue': deque([]),
        }
    }
    program_states[1]['registers']['p'] = 1

    pp = 0
    while True:
        program_states[pp] = run_program(program_states[pp])

        if len(program_states[pp]['send_queue']) == 0 and len(program_states[(pp+1)%2]['send_queue']) == 0:
            break

        if pp == 1:
            result += len(program_states[pp]['send_queue'])

        program_states[(pp+1)%2]['receive_queue'].extend(program_states[pp]['send_queue'])
        program_states[pp]['send_queue'] = []

        pp = (pp+1)%2

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
