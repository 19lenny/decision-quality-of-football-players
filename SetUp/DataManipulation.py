import pandas as pd
import numpy as np
from statsbombpy import sb
from SetUp import CONSTANTS

"""
DataManipulationAngleDistance: all methods receive a dataframe.
This dataframe is manipulated. 
Either the coordination are displayed in a more readable fashion or
the distance to the goal centre is calculated and added to the dataframe
or the angel a shooter has to the goal is calculated and added to the dataframe
"""

# this method calculates the coordinates of a given statsbomb dataframe
# the location is already given in the dataframe, but it is given as a list
# for easier calculation, the x and y coordinates should be saved as double values
# the dataframe is after manipulation returned
def coordinates(dataframe):
    x_coordinates = []
    y_coordinates = []
    for location in dataframe["location"]:
        x_coordinates.append(location[0])
        y_coordinates.append(location[1])

    dataframe["x_coordinate"] = x_coordinates
    dataframe["y_coordinate"] = y_coordinates

    return dataframe


# calculate angle and write it to the df
# return the adjusted df
# visualized in powerpoint 'calculation angle and distance.pptx'
# angle in degree
def angle(dataframe):
    # Morales cesar a "A mathematics-based new penalty area in football: tackling diving", Journal of sports sciences
    # cosinussatz
    dataframe["b"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_POST1) ** 2 +
                      (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_POST1) ** 2) ** 0.5
    dataframe["c"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_POST2) ** 2 +
                      (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_POST2) ** 2) ** 0.5
    dataframe["angle"] = np.where((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                  / (2 * dataframe["b"] * dataframe["c"]) < -0.99999999, 180,
                                  np.rad2deg(
                                      np.arccos((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                                / (2 * dataframe["b"] * dataframe["c"]))))
    return dataframe


# angle in radian
def angleInRadian(dataframe):
    dataframe["b"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_POST1) ** 2 +
                      (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_POST1) ** 2) ** 0.5
    dataframe["c"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_POST2) ** 2 +
                      (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_POST2) ** 2) ** 0.5
    dataframe["angle"] = np.where((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                  / (2 * dataframe["b"] * dataframe["c"]) < -0.99999999, np.pi,
                                  np.arccos((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                            / (2 * dataframe["b"] * dataframe["c"])))
    return dataframe


# calculate distance and write it to the df
# return the adjusted df
def distance(dataframe):
    # distance
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    dataframe["distance_to_goal_centre"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_GOALCENTRE) ** 2 +
                                            (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_GOALCENTRE) ** 2) ** 0.5
    return dataframe


def addGoalBinary(dataframe):
    dataframe['goal'] = np.where(dataframe['shot_outcome'] == 'Goal', 1, 0)
    return dataframe
