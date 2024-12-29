import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def calculate_next_secret_number(secret_number, SALT):
    secret_number = ( secret_number^(secret_number*64) ) % SALT
    secret_number = ( secret_number^(secret_number//32) ) % SALT
    secret_number = ( secret_number^(secret_number*2048) ) % SALT
    return secret_number

def get_current_price(secret_number):
    return secret_number % 10


# Solution to part 1
def part_1():
    result = 0
    SALT = 16777216

    for initial_number in data_lines:
        secret_number = int(initial_number)
        for _ in range(2000):
            secret_number = calculate_next_secret_number(secret_number, SALT)
        result += secret_number

    return result

# Solution to part 2
def part_2():
    result = 0
    SALT = 16777216
    sequence_to_maximum_prize = defaultdict(int)

    for initial_number in data_lines:
        secret_number = int(initial_number)
        previous_price = get_current_price(secret_number)
        price_differences = []
        price_sequences = {}

        for i in range(1, 2001):
            secret_number = calculate_next_secret_number(secret_number, SALT)
            current_price = get_current_price(secret_number)
            price_differences.append(current_price - previous_price)
            previous_price = current_price

            price_sequence = ''
            if i >= 4:
                price_sequence = ','.join(map(str, price_differences[i-4:i]))
                if price_sequence not in price_sequences:
                    price_sequences[price_sequence] = current_price

        for sequence, price in price_sequences.items():
            sequence_to_maximum_prize[sequence] += price

    result = max(sequence_to_maximum_prize.values())

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
