# create a test model for 10 particular shot not for a whole dataframe
# here it can be shown hot the model works

import pandas as pd
from Model import model_info
from SetUp import DataManipulation, CONSTANTS
import numpy as np

square_meter_size = 1
max_shot_distance = 20
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
y_range_pitch = np.arange(18,
                          62 + square_meter_size,
                          square_meter_size)
xGList = []
xList = []
yList = []
for x in x_range_pitch:
    for y in y_range_pitch:

        if (x == 120) & (y == 36 | y == 44):
            xgPrediction = 0
            xList.append(x)
            yList.append(y)
            xGList.append(xgPrediction)
            continue
        logmodel = CONSTANTS.REGRESSION_MODEL
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
        xgPrediction = model_info.predictionOfSingleValues([angle_in_rad, distance_in_yards], CONSTANTS.ATTRIBUTES, logmodel)

        xList.append(x)
        yList.append(y)
        xGList.append(xgPrediction)
data = {'x': xList,
        'y': yList,
        'xGPrediction': xGList,
        }
dfXGGrid = pd.DataFrame(data)

def valid_imshow_data(data):
    data = np.asarray(data)
    if data.ndim == 2:
        return True
    elif data.ndim == 3:
        if 3 <= data.shape[2] <= 4:
            return True
        else:
            print('The "data" has 3 dimensions but the last dimension '
                  'must have a length of 3 (RGB) or 4 (RGBA), not "{}".'
                  ''.format(data.shape[2]))
            return False
    else:
        print('To visualize an image the data must be 2 dimensional or '
              '3 dimensional, not "{}".'
              ''.format(data.ndim))
        return False

# x_coords = np.arange(min(xList),max(xList)+1)
# y_coords = np.arange(min(yList),max(yList)+1)
Z = dfXGGrid['xGPrediction']


