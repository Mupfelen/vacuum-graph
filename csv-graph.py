import matplotlib.pyplot as plt
import argparse as arg
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
    points_list = []
    for _ in range(1, len(in_list[0].split('\t'))):
        points_list.append([])

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
    new_list = []
    divisor = 1
    if format == "minutes":
        divisor = 60
    elif format == "hours":
        divisor = 3600

    for point in point_list:
        point = ((point[0] - first_time).total_seconds() / divisor, point[1])
        new_list.append(point)

    return new_list


def file_to_points(file, time_format):
    # open given file
    print(f"opening file {data_file}...")
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


# add CL arguments
parser = arg.ArgumentParser(description="Show a graph for input data.")
parser.add_argument("file", help="The file to read")
parser.add_argument("-g", "--grid", help="Whether to display a grid",
                    action="store_true")
parser.add_argument("-t", "--time", metavar="TIME",
                    help="The time format. [seconds, minutes, hours]",
                    dest="time_format", default="seconds",
                    choices=["seconds", "minutes", "hours"])
parser.add_argument("-p", "--plot", metavar="CHOICE", default="all",
                    help="Which graph to plot. [all] or int (0-first)",
                    dest="plot_choice")
parser.add_argument("-x", "--xsize", default="10", type=int,
                    help="Width of the window, default 10", dest="xsize",
                    metavar="XSIZE")
parser.add_argument("-y", "--ysize", default="7", type=int,
                    help="Height of the window, default 7", dest="ysize",
                    metavar="YSIZE")
parser.add_argument("-r", "--reference", type=str, help="File for \
                    reference graph", dest="ref_file", metavar="FILE")

# parse CL arguments
args = parser.parse_args()
arg_dict = vars(args)
data_file = arg_dict["file"]

# get pyplot compatible lists from file
x_values, y_values = file_to_points(data_file, arg_dict["time_format"])

# apply plot settings and draw plot
print("Drawing plot...")
xsize = arg_dict["xsize"]
ysize = arg_dict["ysize"]
plt.figure(figsize=(xsize, ysize), num="Pressure Plot")

# select which graphs to plot
which_plot = arg_dict["plot_choice"]
if which_plot == "all":
    for i, _ in enumerate(x_values):
        plt.plot(x_values[i], y_values[i])
else:
    plt.plot(x_values[int(which_plot)], y_values[int(which_plot)])

# if ref file is set, get ref lists from file
ref_file = arg_dict["ref_file"]
if ref_file is not None:
    x_values_r, y_values_r = file_to_points(ref_file, arg_dict["time_format"])

plt.plot(x_values_r[0], y_values_r[0], color="green")

# make grid
grid_choice = arg_dict["grid"]
if (grid_choice is True):
    plt.grid(which='both', color='grey', linestyle='-', linewidth=0.3)

# set labels and scales
plt.xlabel(f'time in {arg_dict["time_format"]}')
plt.ylabel('pressure in mbar')
plt.yscale('log')

# show plot
plt.show()
