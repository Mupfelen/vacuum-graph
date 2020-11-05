import matplotlib.pyplot as plt

first_strings = [51, 52, 53, 54, 55, 56]
second_strings = [1, 2, 3, 4, 5, 6]

string_2d = [first_strings, second_strings]

pre_list = [99, 98, 97, 96, 95, 94]

new = [(x) for x in zip(pre_list, *string_2d) if x[0] % 3 == 0]
print(new)

plt.show()
