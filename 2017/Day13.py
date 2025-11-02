import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_data(data_lines):
    return {int(k): int(v) for k,v in (s.split(': ') for s in data_lines)}

# Solution to part 1
def part_1():
    result = 0

    firewall = get_data(data_lines)
    for d, r in firewall.items():
        if d%(2*(r-1)) == 0:
            result += d*r

    return result

# Solution to part 2
def part_2():
    result = 0

    firewall = get_data(data_lines)

    delay = 0
    while True:
        firewall_results = []

        for d, r in firewall.items():
            firewall_results.append((d+delay)%(2*(r-1)))

        if all(x != 0 for x in firewall_results):
            break

        delay += 1

    return delay

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
