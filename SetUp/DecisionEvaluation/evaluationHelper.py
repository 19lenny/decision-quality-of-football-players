import math
import os
import json
import pandas as pd
from SetUp import CONSTANTS, DataManipulation
from scipy.stats import expon
from decimal import *
import numpy as np
from Model import model_info
import random


# calculates the closest distance (in yards) of every player in a dataframe, for a given position
def findClosestPlayer(dataframe, x_location, y_location):
    x = None
    y = None
    # needs an init value, this value is overwritten with the first player incoming
    closestDistance = 1000
    position = None
    name = None
    time = None
    # before the calculation of the closest teammates can start, it has to be checked if there is a player in the df,
    # if not the alternative xG value was 0 and the iteration can be skipped
    if dataframe.empty:
        x = 0
        y = 0
        position = None
        name = "No Teammate found"
        time = getTimeForDistance(closestDistance, CONSTANTS.PLAYER_SPEED)
        return x,y,closestDistance,position,name,time

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
            time = getTimeForDistance(closestDistance, CONSTANTS.PLAYER_SPEED)


    return x, y, closestDistance, position, name, time


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
    random_number = random.randint(1, 10000000000)
    filename = keyword + str(random_number) + ".json"
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

def deltaDistanceGKToOptimalLine(df_opponents, shot_location, time_ball, time_teammember):
    #if there is no GK in the dataframe the method should return none
    x = df_opponents.loc[df_opponents['name_position'] == 'Goalkeeper'].empty
    if df_opponents.loc[df_opponents['name_position'] == 'Goalkeeper'].empty:
        return None
    # a value error could happen if the coordinates of the GK are corrupted, catch this error, print the dataframe of the error and return 0
    try:
        # search for the GK location.
        #iloc[0] returns the value instead of a dataframe
        x_loc_GK = df_opponents['x_coordinate'][df_opponents['name_position'] == 'Goalkeeper'].iloc[0]
        #x_loc_GK.reset_index(drop=True, inplace=True)
        y_loc_GK = df_opponents['y_coordinate'][df_opponents['name_position'] == 'Goalkeeper'].iloc[0]
        GK_location = (x_loc_GK, y_loc_GK)
        # If the goalkeeper is not in the frame, the method will return 0, such that the GK doesnt play a role in the xG calculation
        # searches the closest point for the GK to the optimal line (angle line)
        intersection = DataManipulation.intersection_point_GK_Shot(GK_location, shot_location)
        if intersection is None:
            return None
        # calculates the distance to this optimal location
        distance_to_optimal_line = DataManipulation.distanceObjectToPoint(x_object=GK_location[0], y_object=GK_location[1], x_point=intersection[0], y_point=intersection[1])
        # time to achieve this distance for the GK
        time_to_optimal_line = getTimeForDistance(distance=distance_to_optimal_line, speed=CONSTANTS.PLAYER_SPEED)
        # search for the limiting factor (how much time does the goalkeeper have to move before the shot is arriving)
        # if the ball is slower than the teammember of the shooting player, than the time of the ball is the limiting factor
        if time_ball >= time_teammember:
            time_limit = time_ball
        #else the time limit is when the teammember arrives
        #if the opponent is faster than the teammember we don't care, since the GK still has to move to the correct position
        else: time_limit = time_teammember
        # we have now every factor, to calculate how far the goalkeeper is coming in the limiting time factor
        distance_limit = time_limit * CONSTANTS.PLAYER_SPEED
        # calculate the difference, between what the GK can achieve in time and what he should achieve in this time

        #if the distance to the optimal line is bigger than the distance_limit, the delta is distance to optimal line - what the GK can achieve in this time
        if distance_to_optimal_line > distance_limit:
            delta = distance_to_optimal_line - distance_limit
        # if the GK achieves more yards than needed the function returns 0, since the GK has time to achieve a optimal point
        else: delta = 0
        return delta
    except TypeError:
        print(df_opponents.loc[df_opponents['name_position'] == 'Goalkeeper'])
        return None



def xGFromAlternative(time_teammate, time_opponent, time_ball, df_opponents, x_location, y_location):
    # cannot return none, but can return 0
    # 0 describes no chance of scoring
    xG = 0
    xP = 0
    ball_control_time = 0
    angle_in_rad = 0
    distance_in_yards = 0
    delta_distance_GK_to_optimal_position = 0
    # cases where the defender clears the ball

    # if the opponent is there before the teammate is there, then the opponent will clear the ball
    if time_opponent < time_teammate:
        # no further calculation needed, return the none value and close method
        return xG, xP, ball_control_time, angle_in_rad, distance_in_yards, delta_distance_GK_to_optimal_position
    # case opponent is slower than the teammate, but is there before the ball arrives,
    # therefore the opponent can clear the ball
    elif time_ball > time_opponent:
        # no further calculation needed, return the none value and close method
        return xG, xP, ball_control_time, angle_in_rad, distance_in_yards, delta_distance_GK_to_optimal_position

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
                                                                    x_point1=CONSTANTS.X_COORDINATE_POST_L,
                                                                    y_point1=CONSTANTS.Y_COORDINATE_POST_L,
                                                                    x_point2=CONSTANTS.X_COORDINATE_POST_R,
                                                                    y_point2=CONSTANTS.Y_COORDINATE_POST_R)
    distance_in_yards = DataManipulation.distanceObjectToPoint(x_object=x_location, y_object=y_location,
                                                               x_point=CONSTANTS.X_COORDINATE_GOALCENTRE,
                                                               y_point=CONSTANTS.Y_COORDINATE_GOALCENTRE)
    ln_angle = DataManipulation.log_angle_single_values(angle=angle_in_rad)
    # returns the numbers of yards the GK actually is away from this optimal line due to the time limitation
    delta_distance_GK_to_optimal_position = deltaDistanceGKToOptimalLine(df_opponents=df_opponents,
                                                                                          shot_location=(x_location, y_location),
                                                                                          time_ball=time_ball,
                                                                                          time_teammember=time_teammate)
    #design choice, if the GK is not in frame, or there is no intersection point, the goalkeeper is automatically in the right position
    if delta_distance_GK_to_optimal_position is None:
        delta_distance_GK_to_optimal_position = 0
    # xG on the current location is the prediction of the expected goal from this location,
    # based on the angle of the location to the goal and the distance of the location to the goal
    # the prediction has to be multiplied with the xPass prediction
    # (the longer the teammate has time, the higher will be xP)
    xgPrediction = model_info.predictionOfSingleValues([distance_in_yards, ln_angle, delta_distance_GK_to_optimal_position], attributes=CONSTANTS.ATTRIBUTES)
    xG = xgPrediction * xP
    # predict returns as a dataframe
    # we only need first value out of dataframe

    return xG, xP, ball_control_time, angle_in_rad, distance_in_yards, delta_distance_GK_to_optimal_position


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
    Spearman (2018) assumes a lambda in the function of 4.30/second. 
    This would mean that an average professional footballer needs 0.23 seconds to control the ball. 
    On the y-axis of the distribution function, the cumulative probability is described. 
    This means, for example, for the point (x) delta 1 second, that 98% of professional football players can control the ball within this one second.
    source: Spearman, W. (2018). Beyond Expected Goals. MIT SLOAN Sports Analytics Conference.
    """
    possible_xP_values = expon.cdf(possible_range_of_sec, 0, 1 / 4.30)
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


