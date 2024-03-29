from typing import List
from SetUp import DataManipulation, CONSTANTS
import numpy as np
from SetUp.DecisionEvaluation import evaluationHelper, offside
import pandas as pd
from tqdm import tqdm


def decisionEvaluation(dfSeason, eventname):
    # create a list to fill the alternative xG Values
    xG_best_alternative: List[float] = [0.0] * len(dfSeason)
    # create a list to fill the difference between the shooters decision and the best alternative
    xG_difference: List[float] = [0.0] * len(dfSeason)
    # create a list to fill the xPass to the best alternatives
    xP_best_alternative: List[float] = [0.0] * len(dfSeason)
    # add the times from xP so a better debug check can happen
    time_ball_list: List[float] = [0.0] * len(dfSeason)
    time_teammember_list:List[float] = [0.0] * len(dfSeason)
    time_opponent_list: List[float] = [0.0] * len(dfSeason)
    ball_control_time_list: List[float] = [0.0] * len(dfSeason)
    x_opponent: List[float] = [0.0] * len(dfSeason)
    y_opponent: List[float] = [0.0] * len(dfSeason)
    x_ball: List[float] = [0.0] * len(dfSeason)
    y_ball: List[float] = [0.0] * len(dfSeason)
    ball_distance_list: List[float] = [0.0] * len(dfSeason)
    teammate_distance: List[float] = [0.0] * len(dfSeason)
    opponent_distance: List[float] = [0.0] * len(dfSeason)
    # create a list to track if the players make the right decisions
    shot_correct_decision: List[bool] = [True] * len(dfSeason)
    # create a list to save the location of the best alternative solution
    x_alternative: List[float] = [0.0] * len(dfSeason)
    y_alternative: List[float] = [0.0] * len(dfSeason)
    # create a list to save the player from the best alternative solution
    alternative_player: List[str] = ["None"] * len(dfSeason)
    alternative_player_opponent: List[str] = ["None"] * len(dfSeason)
    #the features of the alternative
    feature_distance: List[float] = [0.0] * len(dfSeason)
    feature_angle: List[float] = [0.0] * len(dfSeason)
    feature_GK_distance: List[float] = [0.0] * len(dfSeason)

    # for every shot of the competition
    # this for loop gets every shot from a competition, starting with the first shot
    for currentShot in range(len(dfSeason)):
        # if shot freeze frame is empty, it still works, but returns 0 for x and y best alternative
        # get all players that were in the frame during the current shot and put in to a df
        dfOtherPlayers = evaluationHelper.getPlayersOfEvent(dfSeason['shot_freeze_frame'][currentShot], eventname)
        #if no other players are in the dataframe nothing is to fill out and this shot can be skipped
        if dfOtherPlayers.empty:
            continue
        # now the dataset is ready to check if the player originally made a good decision with shooting

        # get the calculated xG value for the current shot
        shooting_player_xG = dfSeason[CONSTANTS.MODELNAME][currentShot]
        x_shooting_player = dfSeason['x_coordinate'][currentShot]
        y_shooting_player = dfSeason['y_coordinate'][currentShot]

        # where is the offside line for this shot
        offside_x = offside.offsideLine(x_shooting_player, dfOtherPlayers)
        # update the dataframe to see who is offside
        # players in the opponent team cannot be offside, but players in the own team
        # if the players in the own team are offside, they cannot be passed to --> they are deleted in the next step
        dfOtherPlayers = offside.isOffside(offside_x, dfOtherPlayers)

        # split the dataframe in to teammates and opponents
        # all Teammates which are offside are not taken into account and are therefore thrown out of the df
        dfTeammates = dfOtherPlayers.loc[
            (dfOtherPlayers['teammate'] == True) & (dfOtherPlayers['isOffside'] == False)]
        # the index has to be reset, otherwise we cannot go through with a for loop
        dfTeammates.reset_index(drop=True, inplace=True)
        dfOpponents = dfOtherPlayers.loc[dfOtherPlayers['teammate'] == False]
        dfOpponents.reset_index(drop=True, inplace=True)

        # go through all 0.5 square meters on the pitch
        # but start from 33 yards (=30 meters) from the goal away, everything farther away is not expected to create high xG values

        square_yard_size = 0.5
        max_shot_distance = 33
        # create the x linspace of the pitch, the end value gets +square meter size,
        # such that the endpoint is still in the range
        # this creates a range from 90 to 120 with step size 0.5
        x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                                  CONSTANTS.X_COORDINATE_GOALCENTRE + square_yard_size,
                                  square_yard_size)
        # create the y linspace of the pitch, the end value gets +square meter size,
        # such that the endpoint is still in the range
        y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE_TOP,
                                  CONSTANTS.Y_MIDDLE_LINE_BOTTOM + square_yard_size,
                                  square_yard_size)
        # check every 0.5 square meter of the pitch
        for x in x_range_pitch:
            for y in y_range_pitch:
                # the player cannot shoot, when the ball is on the post --> the posts should be skipped
                if (x == 120) and (y == 36 or y == 44):
                    continue

                # find the distance the ball has to travel to get from its current location to the location looked at
                ball_distance = DataManipulation.distanceObjectToPoint(x_shooting_player, y_shooting_player, x, y)

                # calculate the time (in seconds) it needs for...
                # ...the ball to arrive at the current looked at location
                time_ball = evaluationHelper.getTimeForDistance(ball_distance, CONSTANTS.BALL_SPEED)

                # find the distance of the teammate, which is the closest to the current position looked at
                # as soon as the distance is known, the time can be calculated it needs for the player to get there
                closest_teammate_x, closest_teammate_y, distance_closest_teammate, position_closest_teammate, name_closest_teammate,time_team_member = \
                    evaluationHelper.findClosestPlayer(dfTeammates, x, y)
                # find the distance of the opponent, which is the closest to the current position looked at
                # the closest opponent is only the goalkeeper, if and only if the keeper is the first on the ball, otherwise the algorithm checks for other opponents which are close
                closest_opponent_x, closest_opponent_y, distance_closest_opponent, position_closest_opponent, name_closest_opponent, time_opponent = \
                    evaluationHelper.findClosestPlayer(dfOpponents, x, y)

                # check if the closest opponent is a goalkeeper,
                # if not everything's ok.
                if position_closest_opponent == 'Goalkeeper':
                    # if he is a goalkeeper,
                    # check if the goalkeeper arrives at the square before the ball. If this is the case the goalkeeper will come out of the goal and intercept the ball.
                    # if not then the ball is there first, so it has to be checked, if the goalkeeper arrives second (after the ball) at the square or if the teammate is second and therefore first on the ball
                    if time_opponent > time_ball:
                        # check if the goalkeeper has the longer distance to the square than our team member
                        # if goalkeeper has shorter way everything's ok. If goalkeeper has longer way, he will not come out of the goal,
                        # therefore it needs recalculation who is the closest opponent without the goalkeeper.
                        if time_opponent > time_team_member:
                            # if the opponent goalkeeper has the longer way than our team member,
                            # take goalkeeper out of the opponent dataframe and calculate again for another player of the opponent
                            dfOpponentsNoGK = dfOpponents.loc[dfOpponents['name_position'] != 'Goalkeeper']
                            dfOpponentsNoGK.reset_index(drop=True, inplace=True)
                            closest_opponent_x, closest_opponent_y, distance_closest_opponent, position_closest_opponent, name_closest_opponent, time_opponent = \
                                evaluationHelper.findClosestPlayer(dfOpponentsNoGK, x, y)

                #for debug reasons, the coordinates are just here, so it is not printed 100000 times. one check per shot is enough:
                if (x == 100) and (y == 40):
                    if distance_closest_teammate == 1000:
                        print("no teammate found")
                    if distance_closest_opponent == 1000:
                        print("no opponent found")

                # calculate xG for current location, if xG is higher as the last calculated xG, save the value

                xG_for_current_location, xP_for_current_location, ball_control_time, angle_alternative, distance_alternative, delta_GK_alternative\
                    = evaluationHelper.xGFromAlternative(time_team_member,
                                                   time_opponent,
                                                   time_ball,
                                                   df_opponents=dfOpponents,
                                                   x_location=x, y_location=y)


                # if the alternative xG value for this current location is higher than for the other ones,
                # than update for the current shot the highest xG alternative

                if xG_for_current_location > xG_best_alternative[currentShot]:
                    xG_best_alternative[currentShot] = xG_for_current_location
                    # if the difference is negative, the player took the wrong decision
                    xG_difference[currentShot] = dfSeason[CONSTANTS.MODELNAME][
                                                     currentShot] - xG_for_current_location
                    # add the xP of the best alternative
                    xP_best_alternative[currentShot] = xP_for_current_location
                    time_ball_list[currentShot] = time_ball
                    time_opponent_list[currentShot] = time_opponent
                    time_teammember_list[currentShot] = time_team_member
                    ball_control_time_list[currentShot] = ball_control_time
                    # if x_alternative == 0 and y_alternative == 0 then no other teammate is in the current frame
                    x_alternative[currentShot] = closest_teammate_x
                    y_alternative[currentShot] = closest_teammate_y
                    x_ball[currentShot] = x
                    y_ball[currentShot] = y
                    x_opponent[currentShot] = closest_opponent_x
                    y_opponent[currentShot] = closest_opponent_y
                    ball_distance_list[currentShot] = ball_distance
                    teammate_distance[currentShot] = distance_closest_teammate
                    opponent_distance[currentShot] = distance_closest_opponent

                    # create a list to save the player from the best alternative solution
                    alternative_player[currentShot] = name_closest_teammate
                    alternative_player_opponent[currentShot] = name_closest_opponent
                    #add the new features to the dataframe
                    feature_angle[currentShot] = angle_alternative
                    feature_distance[currentShot] = distance_alternative
                    feature_GK_distance[currentShot] = delta_GK_alternative

                    if xG_difference[currentShot] < 0:
                        shot_correct_decision[currentShot] = False
                    else:
                        shot_correct_decision[currentShot] = True


        print("progress bar of xG alternatives: ", currentShot, " / ", len(dfSeason) - 1, " | ", currentShot / (len(dfSeason) - 1) * 100, "%")

    dfSeason['xG_best_alternative'] = xG_best_alternative
    dfSeason['xG_Delta_decision_alternative'] = xG_difference
    dfSeason['shot_decision_correct'] = shot_correct_decision
    dfSeason['xP_best_alternative'] = xP_best_alternative
    dfSeason['ball_control_time'] = ball_control_time_list
    dfSeason['time_ball'] = time_ball_list
    dfSeason['time_teammember'] = time_teammember_list
    dfSeason['time_opponent'] = time_opponent_list
    dfSeason['distance_ball'] = ball_distance_list
    dfSeason['distance_teammember'] = teammate_distance
    dfSeason['distance_opponent'] = opponent_distance
    dfSeason['x_ball'] = x_ball
    dfSeason['y_ball'] = y_ball
    dfSeason['x_best_alt'] = x_alternative
    dfSeason['y_best_alt'] = y_alternative
    dfSeason['x_opponent'] = x_opponent
    dfSeason['y_opponent'] = y_opponent
    dfSeason['player_name_alt'] = alternative_player
    dfSeason['player_namer_opponent'] = alternative_player_opponent
    dfSeason['distance_alternative'] = feature_distance
    dfSeason['angle_alternative'] = feature_angle
    dfSeason['delta_GK_line_alternative'] = feature_GK_distance


    return dfSeason
