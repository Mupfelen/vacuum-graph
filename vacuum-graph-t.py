from scripts import data_ops as do
import matplotlib.pyplot as plt
import argparse as arg


def cut_values(x_values, y_values, start, interval, end=None):
    index = x_values.index(start)
    if index > 0:
        del x_values[0:index-1]
        del y_values[0:index-1]

    if end is not None:
        end_index = x_values.index(end)
        del x_values[end_index:-1]
        del y_values[end_index:-1]

    new_list = [(x, y) for x, y in zip(x_values, y_values) if (x - start) % interval == 0]
    new_list = list(zip(*new_list))

    return new_list


def find_start(y_values, trigger=0):
    last = -1
    for i, val in enumerate(y_values):
        if last != -1:
            if (val + trigger) < last or val > (last + trigger):
                print(str(val) + ' ' + str(last))
                return i
        last = val

    return -1


parser = arg.ArgumentParser(description="Show a graph and table for \
                            input data.")
parser.add_argument("file", help="The file to read")
parser.add_argument("-t" "--time", help="Time format [seconds/minutes/hours]",
                    metavar="FORMAT", default="seconds", dest="time_format",
                    choices=["seconds", "minutes", "hours"])
parser.add_argument("-s", "--start", help="start time for values",
                    metavar="TIME", default=0, type=int)
parser.add_argument("-i", "--interval", help="Interval for time",
                    metavar="VALUE", default=1, type=int)
parser.add_argument("-e", "--end", help="Interval for time",
                    metavar="VALUE")
parser.add_argument("-g", "--grid", help="Whether to display a grid",
                    action="store_true")
parser.add_argument("-r", "--reference", type=str, help="File for \
                    reference graph", dest="ref_file", metavar="FILE")

args = parser.parse_args()
arg_dict = vars(args)
data_file = arg_dict["file"]

x_values, y_values = do.file_to_points(data_file, arg_dict["time_format"])
x_values = x_values[0]

fig, ax = plt.subplots(2, 1, figsize=(12, 7), num="Pressure Plot / Table")
# plt.subplots_adjust(bottom=0, hspace=0)

ax[0].plot(x_values, y_values[0])
ax[0].set(yscale="log")

ref_file = arg_dict["ref_file"]
if ref_file is not None:
    x_values_r, y_values_r = do.file_to_points(ref_file, arg_dict["time_format"])

    print("drawing reference plot...")
    ax[0].plot(x_values_r[0], y_values_r[0], color="green")

# hide axes
fig.patch.set_visible(False)
ax[1].axis('off')
ax[1].axis('tight')

start = arg_dict["start"]
end = arg_dict["end"]
interval = arg_dict["interval"]

x_and_y = cut_values(x_values, y_values, start, interval, end)

new_list = list(zip(*x_and_y))
new_list.insert(0, [f"t in {arg_dict['time_format']}", "p in mbar"])

# make grid
grid_choice = arg_dict["grid"]
if (grid_choice is True):
    ax[0].grid(which='both', color='grey', linestyle='-', linewidth=0.3)

print("drawing plot...")
ax[1].table(cellText=new_list, loc="center")

fig.tight_layout()

plt.show()
