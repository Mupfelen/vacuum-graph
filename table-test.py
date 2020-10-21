import matplotlib.pyplot as plt

first_strings = ["a", "b", "c", "d", "e", "f"]
second_strings = ["1", "2", "3", "4", "5", "6"]

string_2d = [first_strings, second_strings]

l = []
l[0] = 5
l[5] = 2

print(l)

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(string_2d, loc="center")

fig.tight_layout()

plt.show()
