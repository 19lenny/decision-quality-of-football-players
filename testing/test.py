import numpy as np
from matplotlib import pyplot as plt, colors
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
x = np.random.randn(100)
y = np.random.randn(100) + 5
fig, ax = plt.subplots()
hh = ax.hist2d(x, y, bins=40, norm=colors.LogNorm())
fig.colorbar(hh[3], ax=ax)
plt.show()