import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_red_tile_positions(data_lines):
    red_tile_positions = []

    for line in data_lines:
        red_tile_positions.append(tuple(map(lambda x: int(x), line.split(','))))

    return red_tile_positions

def check_orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def is_point_between_segment(a, b, point):
    return min(a[0], b[0]) <= point[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= point[1] <= max(a[1], b[1])

def is_point_on_boundary(a, b, point):
    return check_orientation(a, b, point) == 0 and is_point_between_segment(a, b, point)

def is_point_in_polygon_or_on_edge(point, polygon):
    point_is_inside = False

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]

        if is_point_on_boundary(a, b, point):
            return True

        if a[1] == b[1]:
            continue

        if a[1] > b[1]:
            a, b = b, a

        if a[1] <= point[1] < b[1] and check_orientation(a, b, point) > 0:
            point_is_inside = not point_is_inside

    return point_is_inside

def is_segment_intersection(line_segment1, line_segment2):
    a, b = line_segment1
    c, d = line_segment2

    o1 = check_orientation(a, b, c)
    o2 = check_orientation(a, b, d)
    o3 = check_orientation(c, d, a)
    o4 = check_orientation(c, d, b)

    return (o1 > 0 and o2 < 0 or o1 < 0 and o2 > 0) and (o3 > 0 and o4 < 0 or o3 < 0 and o4 > 0)

def is_rectangle_inside_polygon(polygon, polygon_edges, rectangle_points):
    rectangle_corners = [
        (rectangle_points[0][0], rectangle_points[0][1]),
        (rectangle_points[1][0], rectangle_points[0][1]),
        (rectangle_points[1][0], rectangle_points[1][1]),
        (rectangle_points[0][0], rectangle_points[1][1]),
    ]

    for rectangle_corner in rectangle_corners:
        if not is_point_in_polygon_or_on_edge(rectangle_corner, polygon):
            return False

    rectangle_edges = list(zip(rectangle_corners, rectangle_corners[1:] + rectangle_corners[:1]))

    for rectangle_edge in rectangle_edges:
        r_xmin = min(rectangle_edge[0][0], rectangle_edge[1][0])
        r_xmax = max(rectangle_edge[0][0], rectangle_edge[1][0])
        r_ymin = min(rectangle_edge[0][1], rectangle_edge[1][1])
        r_ymax = max(rectangle_edge[0][1], rectangle_edge[1][1])

        for polygon_edge in polygon_edges:
            p_xmin = min(polygon_edge[0][0], polygon_edge[1][0])
            p_xmax = max(polygon_edge[0][0], polygon_edge[1][0])
            p_ymin = min(polygon_edge[0][1], polygon_edge[1][1])
            p_ymax = max(polygon_edge[0][1], polygon_edge[1][1])

            if r_xmax < p_xmin or r_xmin > p_xmax or r_ymax < p_ymin or r_ymin > p_ymax:
                continue

            if is_segment_intersection(rectangle_edge, polygon_edge):
                return False

    return True

def find_largest_possible_area(polygon, polygon_edges, areas_for_rectangle_pairs):
    sorted_areas = list(areas_for_rectangle_pairs.keys())
    sorted_areas.sort(reverse=True)

    for largest_area in sorted_areas:
        for point1, point2 in areas_for_rectangle_pairs[largest_area]:
            if is_rectangle_inside_polygon(polygon, polygon_edges, (point1, point2)):
                return largest_area

# Solution to part 1
def part_1():
    red_tile_positions = get_red_tile_positions(data_lines)

    largest_area = 0
    for i in range(len(red_tile_positions)-1):
        for j in range(i, len(red_tile_positions)):
            point1, point2 = red_tile_positions[i], red_tile_positions[j]
            current_area = (abs(point1[0] - point2[0]) + 1)*(abs(point1[1] - point2[1]) + 1)
            largest_area = max(current_area, largest_area)

    return largest_area

# Solution to part 2
def part_2():
    red_tile_positions = get_red_tile_positions(data_lines)
    polygon_edges = list(zip(red_tile_positions, red_tile_positions[1:] + red_tile_positions[:1]))

    areas_for_rectangle_pairs = defaultdict(list)

    for i in range(len(red_tile_positions)-1):
        for j in range(i, len(red_tile_positions)):
            point1, point2 = red_tile_positions[i], red_tile_positions[j]
            current_area = (abs(point1[0] - point2[0]) + 1)*(abs(point1[1] - point2[1]) + 1)
            areas_for_rectangle_pairs[current_area].append((point1, point2))

    largest_area = find_largest_possible_area(red_tile_positions, polygon_edges, areas_for_rectangle_pairs)

    return largest_area

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
