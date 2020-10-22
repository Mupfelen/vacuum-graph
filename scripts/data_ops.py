import re
from datetime import datetime


# return list of lines from file
def read_file_txt(path):
    # open file and read all lines
    try:
        with open(path, "r") as file:
            try:
                lines = file.readlines()
            except OSError:
                print("error while reading file. exiting...")
                exit(1)
    except IOError:
        print("error while opening file. exiting...")
        exit(1)

    # remove header strings
    first_data = 0
    for index, line in enumerate(lines):
        if "[" in line:
            first_data = index + 1
            break
    del lines[0:first_data]

    return lines


# return list of lists by delimit string
def parse_data(in_list):
    # determine dataset size
    points_list = [[] for _ in range(1, len(in_list[0].split('\t')))]

    for line in in_list:
        # split by tabs
        lin = line.split('\t')

        # remove cs and create datetime object
        time_str = re.sub(r"\.[0-9]{2} ", ' ', lin.pop(0))
        time = datetime.strptime(time_str, '%Y-%m-%d %I:%M:%S %p')

        for i, row in enumerate(lin):
            points_list[i].append((time, float(row)))

    return points_list


def convert_time(point_list, format="seconds"):
    first_time = point_list[0][0]

    divisor = 1
    if format == "minutes":
        divisor = 60
    elif format == "hours":
        divisor = 3600

    new_list = [((point[0] - first_time).total_seconds() / divisor, point[1])
                for point in point_list]

    return new_list


def file_to_points(file, time_format):
    # open given file
    print(f"opening file {file}...")
    file_lines = read_file_txt(file)

    # parse data
    print(f"file opened successfully. reading data...")
    points_list = parse_data(file_lines)

    # convert time formats
    print("data processed successfully. converting...")
    converted_list = [[x for x in convert_time(points, time_format)
                       ] for points in points_list]

    # convert points into usable data for pyplot
    x_values = [[x[0] for x in points] for points in converted_list]
    y_values = [[y[1] for y in points] for points in converted_list]

    return x_values, y_values
