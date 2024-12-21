import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

class EquationSystem:
    coefficients_A = None
    coefficients_B = None
    targets = None

    def determinant(self):
        return self.coefficients_A[0]*self.coefficients_B[1] - self.coefficients_A[1]*self.coefficients_B[0]
    
    def inverse(self):
        determinant = self.determinant()
        if determinant == 0:
            return None
        inverse_matrix = [
            [self.coefficients_B[1]/determinant, -self.coefficients_B[0]/determinant],
            [-self.coefficients_A[1]/determinant, self.coefficients_A[0]/determinant]
        ]
        return inverse_matrix
    
    def solution(self):
        inverse_matrix = self.inverse()
        if inverse_matrix is None:
            return None
        solutions = [
            inverse_matrix[0][0] * self.targets[0] + inverse_matrix[0][1] * self.targets[1],
            inverse_matrix[1][0] * self.targets[0] + inverse_matrix[1][1] * self.targets[1]
        ]
        return solutions
    
    def get_integer_solution(self):
        epsilon = 0.01
        solutions = self.solution()
        if solutions is None:
            return [0, 0]
        int_a, int_b = list(map(lambda x: round(x), solutions))
        return [int_a, int_b] if abs(int_a - solutions[0]) < epsilon and  abs(int_b - solutions[1]) < epsilon else [0,0]
    
    def cost(self):
        integer_solution = self.get_integer_solution()
        return 3*integer_solution[0] + integer_solution[1]

def get_equation_system(data_lines, CORRECTION_FACTOR):
    equation_systems = []

    next_system = EquationSystem()
    for line in data_lines:
        if 'Button A' in line:
            next_system.coefficients_A = list(map(lambda x: int(x.replace('X+','').replace('Y+','')), line.replace('Button A: ', '').split(', ')))
        elif 'Button B' in line:
            next_system.coefficients_B = list(map(lambda x: int(x.replace('X+','').replace('Y+','')), line.replace('Button B: ', '').split(', ')))
        elif 'Prize' in line:
            next_system.targets = list(map(lambda x: int(x.replace('X=','').replace('Y=','')) + CORRECTION_FACTOR, line.replace('Prize: ', '').split(', ')))
        else:
            equation_systems.append(next_system)
            next_system = EquationSystem()
    equation_systems.append(next_system)
    
    return equation_systems


# Solution to part 1
def part_1():
    result = 0

    CORRECTION_FACTOR = 0

    equation_systems = get_equation_system(data_lines, CORRECTION_FACTOR)

    for equation_system in equation_systems:
        result += equation_system.cost()

    return result

# Solution to part 2
def part_2():
    result = 0

    CORRECTION_FACTOR = 10000000000000

    equation_systems = get_equation_system(data_lines, CORRECTION_FACTOR)

    for equation_system in equation_systems:
        result += equation_system.cost()

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
