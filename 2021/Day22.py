import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def create_instructions(data_lines, part=1):
    instructions = []

    for line in data_lines:
        turn_state = int("on" in line)

        x, y, z = line.replace("on ", "").replace("off ", "").split(",")

        if part == 1:
            x = list(map(lambda x: int(x), x.replace("x=", "").split("..")))
            y = list(map(lambda x: int(x), y.replace("y=", "").split("..")))
            z = list(map(lambda x: int(x), z.replace("z=", "").split("..")))
            instructions.append((x, y, z, turn_state))
        else:
            x = tuple(map(lambda x: int(x), x.replace("x=", "").split("..")))
            y = tuple(map(lambda x: int(x), y.replace("y=", "").split("..")))
            z = tuple(map(lambda x: int(x), z.replace("z=", "").split("..")))
            instructions.append(((x, y, z), turn_state))
    
    return instructions

def get_intersect_of_two_cubes(cube_1: tuple[tuple[int]], cube_2: tuple[tuple[int]]) -> tuple:
    # Find the minimum "right-most" x borders and the maximum "left-most" x borders (note: the ternary operator is actually faster compared to min() and max())
    x_min = cube_1[0][1] if cube_1[0][1] < cube_2[0][1] else cube_2[0][1]
    x_max = cube_1[0][0] if cube_1[0][0] > cube_2[0][0] else cube_2[0][0]

    # Find the minimum "right-most" y borders and the maximum "left-most" y borders
    y_min = cube_1[1][1] if cube_1[1][1] < cube_2[1][1] else cube_2[1][1]
    y_max = cube_1[1][0] if cube_1[1][0] > cube_2[1][0] else cube_2[1][0]

    # Find the minimum "right-most" z borders and the maximum "left-most" z borders
    z_min = cube_1[2][1] if cube_1[2][1] < cube_2[2][1] else cube_2[2][1]
    z_max = cube_1[2][0] if cube_1[2][0] > cube_2[2][0] else cube_2[2][0]

    # In case no overlap is found, return false
    if x_min < x_max or y_min < y_max or z_min < z_max:
        return ()
    
    # Return the cube representing the overlap
    return ( (x_max, x_min), (y_max, y_min), (z_max, z_min) )

def get_cube_volume(cube: tuple[tuple[int]]) -> int:
    return (cube[0][1] - cube[0][0] + 1)*(cube[1][1] - cube[1][0] + 1)*(cube[2][1] - cube[2][0] + 1)


# Solution to part 1
def part_1():
    result = 0

    instructions = create_instructions(data_lines, part=1)

    grid = {}
    for instruction in instructions:
        # Get the current cube and its on/off state
        x_range = range(instruction[0][0], instruction[0][1]+1)
        y_range = range(instruction[1][0], instruction[1][1]+1)
        z_range = range(instruction[2][0], instruction[2][1]+1)
        state = instruction[3]

        # Only consider the initialization region
        if max(x_range) < -50 or min(x_range) > 50 or max(y_range) < -50 or min(y_range) > 50 or max(z_range) < -50 or min(z_range) > 50:
            continue

        # Switch the lights on or off
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    key = str(x) + "," + str(y) + "," + str(z)
                    grid[key] = state

    # Count all lights that are turned on
    lights_turned_on = 0
    for i in grid.values():
        lights_turned_on += int(i)

    result = lights_turned_on

    return result

# Solution to part 2
def part_2():
    result = 0
    
    instructions = create_instructions(data_lines, part=2)

    # Initialize a list of all signed volumes and a dictionary previously considered cubes, including newly created intersects
    signed_volumes = []
    cubes = {}

    # Iterate over all instructions
    for curr_instruction in instructions:

        # For each instruction, iterate over previous cubes (including intersects)
        add_cubes = cubes.copy()
        for cube in cubes.items():
            # Check for intersects of the current new cube and the current previously considered cube/intersect
            intersect = get_intersect_of_two_cubes(cube[0], curr_instruction[0])
            
            # If no intersect is found, continue with the next previously considered cube
            if len(intersect) == 0:
                continue
            
            # Add the intersect to the dict of previously considered cubes and add the volume with the correct sign
            if cube[1] != 0:
                signed_volumes.append(-1*cube[1]*get_cube_volume(intersect))
            if intersect in add_cubes:
                add_cubes[intersect] += -1*cube[1]
            else:
                add_cubes[intersect] = -1*cube[1]

        # In case the current new cube is of type "on", add it to the dict of previously considered cubes or update the value if it is already present
        if curr_instruction[1] == 1:
            if curr_instruction[1] != 0:
                signed_volumes.append(curr_instruction[1]*get_cube_volume(curr_instruction[0]))
            if curr_instruction[0] in add_cubes:
                add_cubes[curr_instruction[0]] += 1*curr_instruction[1]
            else:
                add_cubes[curr_instruction[0]] = 1*curr_instruction[1]

        # Update the dict with all previously considered cubes
        cubes = add_cubes.copy()

    result = sum(signed_volumes)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
