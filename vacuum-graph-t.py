from scripts import data_ops as do
import matplotlib.pyplot as plt
import argparse as arg


def cut_values(x_values, y_values, start, interval, end=None):
    index = x_values.index(start)
    count = len(x_values)
    if index > 0:
        del x_values[0:index-1]
        del y_values[0:index-1]

    if end is not None:
        end_index = x_values.index(end)
        del x_values[end_index:count-1]
        del y_values[end_index:count-1]

    new_list = [(x, y) for x, y in zip(x_values, y_values) if x % interval == 0]
    new_list = list(zip(*new_list))

    return new_list


parser = arg.ArgumentParser(description="Show a graph and table for \
                            input data.")
parser.add_argument("file", help="The file to read")
parser.add_argument("-t" "--time", help="Time format [seconds/minutes/hours]",
                    metavar="FORMAT", default="seconds", dest="time_format",
                    choices=["seconds", "minutes", "hours"])
parser.add_argument("-s", "--start", help="start time for values",
                    metavar="TIME", default=1, type=int)
parser.add_argument("-i", "--interval", help="Interval for time",
                    metavar="VALUE", default=1, type=int)
parser.add_argument("-e", "--end", help="Interval for time",
                    metavar="VALUE")
parser.add_argument("-g", "--grid", help="Whether to display a grid",
                    action="store_true")

args = parser.parse_args()
arg_dict = vars(args)
data_file = arg_dict["file"]

x_values, y_values = do.file_to_points(data_file, arg_dict["time_format"])
x_values = x_values[0]
y_values = y_values[0]

fig, ax = plt.subplots(2, 1)

ax[0].plot(x_values, y_values)
ax[0].set(yscale="log")

# hide axes
fig.patch.set_visible(False)
ax[1].axis('off')
ax[1].axis('tight')

start = arg_dict["start"]
end = arg_dict["end"]
interval = arg_dict["interval"]
x_and_y = cut_values(x_values, y_values, start, interval, end)

new_list = list(zip(*x_and_y))

print("drawing plot...")
ax[1].table(cellText=new_list, loc="center")

fig.tight_layout()

plt.show()
