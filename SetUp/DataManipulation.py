from typing import List

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
    dataframe["angleInRadian"] = np.where((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                  / (2 * dataframe["b"] * dataframe["c"]) < -0.99999999, np.pi,
                                  np.arccos((dataframe["b"] ** 2 + dataframe["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                            / (2 * dataframe["b"] * dataframe["c"])))
    return dataframe


def angleInRadianFromObjectToPoints(x_object, y_object, x_point1, y_point1, x_point2, y_point2):
    b = ((x_object - x_point1) ** 2 + (y_object - y_point1) ** 2) ** 0.5
    c = ((x_object - x_point2) ** 2 + (y_object - y_point2) ** 2) ** 0.5
    a = ((x_point1 - x_point2) ** 2 + (y_point1 - y_point2) ** 2) ** 0.5
    angle_in_rad = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

    return angle_in_rad


# calculate distance and write it to the df
# return the adjusted df
def distancePlayerToGoal(dataframe):
    # distance
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    dataframe["distance_to_goal_centre"] = ((dataframe["x_coordinate"] - CONSTANTS.X_COORDINATE_GOALCENTRE) ** 2 +
                                            (dataframe["y_coordinate"] - CONSTANTS.Y_COORDINATE_GOALCENTRE) ** 2) ** 0.5
    return dataframe


# calculate distance
# return the distance in yards
def distanceObjectToPoint(x_object, y_object, x_point, y_point):
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    distance = ((x_object - x_point) ** 2 + (y_object - y_point) ** 2) ** 0.5
    return distance


def addGoalBinary(dataframe):
    dataframe['goal'] = np.where(dataframe['shot_outcome'] == 'Goal', 1, 0)
    return dataframe

def score(df):
    # first extract all match id of dataframe in a unique list
    match_id = df[["match_id"]].drop_duplicates()
    match_id = match_id.values.tolist()
    dfUpdated = pd.DataFrame()
    # the scores are seen from the home team perspective

    for match in match_id:
        # set up for every match
        dfCurrentMatch = df[df['match_id'] == match[0]].sort_values(by = ['minute'])
        # reset index to go through in the for loop
        dfCurrentMatch.reset_index(inplace=True)
        index = 0
        scores: List[int] = [0] * len(dfCurrentMatch)
        score_home_team: List[int] = [0] * len(dfCurrentMatch)
        score_away_team: List[int] = [0] * len(dfCurrentMatch)
        previous_score = 0
        previous_home_team_score = 0
        previous_away_team_score = 0
        for shot in range(len(dfCurrentMatch)):
            home_team = dfCurrentMatch['home_team'][shot]
            away_team = dfCurrentMatch['away_team'][shot]
            shooting_team = dfCurrentMatch['team'][shot]

            if dfCurrentMatch['goal'][shot] == 1:
                # home team scored
                if shooting_team == home_team:
                    previous_score += 1
                    previous_home_team_score += 1

                    scores[index] = previous_score
                    score_home_team[index] = previous_home_team_score
                    score_away_team[index] = previous_away_team_score
                # away team score
                else:
                    previous_score -= 1
                    previous_away_team_score += 1

                    scores[index] = previous_score
                    score_home_team[index] = previous_home_team_score
                    score_away_team[index] = previous_away_team_score
            # no goal happened
            else:

                scores[index] = previous_score
                score_home_team[index] = previous_home_team_score
                score_away_team[index] = previous_away_team_score
            index += 1
        dfCurrentMatch['score'] = scores
        dfCurrentMatch['home_score'] = score_home_team
        dfCurrentMatch['away_score'] = score_away_team
        dfUpdated = pd.concat([dfUpdated, dfCurrentMatch])
    dfUpdated.reset_index(drop=True, inplace=True)
    return dfUpdated
