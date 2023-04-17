from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
from Model import model_info
from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams

df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
df = df.loc[(df['y_ball'] > 0)]
df.reset_index(drop=True, inplace=True)

Z = df.pivot_table(index='x_ball', columns='y_ball', values='xP_best_alternative').T.values
Z = np.nan_to_num(Z, nan=-1)

X_unique = np.sort(df.x_ball.unique())
Y_unique = np.sort(df.y_ball.unique())
X, Y = np.meshgrid(X_unique, Y_unique)

# Initialize plot objects
rcParams['figure.figsize'] = 8, 11  # sets plot size
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()
img = plt.imread("penalty_box.png")
ax.imshow(img, interpolation='nearest', alpha=0.8, extent=[95, 120, 16.5, 64])

cpf = ax.contourf(X, Y, Z, levels=[0, 0.6, 0.7, 0.8, 0.9, 1],
                  colors=['#006F01', '#49be25', '#96be25', '#fb5f04', '#FF2300'], alpha=0.7, antialiased=True)

ax.invert_yaxis()
ax.set_xlabel('x coordinate')
_ = ax.set_ylabel('y coordinate')
plt.title("where the pass with what probability is going", fontdict={'fontsize': 20})
plt.colorbar(cpf, aspect=50)
fig.tight_layout()
plt.show()

#todo change color code