import matplotlib.pyplot as plt
import argparse as arg
import re
from datetime import datetime
from scripts import data_ops as do


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
parser.add_argument("-s", "--table", help="Whether to display a table",
                    action="store_true")

# parse CL arguments
args = parser.parse_args()
arg_dict = vars(args)
data_file = arg_dict["file"]

# get pyplot compatible lists from file
x_values, y_values = do.file_to_points(data_file, arg_dict["time_format"])

# apply plot settings and draw plot
print("drawing plot...")
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
    x_values_r, y_values_r = do.file_to_points(ref_file, arg_dict["time_format"])

    print("drawing reference plot...")
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
