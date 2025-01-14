import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import re
from math import ceil

def add_snailfish_numbers(num1: str, num2: str) -> str:
    return "[{},{}]".format(num1, num2)

def find_explode_candidate(s: str) -> tuple[str, list]:
    bracket_count = 0
    i = 0
    while i < len(s):
        if s[i] == "[":
            bracket_count += 1
        elif s[i] == "]":
            bracket_count -= 1
        
        if bracket_count > 4:
            expl_cand = ""
            expl_cand_range = [i]
            while True:
                expl_cand += s[i]
                if s[i] == "]":
                    expl_cand_range.append(i)
                    return expl_cand, expl_cand_range
                i += 1
        i += 1
    return "", []

def find_split_candidate(s: str) -> tuple[str, list]:
    match = re.search(r"\d{2,}", s)
    if match is not None:
        return match.group(0), [match.start(), match.end()-1]
    return "", []

def explode_snailfish_number(s: str, expl_cand: str, expl_cand_range: list) -> str:
    left_s = s[:expl_cand_range[0]]
    right_s = s[expl_cand_range[1]+1:]

    candidate_numbers = list(map(lambda x: int(x), expl_cand.replace("[", "").replace("]", "").split(",")))
    left_candidate_number = candidate_numbers[0]
    right_candidate_number = candidate_numbers[1]

    # Find the next number to the left, if any
    left_match = list(re.finditer(r"\d+", left_s))
    if len(left_match) > 0:
        new_left_number = str(int(left_match[-1].group(0)) + left_candidate_number)
        left_s = left_s[:left_match[-1].start()] + new_left_number + left_s[left_match[-1].end():]

    # Find the next number to the right, if any
    right_match = re.search(r"\d+", right_s)
    if right_match is not None:
        new_right_number = str(int(right_match.group(0)) + right_candidate_number)
        right_s = right_s[:right_match.start()] + new_right_number + right_s[right_match.end():]

    return "{}0{}".format(left_s, right_s)

def split_snailfish_number(s: str, split_cand: str, split_cand_range: list) -> str:
    left_s = s[:split_cand_range[0]]
    right_s = s[split_cand_range[1]+1:]

    new_number = str([int(split_cand)//2,ceil(int(split_cand)/2)]).replace(" ", "")

    return left_s + new_number + right_s

def calculate_snailfish_magnitude(s: str) -> int:
    reduced_s = s

    while True:
        match = re.search(r"\[\d+\,\d+\]", reduced_s)
        if match is None:
            return int(reduced_s)

        match_numbers = list(map(lambda x: int(x), match.group(0).replace("[", "").replace("]", "").split(",")))
        left_candidate_number = match_numbers[0]
        right_candidate_number = match_numbers[1]
        new_number = str(3*left_candidate_number + 2*right_candidate_number)
        left_s = reduced_s[:match.start()]
        right_s = reduced_s[match.end():]
        reduced_s = left_s + new_number + right_s

def reduce_snailfish_numbers(curr_sum):
    old_sum = None

    # Reduce the snailfish numbers until they cannot be further reduced
    while curr_sum != old_sum:
        old_sum = curr_sum

        # Handle explodes
        expl_cand, expl_cand_range = find_explode_candidate(curr_sum)
        if expl_cand != "":
            curr_sum = explode_snailfish_number(curr_sum, expl_cand, expl_cand_range)
            continue
        
        # Handle splits
        split_cand, split_cand_range = find_split_candidate(curr_sum)
        if split_cand != "":
            curr_sum = split_snailfish_number(curr_sum, split_cand, split_cand_range)
    
    return curr_sum


# Solution to part 1
def part_1():
    result = 0

    # Perform all snailfish number summations from the input file
    curr_sum = data_lines[0]
    for i in range(len(data_lines)-1):
        # Add the snailfish numbers
        left_summand = curr_sum
        right_summand = data_lines[i+1]
        curr_sum = reduce_snailfish_numbers(add_snailfish_numbers(left_summand, right_summand))

    # Get the magnitude of the final sum
    result = calculate_snailfish_magnitude(curr_sum)

    return result

# Solution to part 2
def part_2():
    result = 0

    # Perform the snailfish number summations of all possible pairs from input file
    max_magnitude = 0
    for i in range(len(data_lines)):
        for j in range(len(data_lines)):
            if i == j:
                continue

            # Add the snailfish numbers
            left_summand = data_lines[i]
            right_summand = data_lines[j]
            curr_sum = reduce_snailfish_numbers(add_snailfish_numbers(left_summand, right_summand))

            # Check for the maximum sum
            magnitude_of_sum = calculate_snailfish_magnitude(curr_sum)
            if magnitude_of_sum > max_magnitude:
                max_magnitude = magnitude_of_sum
    
    result = max_magnitude

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
