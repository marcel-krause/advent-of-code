import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def compute_completions(data_lines, part=1):
    # Matching brackets and error scores for each bracket
    MATCHING_PAIRS = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    COMPLETION_SCORES = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    ERROR_SCORES = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    # Get the total syntax error score
    all_completion_scores = []
    total_score = 0
    for line in data_lines:
        queue = []
        is_legal = True
        completion_score = 0

        for char in line:
            if char in MATCHING_PAIRS.keys():
                queue.append(char)
                continue
            
            last_element = queue[-1]
            if MATCHING_PAIRS[last_element] == char:
                queue.pop()
            else:
                total_score += ERROR_SCORES[char]
                is_legal = False
                break
        
        if is_legal and part==2:
            completion_queue = list(map(lambda x: MATCHING_PAIRS[x], queue))
            for item in reversed(completion_queue):
                completion_score *= 5
                completion_score += COMPLETION_SCORES[item]
            all_completion_scores.append(completion_score)
    
    if part==1:
        return total_score
    else:
        all_completion_scores.sort()
        return all_completion_scores[len(all_completion_scores)//2]


# Solution to part 1
def part_1():
    result = compute_completions(data_lines, part=1)

    return result

# Solution to part 2
def part_2():
    result = compute_completions(data_lines, part=2)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
