import pandas as pd
import numpy as np
from statsbombpy import sb

"""
DataManipulationAngleDistance: all methods receive a dataframe.
This dataframe is manipulated. 
Either the coordination are displayed in a more readable fashion or
the distance to the goal centre is calculated and added to the dataframe
or the angel a shooter has to the goal is calculated and added to the dataframe
"""


# Variable Definition
# x and y coordinates do not have to be transformed:
# https://www.bundesliga.com/en/faq/all-you-need-to-know-about-soccer/all-you-need-to-know-about-a-soccer-field-10572

# these are the official coordinates of statsbomb.
# they official disclosures can be found in statsbomb Open Data specification v1.pdf
# https://github.com/statsbomb/statsbombpy/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf
goal_length = 7.32
x_coordinate_post1 = 120
y_coordinate_post1 = 36.34
x_coordinate_post2 = 120
y_coordinate_post2 = 43.66
x_coordinate_goalCentre = 120
y_coordinate_goalCentre = y_coordinate_post1 + goal_length / 2


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
def angle(dataframe):
    # Morales cesar a "A mathematics-based new penalty area in football: tackling diving", Journal of sports sciences
    # cosinussatz
    dataframe["b"] = ((dataframe["x_coordinate"] - x_coordinate_post1) ** 2 +
                      (dataframe["y_coordinate"] - y_coordinate_post1) ** 2) ** 0.5
    dataframe["c"] = ((dataframe["x_coordinate"] - x_coordinate_post2) ** 2 +
                      (dataframe["y_coordinate"] - y_coordinate_post2) ** 2) ** 0.5
    dataframe["angle"] = np.where((dataframe["b"] ** 2 + dataframe["c"] ** 2 - goal_length ** 2)
                                  / (2 * dataframe["b"] * dataframe["c"]) < -0.99999999, 180,
                                  np.rad2deg(np.arccos((dataframe["b"] ** 2 + dataframe["c"] ** 2 - goal_length ** 2)
                                                       / (2 * dataframe["b"] * dataframe["c"]))))
    return dataframe


# calculate distance and write it to the df
# return the adjusted df
def distance(dataframe):
    # distance
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    dataframe["distance_to_goal_centre"] = ((dataframe["x_coordinate"] - x_coordinate_goalCentre) ** 2 + (
            dataframe["y_coordinate"] - y_coordinate_goalCentre) ** 2) ** 0.5
    return dataframe
