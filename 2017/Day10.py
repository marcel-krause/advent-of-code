import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from functools import reduce
from operator import ixor

def hash_round(string, lengths, idx, skip):
    for length in lengths:
        if idx+length > len(string):
            sublist = (string[idx:len(string)] + string[0:idx+length-len(string)])[::-1]
            string = sublist[len(string)-idx:] + string[idx+length-len(string):idx] + sublist[:len(string)-idx]
        else:
            string = string[0:idx] + (string[idx:idx+length])[::-1] + string[idx+length:len(string)]
        
        idx = (idx + length + skip)%len(string)
        skip += 1
    
    return string, idx, skip

def sparse_hash(lengths, ROUNDS=1):
    string = list(range(256))
    idx = 0
    skip = 0

    for _ in range(ROUNDS):
        string, idx, skip = hash_round(string, lengths, idx, skip)

    return string

def dense_hash(sparse):
    dense_hash = [reduce(ixor, sparse[x:x+16]) for x in range(0,256,16)]
    return dense_hash

def hex_hash(dense):
    return ''.join(list(map(lambda x: format(x,f'0{2}x'), dense)))

def knot_hash(lengths, ROUNDS=1):
    sparse = sparse_hash(lengths, ROUNDS)
    dense = dense_hash(sparse)
    hex = hex_hash(dense)
    return hex


# Solution to part 1
def part_1():
    lengths = list(map(lambda x: int(x), data_lines[0].split(',')))

    string = sparse_hash(lengths)

    return string[0]*string[1]

# Solution to part 2
def part_2():
    lengths = [ord(c) for c in data_lines[0]] + [17,31,73,47,23]

    return knot_hash(lengths, ROUNDS=64)

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
