import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

def button_combinations(n):
    buttons = range(n)
    
    for k in range(1, n + 1):
        for combo in combinations(buttons, k):
            yield combo

def get_machine_and_buttons(data_lines):
    machine_sets = []

    for line in data_lines:
        line_parts = line.split()
        target_state = [0 if digit == '.' else 1 for digit in list(line_parts[0].replace('[', '').replace(']', ''))]
        joltage = list(map(lambda x: int(x), line_parts[-1].replace('{', '').replace('}', '').split(',')))

        buttons = []
        for button_part in line_parts[1:-1]:
            buttons.append(list(map(lambda x: int(x), button_part.replace('(', '').replace(')', '').split(','))))

        machine_sets.append({
            'target_state': target_state,
            'buttons': buttons,
            'joltage': joltage
        })

    return machine_sets

def create_augmented_matrix(machine_set):
    num_cols = len(machine_set['buttons']) + 1
    num_rows = len(machine_set['joltage'])

    augmented_matrix = [[0]*num_cols for _ in range(num_rows)]

    for i in range(len(machine_set['buttons'])):
        for j in machine_set['buttons'][i]:
            augmented_matrix[j][i] = 1

    for j in range(len(machine_set['joltage'])):
        augmented_matrix[j][-1] = machine_set['joltage'][j]

    return augmented_matrix

def compute_rref_with_gauss_jordan(augmented_matrix):
    rref_matrix = [[Fraction(x) for x in row] for row in augmented_matrix]
    rows = len(rref_matrix)
    cols = len(rref_matrix[0])

    pivot_row = 0
    for c in range(cols):
        if pivot_row >= rows:
            break

        # Find pivot
        pivot = None
        for i in range(pivot_row, rows):
            if rref_matrix[i][c] != 0:
                pivot = i
                break

        if pivot is None:
            continue

        # Swap pivot row into place
        rref_matrix[pivot_row], rref_matrix[pivot] = rref_matrix[pivot], rref_matrix[pivot_row]

        # Normalize pivot row
        pivot_val = rref_matrix[pivot_row][c]
        rref_matrix[pivot_row] = [x / pivot_val for x in rref_matrix[pivot_row]]

        # Eliminate column
        for i in range(rows):
            if i != pivot_row and rref_matrix[i][c] != 0:
                factor = rref_matrix[i][c]
                rref_matrix[i] = [
                    rref_matrix[i][j] - factor * rref_matrix[pivot_row][j]
                    for j in range(cols)
                ]

        pivot_row += 1

    return rref_matrix

def build_solution_functions(rref_matrix):
    rows = len(rref_matrix)
    n_vars = len(rref_matrix[0]) - 1

    pivot_row_for_col = {}
    pivot_cols = set()

    # Identify pivots
    for i in range(rows):
        for j in range(n_vars):
            if rref_matrix[i][j] == 1 and all(rref_matrix[k][j] == 0 for k in range(rows) if k != i):
                pivot_row_for_col[j] = i
                pivot_cols.add(j)
                break

    free_variables = [j for j in range(n_vars) if j not in pivot_cols]

    # Build affine expressions of the form x[i] = const[i] + sum(coeff[i][k] * free[k])
    constants = [Fraction(0)] * n_vars
    coefficients = [{f: Fraction(0) for f in free_variables} for _ in range(n_vars)]

    for j in range(n_vars):
        if j in pivot_cols:
            row = pivot_row_for_col[j]
            constants[j] = rref_matrix[row][-1]
            for f in free_variables:
                coefficients[j][f] = -rref_matrix[row][f]
        else:
            coefficients[j][j] = Fraction(1)

    # Create the constraints
    constraints = []

    for i in range(len(constants)):
        constraint = {}
        constraint['b'] = -constants[i]

        for key, val in coefficients[i].items():
            constraint[key] = val

        constraints.append(constraint)

    return free_variables, constants, coefficients, constraints

def evaluate_solution(constants, coefficients, free_values):
    n_vars = len(constants)
    result = [0] * n_vars

    for i in range(n_vars):
        value = constants[i]

        for f_key, f_value in free_values.items():
            value += coefficients[i].get(f_key, 0) * f_value

        result[i] = value

    return result

def yield_free_variable_combinations(search_ranges):
    free_variables = list(search_ranges.keys())
    ranges = list(search_ranges.values())

    for values in product(*ranges):
        yield dict(zip(free_variables, values))

def create_objective_function(coefficients, constants):
    objective_function = defaultdict(int)

    for coefficient, constant in zip(coefficients, constants):
        objective_function['c'] += constant

        for key, value in coefficient.items():
            objective_function[key] += value

    return {key: value for key, value in objective_function.items() if value != 0}

