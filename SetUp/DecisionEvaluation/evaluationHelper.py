import math
import os
import json
import pandas as pd
from SetUp import CONSTANTS, DataManipulation
from scipy.stats import expon
from decimal import *
import numpy as np
from Model import model_info


# calculates the closest distance (in yards) of every player in a dataframe, for a given position
def findClosestPlayer(dataframe, x_location, y_location):
    x = None
    y = None
    # needs an init value, this value is overwritten with the first player incoming
    closestDistance = 1000
    position = None
    name = None

    for row in range(len(dataframe)):
        current_distance = DataManipulation.distanceObjectToPoint(dataframe["x_coordinate"][row],
                                                                  dataframe["y_coordinate"][row],
                                                                  x_location, y_location)
        # if the calculated current distance is closer than the closest distance from before,
        # than update the closest distance
        if current_distance < closestDistance:
            closestDistance = current_distance
            x = dataframe["x_coordinate"][row]
            y = dataframe["y_coordinate"][row]
            position = dataframe["name_position"][row]
            name = dataframe['name_player'][row]

    return x, y, closestDistance, position, name


# get all players that were in the frame during the current shot
# the dataframe contains a json like format
# this has to be transformed to a dataframe
# keyword is a word for the helper file. this avoids that multiple classes try to create the same helper file
def getPlayersOfEvent(shot, keyword):
    # transform players which are in the shot from a json like format to a dataframe format

    # the event comes in a json like format
    # transform it to a real json
    jsonOtherPlayers = json.dumps(shot)
    # save the json (name = sample.json), so we can import it to a dataframe
    filename = keyword + ".json"
    with open(filename, "w") as outfile:
        outfile.write(jsonOtherPlayers)

    # import it to a dataframe
    # this dataframe contains all data from all players that were in the frame during the shot
    dfOtherPlayers = pd.read_json(filename)
    dfOtherPlayers.reset_index(drop=True, inplace=True)

    # clean up
    # sample.json is no longer needed and can be deleted
    os.remove(filename)

    # the player_id, the player_name, the position_id and the position name have in the df still a dictionary like format
    # change this, such that id and name are additional columns in the dataframe

    # create empty lists, they symbolize the rows, which are filled in the next for loop
    idOtherPlayer = []
    nameOtherPlayer = []
    idPosition = []
    namePosition = []
    # go through every player that was in the shot...
    # if the dataframe of other players is empty, it generates a key error, this error has to be cathced
    try:
        for rowPlayers in range(len(dfOtherPlayers['player'])):
            x = dfOtherPlayers['player']
            # ...and add his personal id to a list
            idOtherPlayer.append(dfOtherPlayers['player'][rowPlayers]['id'])
            # ...and add his name to a list
            nameOtherPlayer.append(dfOtherPlayers['player'][rowPlayers]['name'])
            # ...and add his position id to a list
            idPosition.append(dfOtherPlayers['position'][rowPlayers]['id'])
            # ...and add the position name to a list
            namePosition.append(dfOtherPlayers['position'][rowPlayers]['name'])

        # the lists that were created before are now transformed back rows
        dfOtherPlayers['id_player'] = idOtherPlayer
        dfOtherPlayers['name_player'] = nameOtherPlayer
        dfOtherPlayers['id_position'] = idPosition
        dfOtherPlayers['name_position'] = namePosition

        # the x and x coordinates of each player have in the df still a list like format
        # change this, such that x and a are additional columns in the dataframe

        # for better readability are the x and y coordinates changed from a list setting to single rows setting in the df
        dfOtherPlayers = DataManipulation.coordinates(dfOtherPlayers)

        # remove the columns which have a dictionary / list like format
        dfOtherPlayers = dfOtherPlayers.drop(columns=["location", "player", "position"])
    except KeyError:
        print("Key Error")
    # dataframe of every player in the freeze-frame is prepared: return the df
    return dfOtherPlayers


def getTimeForDistance(distance, speed):
    seconds = distance / speed
    return seconds


