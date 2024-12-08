import sys
import os

def get_day_from_filename():
    filename = os.path.basename(sys.argv[0])
    day_number = ''.join(filter(str.isdigit, filename))
    return day_number

def load_data():
    curr_day = get_day_from_filename()

    # Get command line arguments
    part = 1
    input_type = 'sample'
    if len(sys.argv) > 2:
        relevant_arguments = sys.argv[1:]

        if '1' in relevant_arguments:
            part = 1
        elif '2' in relevant_arguments:
            part = 2

        if 's' in relevant_arguments:
            input_type = 'sample'
        elif 'r' in relevant_arguments:
            input_type = 'real'

    # Initialize data storage
    data = {
        "sample": dict(),
        "real": dict()
    }

    # Read the sample input file
    with open(f'Day{curr_day}_sample.dat', 'r') as content_file:
        data["sample"]["raw"] = content_file.read()
        data["sample"]["lines"] = data["sample"]["raw"].splitlines()
        try:
            data["sample"]["lines_int"] = list(map(lambda x: int(x), data["sample"]["lines"]))
        except:
            data["sample"]["lines_int"] = []

    # Read the real input file
    with open(f'Day{curr_day}_input.dat', 'r') as content_file:
        data["real"]["raw"] = content_file.read()
        data["real"]["lines"] = data["real"]["raw"].splitlines()
        try:
            data["real"]["lines_int"] = list(map(lambda x: int(x), data["real"]["lines"]))
        except:
            data["real"]["lines_int"] = []

    return part, input_type, data[input_type]["raw"], data[input_type]["lines"], data[input_type]["lines_int"]
