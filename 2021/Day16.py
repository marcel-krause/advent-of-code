import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from functools import reduce

def parse_string(s: str) -> dict:
    # Get the packet version and type ID
    packet_version = int("".join(s[:3]), 2)
    s[:] = s[3:]
    type_id = int("".join(s[:3]), 2)
    s[:] = s[3:]

    # Handle the different type IDs
    if type_id == 4:
        # Handle literal strings
        literal_value = ""
        while True:
            literal_value += "".join(s[1:5])
            value_char = s[0]
            s[:] = s[5:]
            if value_char == "0":
                break
        literal_value_dec = int(literal_value, 2)
        
        return {"version": packet_version, "type_id": type_id, "value": literal_value_dec}
    else:
        # Handle operator strings
        length_type_id = s.pop(0)
        
        if length_type_id == "0":
            # Handle length type 0 strings (the length represents the amount of bits which contain the sub-packets)
            length = int("".join(s[:15]), 2)
            s[:] = s[15:]
            sub_s = s[:length]
            s[:] = s[length:]

            # Iterate over the substring until the length is exhausted
            sub_packet_data = list()
            while len(sub_s) > 0:
                sub_packet_data.append(parse_string(sub_s))

            output = {"version": packet_version, "type_id": type_id, "length_type_id": length_type_id, "length": length, "sub_packets": sub_packet_data}
        else:
            # Handle length type 1 strings (the length represents the amount of sub-packets to follow)
            num_sub_packets = int("".join(s[:11]), 2)
            s[:] = s[11:]

            # Iterate over the number of sub-packets
            sub_packet_data = list()
            for _ in range(num_sub_packets):
                parse_result = parse_string(s)
                sub_packet_data.append(parse_result)

            output = {"version": packet_version, "type_id": type_id, "length_type_id": length_type_id, "num_sub_packets": num_sub_packets, "sub_packets": sub_packet_data}

        return output

def get_version_sum(sub_list: list) -> int:
    sub_sum = 0
    for sub_list_element in sub_list:
        sub_sum += sub_list_element["version"]
        if "sub_packets" in sub_list_element:
            sub_sum += get_version_sum(sub_list_element["sub_packets"])
    return sub_sum

def get_packet_value(sub_list: list) -> list[int]:
    sub_sum = []
    for sub_list_element in sub_list:
        if sub_list_element["type_id"] == 4:
            sub_sum_element = sub_list_element["value"]
        elif sub_list_element["type_id"] == 0:
            sub_sum_element = sum(get_packet_value(sub_list_element["sub_packets"]))
        elif sub_list_element["type_id"] == 1:
            sub_sum_element = reduce(lambda x, y: x * y, get_packet_value(sub_list_element["sub_packets"]), 1)
        elif sub_list_element["type_id"] == 2:
            sub_sum_element = min(get_packet_value(sub_list_element["sub_packets"]))
        elif sub_list_element["type_id"] == 3:
            sub_sum_element = max(get_packet_value(sub_list_element["sub_packets"]))
        elif sub_list_element["type_id"] == 5:
            sub_sum_res = get_packet_value(sub_list_element["sub_packets"])
            sub_sum_element = int(sub_sum_res[0] > sub_sum_res[1])
        elif sub_list_element["type_id"] == 6:
            sub_sum_res = get_packet_value(sub_list_element["sub_packets"])
            sub_sum_element = int(sub_sum_res[0] < sub_sum_res[1])
        elif sub_list_element["type_id"] == 7:
            sub_sum_res = get_packet_value(sub_list_element["sub_packets"])
            sub_sum_element = int(sub_sum_res[0] == sub_sum_res[1])

        sub_sum.append(sub_sum_element)

    return sub_sum

def convert_hex_to_binary(hex_string):
    hex_string = hex_string
    binary_string = ""

    for c in hex_string:
        binary_string += bin(int(c, 16))[2:].zfill(4)

    return binary_string

def decode_packet(binary_string):
    s = list(binary_string)
    return [parse_string(s)]


# Solution to part 1
def part_1():
    result = 0

    binary_string = convert_hex_to_binary(data_lines[0])
    decoded_packet = decode_packet(binary_string)
    result = get_version_sum(decoded_packet)

    return result

# Solution to part 2
def part_2():
    result = 0

    binary_string = convert_hex_to_binary(data_lines[0])
    decoded_packet = decode_packet(binary_string)
    result = get_packet_value(decoded_packet)[0]

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
