# create a test model for 10 particular shot not for a whole dataframe
# here it can be shown hot the model works

from typing import List
import pandas as pd

from Draw import FCPython
from Model import model
from SetUp import JSONtoDF, DataManipulation, CONSTANTS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from DecisionEvaluation import evaluationHelper
from IPython.display import set_matplotlib_formats

import matplotlib.pyplot as plt
from matplotlib import rcParams
from DecisionEvaluation import offside

square_meter_size = 1
max_shot_distance = 25
# -----------------------------------------------------------------------------------------------------------
# create a grid which shows for every x and y combination the xGoal according to regression

x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                          CONSTANTS.X_COORDINATE_GOALCENTRE + square_meter_size,
                          square_meter_size)
# create the y linspace of the pitch, the end value gets +square meter size,
# such that the endpoint is still in the range
"""
y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE1,
                          CONSTANTS.Y_MIDDLE_LINE2 + square_meter_size,
                          square_meter_size)
"""
y_range_pitch = np.arange(15,
                          65+square_meter_size,
                          square_meter_size)

xGList = []
xList = []
yList = []
for x in x_range_pitch:
    for y in y_range_pitch:
        # left post
        if (x == 120) & (y == 36):
            xgPrediction = 0
            xList.append(x)
            yList.append(y)
            xGList.append(xgPrediction)
            continue
        # right post
        elif (x == 120) & (y == 44):
            xgPrediction = 0
            xList.append(x)
            yList.append(y)
            xGList.append(xgPrediction)
            continue
        logmodel = CONSTANTS.REGMODELINTERC
        x_location = x
        y_location = y

        angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_location, y_object=y_location,
                                                                        x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                        y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                        x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                        y_point2=CONSTANTS.Y_COORDINATE_POST2)
        distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                                   x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                                   y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
        # xG on the current location is the prediction of the expected goal from this location,
        # based on the angle of the location to the goal and the distance of the location to the goal
        # the prediction has to be multiplied with the xPass prediction
        # (the longer the teammate has time, the higher will be xP)
        xgPrediction = model.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, logmodel)

        xList.append(x)
        yList.append(y)
        xGList.append(xgPrediction)
data = {'x': xList,
        'y': yList,
        'xGPrediction': xGList,
        }
dfXGGrid = pd.DataFrame(data)

"""
What’s going on here? Looking at the Z data first, I’ve merely used the pivot_table method from pandas to cast my data 
into a matrix format, where the columns/rows correspond to the values of Z for each of the points in the range of the 
x-y-axes."""

Z = dfXGGrid.pivot_table(index='x', columns='y', values='xGPrediction').T.values

X_unique = np.sort(dfXGGrid.x.unique())
Y_unique = np.sort(dfXGGrid.y.unique())
X, Y = np.meshgrid(X_unique, Y_unique)
# Initialize plot objects
rcParams['figure.figsize'] = 8, 11  # sets plot size
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
img = plt.imread("half field.png")
ax.imshow(img, interpolation='nearest', alpha=0.8,extent=[95, 120, 15, 65])
levels = np.linspace(Z.min(), Z.max(), 14)


# Generate a color mapping of the levels we've specified
import matplotlib.cm as cm  # matplotlib's color map library

cpf = ax.contourf(X, Y, Z, len(levels), alpha=0.5, antialiased = True)

# Set all level lines to black
line_colors = ['white' for l in cpf.levels]

# Make plot and customize axes
cp = ax.contour(X, Y, Z, levels=levels, colors= line_colors)
ax.clabel(cp, fontsize=12)
ax.set_xlabel('x coordinate')
_ = ax.set_ylabel('y coordinate')
plt.title("xG Model", fontdict={'fontsize': 20})
plt.colorbar(cpf, aspect=50)
fig.tight_layout()
plt.show()