def xGFromAlternative(time_teammate, time_opponent, time_ball, x_location, y_location):
    # cannot return none, but can return 0
    # 0 describes no chance of scoring
    xG = 0
    xP = 0
    ball_control_time = 0
    # cases where the defender clears the ball

    # if the opponent is there before the teammate is there, then the opponent will clear the ball
    if time_opponent < time_teammate:
        # no further calculation needed, return the none value and close method
        return xG, xP, ball_control_time
    # case opponent is slower than the teammate, but is there before the ball arrives,
    # therefore the opponent can clear the ball
    elif time_ball > time_opponent:
        # no further calculation needed, return the none value and close method
        return xG, xP, ball_control_time

    # cases where the offensive player can shoot the ball

    # case teammate is on the ball before the opponent
    # the opponent arrives after the ball arrived
    # but the teammate arrives before the ball arrives
    elif time_ball > time_teammate:
        # first step is to calculate the xPass

        # for this you have to know how long the team player has time to control the ball
        # the ball arrives after our teammate
        # this means the teammate does have to wait for the ball
        # the limitation factor for time is when the ball is arriving
        # the opponent is arriving after the ball
        # therefore time to control the ball = time_opponent - time_ball
        xP, ball_control_time = xPModel(time_opponent, time_ball)

        # since the xG is calculated the same for every case, it is calculated in the end
        # the only thing that changes is the xP value based on the time


    # case teammate is on the ball before the opponent
    # the opponent arrives after the ball arrived
    # the teammate arrives after the ball arrives
    elif time_ball <= time_teammate:
        # first step is to calculate the xPass

        # for this you have to know how long the team player has time to control the ball
        # the ball arrives before our teammate
        # this means the teammate doesn't have to wait for the ball and
        # has time until the opponent is arriving to control the ball
        # therefore time to control the ball = time_opponent - time_teammate
        xP, ball_control_time = xPModel(time_opponent, time_teammate)

        # since the xG is calculated the same for every case, it is calculated in the end
        # the only thing that changes is the xP value based on the time

    # calculate xG and return it

    # before we can calculate the xG, we have to know the angle, the penalty for bad angles and distance from the current location to the goal
    angle_in_rad = DataManipulation.angleInRadianFromObjectToPoints(x_object=x_location, y_object=y_location,
                                                                    x_point1=CONSTANTS.X_COORDINATE_POST1,
                                                                    y_point1=CONSTANTS.Y_COORDINATE_POST1,
                                                                    x_point2=CONSTANTS.X_COORDINATE_POST2,
                                                                    y_point2=CONSTANTS.Y_COORDINATE_POST2)
    distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                               x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                               y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
    penalty_log = DataManipulation.log_penalty_for_single_values(angle=angle_in_rad)
    # xG on the current location is the prediction of the expected goal from this location,
    # based on the angle of the location to the goal and the distance of the location to the goal
    # the prediction has to be multiplied with the xPass prediction
    # (the longer the teammate has time, the higher will be xP)
    xgPrediction = model_info.predictionOfSingleValues([distance_in_yards, penalty_log], attributes=CONSTANTS.ATTRIBUTES)
    xG = xgPrediction * xP
    # predict returns as a dataframe
    # we only need first value out of dataframe

    return xG, xP, ball_control_time


def xPModel(time_bigger, time_smaller):
    # todo: test xP Model function, with help of get_testing_DF
    # source: william spearman 2018, beyond expected goals
    # the ball control time can be between 0 and 5, if it is higher than 5, the xP = 100% (according to the formula)

    # this calculates the ball control time for three decimals after the dot
    ball_control_time = time_bigger - time_smaller
    # if the ball contol time is bigger than 4.99, it will be set to 4.99
    # there is near to none movement in xP after 4.99
    if ball_control_time > 4.99:
        ball_control_time = 4.99
    # this is the time span a footballer can control the ball
    possible_range_of_sec = np.arange(0, 5, 0.001)
    # these are the possibilities to control the ball for a certain time span
    """
    To convert the time difference into a probability, an exponential cumulative distribution function (CDF) is used. 
    Spearman (2018) assumes a lambda in the function of 4.32/second. 
    This would mean that an average professional footballer needs 0.23 seconds to control the ball. 
    On the y-axis of the distribution function, the cumulative probability is described. 
    This means, for example, for the point (x) delta 1 second, that 98% of professional football players can control the ball within this one second.
    source: Spearman, W. (2018). Beyond Expected Goals. MIT SLOAN Sports Analytics Conference.
    """
    possible_xP_values = expon.cdf(possible_range_of_sec, 0, 1 / 4.32)
    # find the position where the ball control time is closest to in the possible range of sec
    position = 0
    for position in range(len(possible_range_of_sec)):
        bc = possible_range_of_sec[position]
        # math is close compares floats
        # if abs(ball control time - bc) is less than 1e-9 * max(abs(ball control time), abs(bc)),
        # then ball control time and bc are considered "close" to each other.
        # This guarantees that a and b are equal to about nine decimal places.
        # https://davidamos.dev/the-right-way-to-compare-floats-in-python/
        # the comparison should be done in the third spot after the dot
        if math.isclose(ball_control_time, bc, abs_tol=1e-3):
            # if the position is found, stop the loop
            # the position is still saved as a variable
            break
    xP = possible_xP_values[position]
    return xP, ball_control_time
