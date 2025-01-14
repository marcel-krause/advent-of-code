import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_energy_levels(data_lines):
    energy_levels = [list(map(lambda x: int(x), line.rstrip('\n'))) for line in data_lines]
    bounded_energy_levels = [[float("-Inf")]*(len(energy_levels[0])+2)]

    for row in energy_levels:
        bounded_energy_levels.append([float("-Inf")] + row + [float("-Inf")])
    bounded_energy_levels.append([float("-Inf")]*(len(energy_levels[0])+2))

    return bounded_energy_levels

def perform_steps(energy_levels, part=1):
    step = 1
    total_flashes = 0

    while True:
        # Increase the energy count of the current octopus and get the locations of all initially flashing octopuses
        flashing_octopuses = []
        for row in range(len(energy_levels)):
            for col in range(len(energy_levels[0])):
                energy_levels[row][col] += 1
                if energy_levels[row][col] == 10:
                    total_flashes += 1
                    flashing_octopuses.append([row, col])

        # Flash the octopuses and increase the energy levels of the neighbors
        for row, col in flashing_octopuses:
            for neighbor_row in range(row-1, row+2):
                for neighbor_col in range(col-1, col+2):
                    if neighbor_row == row and neighbor_col == col:
                        continue
                    energy_levels[neighbor_row][neighbor_col] += 1
                    if energy_levels[neighbor_row][neighbor_col] == 10 and [neighbor_row, neighbor_col] not in flashing_octopuses:
                        total_flashes += 1
                        flashing_octopuses.append([neighbor_row, neighbor_col])

        # Check if all octopuses flashed at the same time
        if part == 2 and all(all(j > 9 or j == float("-inf") for j in i) for i in energy_levels):
            return step

        # Reset all octopuses that flashed
        for row in range(len(energy_levels)):
            for col in range(len(energy_levels[0])):
                if energy_levels[row][col] > 9:
                    energy_levels[row][col] = 0

        step += 1

        if part == 1 and step > 100:
            return total_flashes

# Solution to part 1
def part_1():
    result = 0

    energy_levels = get_energy_levels(data_lines)
    result = perform_steps(energy_levels, part=1)

    return result

# Solution to part 2
def part_2():
    result = 0

    energy_levels = get_energy_levels(data_lines)
    result = perform_steps(energy_levels, part=2)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
