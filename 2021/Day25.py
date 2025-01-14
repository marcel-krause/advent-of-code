import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_initial_positions(data_lines, HEIGHT, WIDTH):
    east_herd_positions = set()
    south_herd_positions = set()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            curr_element = data_lines[row][col]
            if curr_element == ">":
                east_herd_positions.add((row, col))
            elif curr_element == "v":
                south_herd_positions.add((row, col))
    
    return east_herd_positions, south_herd_positions


# Solution to part 1
def part_1():
    result = 0

    HEIGHT = len(data_lines)
    WIDTH = len(data_lines[0])
    east_herd_positions, south_herd_positions = get_initial_positions(data_lines, HEIGHT, WIDTH)

    # Perform the steps
    step = 0
    while True:
        step += 1
        positions_changed = False
        
        # Move the sea cucumbers in the east-facing herd
        east_to_remove = set()
        east_to_add = set()
        for east_cucumber_position in east_herd_positions:
            # Get the next position, accounting for the boundary of the grid
            if east_cucumber_position[1] < WIDTH-1:
                next_position = (east_cucumber_position[0], east_cucumber_position[1]+1)
            else:
                next_position = (east_cucumber_position[0], 0)

            # The sea cucumber only moves if the next position is not occupied
            if next_position not in east_herd_positions and next_position not in south_herd_positions:
                positions_changed = True
                east_to_add.add(next_position)
                east_to_remove.add(east_cucumber_position)

        # Update the positions of the cucumbers in the east-facing herd
        east_herd_positions = east_herd_positions.union(east_to_add) - east_to_remove
        
        # Move the sea cucumbers in the south-facing herd
        south_to_remove = set()
        south_to_add = set()
        for south_cucumber_position in south_herd_positions:
            # Get the next position, accounting for the boundary of the grid
            if south_cucumber_position[0] < HEIGHT-1:
                next_position = (south_cucumber_position[0]+1, south_cucumber_position[1])
            else:
                next_position = (0, south_cucumber_position[1])

            # The sea cucumber only moves if the next position is not occupied
            if next_position not in east_herd_positions and next_position not in south_herd_positions:
                positions_changed = True
                south_to_add.add(next_position)
                south_to_remove.add(south_cucumber_position)

        # Update the positions of the cucumbers in the south-facing herd
        south_herd_positions = south_herd_positions.union(south_to_add) - south_to_remove

        # Check if the sea cucumbers stopped moving
        if not positions_changed:
            break

    result = step

    return result

# Solution to part 2
def part_2():
    result = 'Merry Christmas!'

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
