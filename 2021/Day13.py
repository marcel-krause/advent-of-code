import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def prepare_folding_instructions(data_lines):
    dot_coordinates = []
    folding_instructions = []
    max_row = 0
    max_col = 0
    for line in data_lines:
        if ',' in line:
            col, row = list(map(lambda x: int(x), line.split(',')))
            dot_coordinates.append([row, col])
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        if 'x=' in line:
            folding_instructions.append('x')
        if 'y=' in line:
            folding_instructions.append('y')

    # Fill the initial dot grid
    dot_grid = [ [0 for _ in range(max_col + 1)] for _ in range(max_row + 1) ]
    for row, col in dot_coordinates:
        dot_grid[row][col] += 1
    
    return folding_instructions, dot_grid

def fold(folding_instructions, dot_grid, first_only=True):
    for curr_folding_instruction in folding_instructions:
        if curr_folding_instruction == 'y':
            new_dot_grid = [ [0 for _ in range(len(dot_grid[0]))] for _ in range(len(dot_grid)//2) ]
            for row in range(len(dot_grid)//2):
                for col in range(len(dot_grid[0])):
                    new_dot_grid[row][col] = dot_grid[row][col]

            dot_grid_copy = dot_grid.copy()
            dot_grid_copy.reverse()

            for row in range(len(dot_grid_copy)//2):
                for col in range(len(dot_grid_copy[0])):
                    if dot_grid_copy[row][col] == 1:
                        new_dot_grid[row][col] = 1
        else:
            new_dot_grid = [ [0 for _ in range(len(dot_grid[0])//2)] for _ in range(len(dot_grid)) ]
            for row in range(len(dot_grid)):
                for col in range(len(dot_grid[0])//2):
                    new_dot_grid[row][col] = dot_grid[row][col]

            dot_grid_copy = []
            for i in range(len(dot_grid)):
                curr_row = dot_grid[i].copy()
                curr_row.reverse()
                dot_grid_copy.append(curr_row)

            for row in range(len(dot_grid_copy)):
                for col in range(len(dot_grid_copy[0])//2):
                    if dot_grid_copy[row][col] == 1:
                        new_dot_grid[row][col] = 1

        dot_grid = new_dot_grid.copy()

        if first_only:
            return dot_grid
    
    return dot_grid

def count_dots(dot_grid):
    dot_count = 0

    for row in dot_grid:
        for dot in row:
            dot_count += dot

    return dot_count

def print_dot_grid(dot_grid):
    for row in dot_grid:
        print_row = ''
        for dot in row:
            if dot == 1:
                print_row += '*'
            else:
                print_row += ' '
        print(print_row)


# Solution to part 1
def part_1():
    result = 0
    
    folding_instructions, dot_grid = prepare_folding_instructions(data_lines)
    dot_grid = fold(folding_instructions, dot_grid, first_only=True)
    result = count_dots(dot_grid)

    return result

# Solution to part 2
def part_2():
    result = 0
    
    folding_instructions, dot_grid = prepare_folding_instructions(data_lines)
    dot_grid = fold(folding_instructions, dot_grid, first_only=False)
    print_dot_grid(dot_grid)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
