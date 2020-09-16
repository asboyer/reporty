import matplotlib.pyplot as plt
import mpld3
dev_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
dev_y = [38496, 42000, 46752, 49320, 53200,
     56000, 62316, 64928, 67317, 68748, 73752]
fig = plt.plot(dev_x, dev_y)

print(mpld3.fig_to_html(fig))

