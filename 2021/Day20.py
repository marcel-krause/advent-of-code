import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

def get_algorithm_and_raw_image(data_lines):
    enhancement_algorithm = data_lines[0]
    input_image_raw = data_lines[2:]

    input_image = []
    for line in input_image_raw:
        input_image.append(list(line))

    additional_chars = 3
    top_bottom = ["."]*(2*additional_chars + len(input_image))
    new_input_image = [top_bottom.copy() for _ in range(additional_chars)]
    for line in input_image:
        new_input_image.append(["."]*additional_chars + list(line) + ["."]*additional_chars)
    for _ in range(additional_chars):
        new_input_image.append(top_bottom)

    return enhancement_algorithm, new_input_image

def enhance(enhancement_algorithm, input_image, ITERATIONS):
    for step in range(ITERATIONS):
        # Initialize the new output image
        output_image = [ ["." for _ in range(len(input_image))] for _ in range(len(input_image)) ]

        # Scan through the current input image and perform the image enhancement
        for row in range(1, len(input_image)-1):
            for col in range(1, len(input_image[row])-1):

                # Get the neighbors of the current pixel (including the pixel itself)
                neighbor_points = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        neighbor_points.append( (row + i, col+j) )
                
                # Calculate the current pixel enhancement value by building a binary number from the pixel and its neighbors
                pixel_enhancement_value = ""
                for neighbor in neighbor_points:
                    pixel_enhancement_value += input_image[neighbor[0]][neighbor[1]]
                enhancement_index = int(pixel_enhancement_value.replace("#", "1").replace(".", "0"), 2)

                # Set the current pixel to its new value according to the enhancement algorithm
                output_pixel = enhancement_algorithm[enhancement_index]
                output_image[row][col] = output_pixel

        # Adjust for the infinite size of the grid by correcting the borders of the current image
        replacement_pixel = output_image[1][1]
        for row in range(len(output_image)):
            if row == 0 or row == len(output_image)-1:
                col_range = range(len(output_image[0]))
            else:
                col_range = [0, len(output_image[0])-1]

            for col in col_range:
                output_image[row][col] = replacement_pixel

        # Extend the image by one pixel on each side
        if step < ITERATIONS-1:
            top_bottom = [replacement_pixel]*(2 + len(output_image))
            input_image = [top_bottom.copy()].copy()
            for line in output_image:
                input_image.append([replacement_pixel] + line + [replacement_pixel])
            input_image.append(top_bottom)

    return output_image

def count_lit_pixels(output_image):
    lit_pixel_count = 0

    for row in output_image:
        for pixel in row:
            if pixel == "#":
                lit_pixel_count += 1
    
    return lit_pixel_count


# Solution to part 1
def part_1():
    result = 0

    ITERATIONS = 2

    enhancement_algorithm, input_image = get_algorithm_and_raw_image(data_lines)
    output_image = enhance(enhancement_algorithm, input_image, ITERATIONS)
    result = count_lit_pixels(output_image)

    return result

# Solution to part 2
def part_2():
    result = 0

    ITERATIONS = 50

    enhancement_algorithm, input_image = get_algorithm_and_raw_image(data_lines)
    output_image = enhance(enhancement_algorithm, input_image, ITERATIONS)
    result = count_lit_pixels(output_image)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
