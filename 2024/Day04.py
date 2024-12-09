import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def append_empty_rows(word_matrix, line_length):
    for _ in range(3):
        word_matrix.append(['.']*(line_length + 6))

def create_extended_word_matrix(data_lines):
    word_matrix = []
    append_empty_rows(word_matrix, len(data_lines[0]))
    for line in data_lines:
        curr_row = ['.']*3 + list(line) + ['.']*3
        word_matrix.append(curr_row)
    append_empty_rows(word_matrix, len(data_lines[0]))
    return word_matrix

def check_for_xmas(word_matrix, x, y):
    target_word = 'XMAS'
    count = 0

    # Check vertically
    for sign in range(-1, 2, 2):
        for i in range(1, len(target_word)):
            if i == len(target_word)-1 and word_matrix[y + sign*i][x] == target_word[i]:
                count += 1
            elif word_matrix[y + sign*i][x] != target_word[i]:
                break

    # Check horizontally
    for sign in range(-1, 2, 2):
        for i in range(1, len(target_word)):
            if i == len(target_word)-1 and word_matrix[y][x + sign*i] == target_word[i]:
                count += 1
            elif word_matrix[y][x + sign*i] != target_word[i]:
                break

    # Check diagonally
    for sign_x in range(-1, 2, 2):
        for sign_y in range(-1, 2, 2):
            for i in range(1, len(target_word)):
                if i == len(target_word)-1 and word_matrix[y + sign_y*i][x + sign_x*i] == target_word[i]:
                    count += 1
                elif word_matrix[y + sign_y*i][x + sign_x*i] != target_word[i]:
                    break
    
    return count

def get_window(word_matrix, x, y):
    window = []
    for dy in range(y, y+3):
        window.append(word_matrix[dy][x:x+3])
    return window

def collapse_window(window):
    collapsed_window = ''
    for line in window:
        collapsed_window += ''.join(line)
    return collapsed_window[::2]

def check_for_xmas_cross(collapsed_window):
    valid_xmas_crossed = {"MSAMS", "MMASS", "SMASM", "SSAMM"}
    return collapsed_window in valid_xmas_crossed

# Solution to part 1
def part_1():
    result = 0
    
    word_matrix = create_extended_word_matrix(data_lines)

    for y in range(3, len(word_matrix)-3):
        for x in range(3, len(word_matrix[0])-3):
            if word_matrix[y][x] == 'X':
                result += check_for_xmas(word_matrix, x, y)

    return result

# Solution to part 2
def part_2():
    result = 0

    word_matrix = create_extended_word_matrix(data_lines)

    for y in range(3, len(word_matrix)-5):
        for x in range(3, len(word_matrix[0])-5):
            window = get_window(word_matrix, x, y)
            collapsed_window = collapse_window(window)
            if check_for_xmas_cross(collapsed_window):
                result += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
