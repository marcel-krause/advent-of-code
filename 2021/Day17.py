import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from math import sqrt, ceil

# Solution to part 1
def part_1():
    result = 0

    area_ranges = data_lines[0].replace("target area: ", "").split(", ")
    y_ranges = area_ranges[1].replace("y=", "").split("..")
    result = -int(y_ranges[0]) * (-int(y_ranges[0]) - 1)//2

    return result

# Solution to part 2
def part_2():
    result = 0

    # Get the target areas
    area_ranges = data_lines[0].replace("target area: ", "").split(", ")
    x_ranges = area_ranges[0].replace("x=", "").split("..")
    y_ranges = area_ranges[1].replace("y=", "").split("..")
    x_range_target_area = set(range(int(x_ranges[0]), int(x_ranges[1]) + 1))
    y_range_target_area = set(range(int(y_ranges[0]), int(y_ranges[1]) + 1))
    max_x_in_target = max(x_range_target_area)
    min_y_in_target = min(y_range_target_area)

    # Find all valid trajectories
    largest_y_reached = -float("Inf")
    valid_configurations = set()
    x_range_min = ceil((sqrt(1 + 8*int(x_ranges[0])) - 1)/2)
    for x in range(x_range_min, int(x_ranges[1])+1):
        for y in range(int(y_ranges[0]), -int(y_ranges[0])):

            # Initialize the probe
            probe_position = [0, 0]
            probe_velocity = [x, y]
            max_y_position = -float("Inf")

            # Perform the steps
            for _ in range(1000):
                # Probe movement
                probe_position[0] += probe_velocity[0]
                probe_position[1] += probe_velocity[1]

                # Update the largest y value, if necessary
                if probe_position[1] > max_y_position:
                    max_y_position = probe_position[1]

                # Drag influence
                if probe_velocity[0] > 0:
                    probe_velocity[0] -= 1
                elif probe_velocity[0] < 0:
                    probe_velocity[0] += 1
                
                # Gravity influence
                probe_velocity[1] -= 1

                # Check if the probe has entered the target area
                if probe_position[0] in x_range_target_area and probe_position[1] in y_range_target_area:
                    valid_configurations.add((x, y))
                    if max_y_position > largest_y_reached:
                        largest_y_reached = max_y_position
                    break
                
                # Check if the probe overshoots
                if probe_position[0] > max_x_in_target or probe_position[1] < min_y_in_target:
                    break

    result = len(valid_configurations)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
