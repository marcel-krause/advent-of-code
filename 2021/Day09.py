import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def find_local_minima(data_lines):
    # Get the height map from the input
    height_map = []
    for line in data_lines:
        row = [int(x) for x in line]
        height_map.append(row)

    # Put a border around the map
    bounded_height_map = [[9]*(len(height_map[0])+2)]
    for row in height_map:
        bounded_height_map.append([9] + row + [9])
    bounded_height_map.append([9]*(len(height_map[0])+2))

    # Find the local minima
    low_points = []
    low_point_coordinates = []
    for row_count in range(1, len(bounded_height_map) - 1):
        for col_count in range(1, len(bounded_height_map[0]) - 1):
            curr_point = bounded_height_map[row_count][col_count]

            neighbor_points = [
                bounded_height_map[row_count-1][col_count],
                bounded_height_map[row_count][col_count+1],
                bounded_height_map[row_count+1][col_count],
                bounded_height_map[row_count][col_count-1]
            ]

            if all(curr_point < i for i in neighbor_points):
                low_points.append(curr_point)
                low_point_coordinates.append([row_count, col_count])

    return low_points, low_point_coordinates, bounded_height_map


# Solution to part 1
def part_1():
    result = 0

    low_points, _, _ = find_local_minima(data_lines)

    # Calculate the risk level
    risk_levels = [x + 1 for x in low_points]
    result = sum(risk_levels)

    return result

# Solution to part 2
def part_2():
    result = 0
    
    _, low_point_coordinates, bounded_height_map = find_local_minima(data_lines)

    # Get the basin sizes
    basin_sizes = []
    for curr_low_point in low_point_coordinates:
        points_in_basin = [[curr_low_point[0], curr_low_point[1]]]

        for curr_point in points_in_basin:
            row, col = curr_point[0], curr_point[1]

            neighbor_points = [
                [row + 1, col],
                [row, col + 1],
                [row - 1, col],
                [row, col - 1]
            ]

            for neighbor_point in neighbor_points:
                if neighbor_point not in points_in_basin and bounded_height_map[neighbor_point[0]][neighbor_point[1]] != 9:
                    points_in_basin.append(neighbor_point)

        basin_sizes.append(len(points_in_basin))

    basin_sizes.sort()    

    product = 1
    for item in basin_sizes[-3:]:
        product *= item
    result = product

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
