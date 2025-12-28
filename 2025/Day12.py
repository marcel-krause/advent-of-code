import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_shapes_and_areas(data_lines):
    shapes = []
    areas = []

    current_shape = []
    for line in data_lines:
        if 'x' in line:
            area_part, present_part = line.split(': ')
            height, width = list(map(lambda x: int(x), area_part.split('x')))
            present_list = list(map(lambda x: int(x), present_part.split()))

            areas.append({
                'height': height,
                'width': width,
                'area': height*width,
                'present_list': present_list
            })
        elif line == '':
            shapes.append(current_shape)
            current_shape = []
        elif ':' in line:
            continue
        else:
            current_shape.append(line)

    return shapes, areas
            
def get_shape_areas(shapes):
    shape_areas = []

    for shape in shapes:
        count = 0

        for row in shape:
            count += row.count('#')
        
        shape_areas.append(count)
    
    return shape_areas

def get_minimum_area_for_present_list(shape_areas, present_list):
    minimum_area = 0

    for i in range(len(present_list)):
        minimum_area += present_list[i] * shape_areas[i]

    return minimum_area

# Solution to part 1
def part_1():
    shapes, areas = get_shapes_and_areas(data_lines)
    shape_areas = get_shape_areas(shapes)

    trivially_fits = []
    trivially_too_large = []
    residuals = []

    for area in areas:
        current_area = area['area']
        minimum_area = get_minimum_area_for_present_list(shape_areas, area['present_list'])

        if minimum_area > current_area:
            trivially_too_large.append(area)
        else:
            if current_area - minimum_area > 333:
                trivially_fits.append(area)
            else:
                residuals.append(area)

    return len(trivially_fits)

# Solution to part 2
def part_2():
    result = 'Merry Christmas!'

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
