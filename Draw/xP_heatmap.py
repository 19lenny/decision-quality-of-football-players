from SetUp import JSONtoDF, CONSTANTS
import pandas as pd
from Model import model_info
from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams
def xP_heatmap(correct_decision, title):
    df = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
    # some alternatives show are emtpy because no good alternative is in frame, these has to be taken out of the dataframe for visualization,
    # because no one played a pass in this situation
    df = df.loc[(df['y_ball'] > 0) | (df['x_ball'] > 0)]
    # only show the passes from the wrong decisions
    # if this is not activated, then every pass is shown
    if correct_decision == False:
        df = df.loc[(df['shot_decision_correct'] == False)]
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
    img = plt.imread("40_per_field.png")
    ax.imshow(img, interpolation='nearest', alpha=0.8, extent=[80, 120, 0, 80])

    cpf = ax.contourf(X, Y, Z, levels=[0, 0.6, 0.7, 0.8, 0.9, 1],
                      colors=['#006F01', '#49be25', '#96be25', '#fb5f04', '#FF2300'], alpha=0.7, antialiased=True)

    ax.invert_yaxis()
    ax.set_xlabel('x coordinate')
    _ = ax.set_ylabel('y coordinate')
    plt.title(title, fontdict={'fontsize': 20})
    plt.colorbar(cpf, aspect=50)
    fig.tight_layout()
    plt.show()

#todo change color code

xP_heatmap(correct_decision=False, title="xP heatmap wrong decisions")
xP_heatmap(correct_decision=True, title="xP heatmap all decisions")