import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    differences = []
    for line in data_lines:
        nums = [int(x) for x in line.split()]
        diff = max(nums) - min(nums)
        differences.append(diff)

    result = sum(differences)

    return result

# Solution to part 2
def part_2():
    divisions = []
    for line in data_lines:
        nums = [int(x) for x in line.split()]
        nums.sort(reverse=True)
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if nums[i] % nums[j] == 0:
                    divisions.append(nums[i] // nums[j])
                    break
            else:
                continue
            break

    result = sum(divisions)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
