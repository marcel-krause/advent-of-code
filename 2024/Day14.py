import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_quadrants(X_MAX, Y_MAX):
    quadrants = {}
    for x in range(X_MAX//2):
        for y in range(Y_MAX//2):
            quadrants[(x, y)] = 1

    for x in range(X_MAX//2+1, X_MAX):
        for y in range(Y_MAX//2):
            quadrants[(x, y)] = 0

    for x in range(X_MAX//2):
        for y in range(Y_MAX//2+1, Y_MAX):
            quadrants[(x, y)] = 2

    for x in range(X_MAX//2+1, X_MAX):
        for y in range(Y_MAX//2+1, Y_MAX):
            quadrants[(x, y)] = 3
    
    return quadrants

def initialize_robots(data_lines):
    robots = []
    robot_positions = set()

    for line in data_lines:
        p_part, v_part = line.replace('p=', '').replace('v=', '').split(' ')
        p = tuple(map(lambda x: int(x), p_part.split(',')))
        v = tuple(map(lambda x: int(x), v_part.split(',')))
        robots.append(Robot(p, v))
        robot_positions.add(p)

    return robots, robot_positions

def move_robots(robots, t, X_MAX, Y_MAX, QUADRANTS):
    quadrant_counts = defaultdict(int)
    robot_positions = set()

    for robot in robots:
        robot.update_position(t, X_MAX, Y_MAX)
        robot_positions.add(robot.p)
        quadrant_counts[robot.get_robot_quadrant(QUADRANTS)] += 1
        
    return quadrant_counts, robot_positions

def calculate_safety_factor(quadrant_counts):
    safety_factor = 1
    for i in range(4):
        safety_factor *= quadrant_counts[i]
    return safety_factor

def plot_map(robot_positions, t, X_MAX, Y_MAX):
    print(f"After {t} seconds:")
    for y in range(Y_MAX):
        line = ''
        for x in range(X_MAX):
            line += '#' if (x,y) in robot_positions else '.'
        print(line)
    print()

def check_map_for_tree(robot_positions, X_MAX, Y_MAX):
    for y in range(Y_MAX):
        counter = 0
        for x in range(X_MAX):
            counter = counter+1 if (x,y) in robot_positions else 0

            if counter > 10:
                return True
            
    return False

class Robot:
    def __init__(self, p, v):
        self.p = p
        self.v = v
    
    def update_position(self, t, X_MAX, Y_MAX):
        self.p = (
            (self.p[0] + self.v[0]*t)%X_MAX,
            (self.p[1] + self.v[1]*t)%Y_MAX
        )

    def get_robot_quadrant(self, QUADRANTS):
        return QUADRANTS[self.p] if self.p in QUADRANTS else -1


# Solution to part 1
def part_1():
    result = 0

    X_MAX = 11 if input_type == 'sample' else 101
    Y_MAX = 7 if input_type == 'sample' else 103
    T = 100
    QUADRANTS = get_quadrants(X_MAX, Y_MAX)

    robots, _ = initialize_robots(data_lines)
    quadrant_counts, _ = move_robots(robots, T, X_MAX, Y_MAX, QUADRANTS)
    result = calculate_safety_factor(quadrant_counts)

    return result

# Solution to part 2
def part_2():
    result = 0

    if input_type == 'sample':
        print("Part 2 does not work for the sample data. Try your actual input data instead.")
    else:
        X_MAX = 101
        Y_MAX = 103
        QUADRANTS = get_quadrants(X_MAX, Y_MAX)

        robots, robot_positions = initialize_robots(data_lines)

        t = 1
        while True:
            _, robot_positions = move_robots(robots, 1, X_MAX, Y_MAX, QUADRANTS)
            
            if check_map_for_tree(robot_positions, X_MAX, Y_MAX):
                plot_map(robot_positions, t, X_MAX, Y_MAX)
                result = t
                break

            t += 1

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
