import pandas as pd
import numpy as np
from statsbombpy import sb


# Variable Definition
# x and y coordinates do not have to be transformed:
# https://www.bundesliga.com/en/faq/all-you-need-to-know-about-soccer/all-you-need-to-know-about-a-soccer-field-10572

goal_length = 7.32
x_coordinate_post1 = 120
y_coordinate_post1 = 36.34
x_coordinate_post2 = 120
y_coordinate_post2 = 43.66
x_coordinate_goalCentre = 120
y_coordinate_goalCentre = y_coordinate_post1 + goal_length / 2


# coordinates
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

def angle(dataframe):
    # Morales cesar a "A mathematics-based new penalty area in football: tackling diving", Journal of sports sciences
    # cosinussatz
    dataframe["a"] = ((dataframe["x_coordinate"] - x_coordinate_post1) ** 2 +
                      (dataframe["y_coordinate"] - y_coordinate_post1) ** 2) ** 0.5
    dataframe["b"] = ((dataframe["x_coordinate"] - x_coordinate_post2) ** 2 +
                      (dataframe["y_coordinate"] - y_coordinate_post2) ** 2) ** 0.5
    dataframe["angle"] = np.where((dataframe["a"] ** 2 + dataframe["b"] ** 2 - goal_length ** 2)
                                  / (2 * dataframe["a"] * dataframe["b"]) < -0.99999999, 180,
                                  np.rad2deg(np.arccos((dataframe["a"] ** 2 + dataframe["b"] ** 2 - goal_length ** 2)
                                                       / (2 * dataframe["a"] * dataframe["b"]))))
    return dataframe


# calculate distance and write it to the df
# return the adjusted df
def distance(dataframe):
    # distance
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    dataframe["distance_to_goal_centre"] = ((dataframe["x_coordinate"] - x_coordinate_goalCentre) ** 2 + (
            dataframe["y_coordinate"] - y_coordinate_goalCentre) ** 2) ** 0.5
    return dataframe