def get_relevant_free_variables(objective_function):
    return [key for key in objective_function.keys() if key != 'c']

def find_solution_candidates(constraints, free_variables):
    candidates = []

    for combination in combinations(constraints, len(free_variables)):
        M = []
        for c in combination:
            M.append([c.get(v, Fraction(0)) for v in free_variables] + [c['b']])

        solved_system = compute_rref_with_gauss_jordan(M)
        solution_candidate = []

        for i in range(len(M)):
            if solved_system[i][i] == 0:
                solution_candidate = None
                break

            solution_candidate.append(solved_system[i][len(M)])

        if solution_candidate is None:
            continue

        candidates.append(dict(zip(free_variables, solution_candidate)))

    return candidates

def is_feasible_point(point, constraints):
    for c in constraints:
        lhs = sum(c.get(v, Fraction(0)) * point[v] for v in point)

        if lhs < c['b']:
            return False
        
    return True

def evaluate_objective(point, objective):
    value = objective['c']

    for key, coefficient in objective.items():
        if key != 'c':
            value += coefficient * point.get(key, Fraction(0))

    return value

def lp_minimize(objective, constraints, free_variables):
    minimum_value, minimum_point = -1, None

    for point in find_solution_candidates(constraints, free_variables):
        if not is_feasible_point(point, constraints):
            continue

        value = evaluate_objective(point, objective)

        if minimum_value == -1 or value < minimum_value:
            minimum_value, minimum_point = value, point

    return minimum_value, minimum_point

def get_search_ranges(objective_function, free_variables, minimum_point, CUSTOM_RANGE_WINDOW, DEFAULT_RANGE_SIZE):
    search_ranges = {}

    relevant_free_variables = get_relevant_free_variables(objective_function)

    for var in free_variables:
        if var not in relevant_free_variables:
            search_ranges[var] = list(range(DEFAULT_RANGE_SIZE))
        else:
            middle = minimum_point[var].__floor__()
            bounds = [middle - CUSTOM_RANGE_WINDOW, middle + CUSTOM_RANGE_WINDOW + 1]

            if bounds[0] < 0:
                bounds[0], bounds[1] = 0, bounds[1] + abs(bounds[0])
            
            search_ranges[var] = list(range(bounds[0], bounds[1]))
    
    return search_ranges

def find_minimum(objective_function, constants, coefficients, constraints, free_variables, CUSTOM_RANGE_WINDOW, DEFAULT_RANGE_SIZE):
    minimum = float('inf')

    if 'c' in objective_function and len(objective_function) == 1:
        minimum = objective_function['c']
    else:
        minimum_value, minimum_point = lp_minimize(objective_function, constraints, free_variables)
        integer_minimum_value = minimum_value.__ceil__()

        search_ranges = get_search_ranges(objective_function, free_variables, minimum_point, CUSTOM_RANGE_WINDOW, DEFAULT_RANGE_SIZE)
        
        for free_values in yield_free_variable_combinations(search_ranges):
            solution_candidate = evaluate_solution(constants, coefficients, free_values)

            if all(v >= 0 and v.denominator == 1 for v in solution_candidate):
                minimum = min(minimum, sum([int(v) for v in solution_candidate]))

                if minimum == integer_minimum_value:
                    break
    
    return minimum

# Solution to part 1
def part_1():
    machine_sets = get_machine_and_buttons(data_lines)

    minimum_button_counts = []

    for machine_set in machine_sets:
        buttons = machine_set['buttons']
        target_state = machine_set['target_state']
        target_state_string = ''.join(map(lambda x: str(x), target_state))

        for all_combinations in button_combinations(len(buttons)):
            state = [0]*len(target_state)

            for combination in all_combinations:
                pressed_button = buttons[combination]
                
                for idx in pressed_button:
                    state[idx] = (state[idx] + 1)%2
                
            if target_state_string == ''.join(map(lambda x: str(x), state)):
                minimum_button_counts.append(len(all_combinations))
                break

    return sum(minimum_button_counts)

# Solution to part 2
def part_2():
    result = 0

    DEFAULT_RANGE_SIZE = 200
    CUSTOM_RANGE_WINDOW = 5

    machine_sets = get_machine_and_buttons(data_lines)

    for machine_set in machine_sets:
        augmented_matrix = create_augmented_matrix(machine_set)
        rref_matrix = compute_rref_with_gauss_jordan(augmented_matrix)

        free_variables, constants, coefficients, constraints = build_solution_functions(rref_matrix)
        objective_function = create_objective_function(coefficients, constants)

        result += find_minimum(objective_function, constants, coefficients, constraints, free_variables, CUSTOM_RANGE_WINDOW, DEFAULT_RANGE_SIZE)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
