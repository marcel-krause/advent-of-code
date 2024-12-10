import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

class bingo_board():
    def __init__(self, board_config):
        self.board_config = board_config
        self.played_numbers = [ [0 for _ in range(len(board_config[0]))] for _ in range(len(board_config[0]))]
    
    def print_board(self):
        for line in self.board_config:
            print(line)

    def print_played_numbers(self):
        for line in self.played_numbers:
            print(line)

    def check_number(self, num):
        for i in range(len(self.board_config)):
            for j in range(len(self.board_config[0])):
                if self.board_config[i][j] == num:
                    self.played_numbers[i][j] = 1
    
    def check_for_bingo(self):
        target_count = len(self.board_config[0])
        col_count = [0 for _ in range(target_count)]
        for i in range(len(self.played_numbers)):
            row_count = 0
            for j in range(len(self.played_numbers[0])):
                row_count += self.played_numbers[i][j]
                col_count[j] += self.played_numbers[i][j]
                if col_count[j] == target_count:
                    return True
            if row_count == target_count:
                return True
        
        return False
    
    def get_score(self):
        total_score = 0
        for i in range(len(self.played_numbers)):
            for j in range(len(self.played_numbers[0])):
                if self.played_numbers[i][j] == 0:
                    total_score += self.board_config[i][j]
        return total_score

def get_drawn_numbers_and_bingo_boards():
    drawn_numbers = list(map(lambda x: int(x), data_lines[0].split(',')))

    board_config = []
    all_boards = []
    for line in data_lines[2:]:
        if line == '':
            all_boards.append(bingo_board(board_config))
            board_config = []
            continue
        
        board_config.append(list(map(lambda x: int(x), line.split())))
    all_boards.append(bingo_board(board_config))

    return drawn_numbers, all_boards


# Solution to part 1
def part_1():
    drawn_numbers, all_boards = get_drawn_numbers_and_bingo_boards()

    game_over = False
    for drawn_number in drawn_numbers:
        for board in all_boards:
            board.check_number(drawn_number)
            if board.check_for_bingo():
                result = board.get_score() * drawn_number
                game_over = True
                break
        if game_over:
            break

    return result

# Solution to part 2
def part_2():
    drawn_numbers, all_boards = get_drawn_numbers_and_bingo_boards()

    for drawn_number in drawn_numbers:
        if len(all_boards) == 1:
            all_boards[0].check_number(drawn_number)
            if all_boards[0].check_for_bingo():
                result = all_boards[0].get_score() * drawn_number
                break
        else:
            new_boards = []
            for board in all_boards:
                board.check_number(drawn_number)
                if not board.check_for_bingo():
                    new_boards.append(board)
                    continue
            all_boards = new_boards

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
