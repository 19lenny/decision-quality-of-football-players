from typing import List
from SetUp import DataManipulation, CONSTANTS
import numpy as np
from SetUp.DecisionEvaluation import evaluationHelper, offside


def decisionEvaluation(dfSeason, eventname):
    # create a list to fill the alternative xG Values
    xG_best_alternative: List[float] = [0.0] * len(dfSeason)
    # create a list to fill the difference between the shooters decision and the best alternative
    xG_difference: List[float] = [0.0] * len(dfSeason)
    # create a list to fill the xPass to the best alternatives
    xP_best_alternative: List[float] = [0.0] * len(dfSeason)
    # create a list to track if the players make the right decisions
    shot_correct_decision: List[bool] = [True] * len(dfSeason)
    # create a list to save the location of the best alternative solution
    x_alternative: List[float] = [0.0] * len(dfSeason)
    y_alternative: List[float] = [0.0] * len(dfSeason)
    # create a list to save the player from the best alternative solution
    alternative_player: List[str] = ["None"] * len(dfSeason)

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
        # all Teammates which are offside are not taken in to account and are therefore thrown out of the df
        dfTeammates = dfOtherPlayers.loc[
            (dfOtherPlayers['teammate'] == True) & (dfOtherPlayers['isOffside'] == False)]
        # the index has to be reset, otherwise we cannot go through with a for loop
        dfTeammates.reset_index(inplace=True)
        dfOpponents = dfOtherPlayers.loc[dfOtherPlayers['teammate'] == False]
        dfOpponents.reset_index(inplace=True)

        # go through all 0.5 square meters on the pitch
        # but start from 40 yards from the goal away, everything farther away creates not higher xG values

        square_meter_size = 0.5
        max_shot_distance = 40
        # create the x linspace of the pitch, the end value gets +square meter size,
        # such that the endpoint is still in the range
        # this creates a range from 80 to 120 with step size 0.5
        x_range_pitch = np.arange(CONSTANTS.X_COORDINATE_GOALCENTRE - max_shot_distance,
                                  CONSTANTS.X_COORDINATE_GOALCENTRE + square_meter_size,
                                  square_meter_size)
        # create the y linspace of the pitch, the end value gets +square meter size,
        # such that the endpoint is still in the range
        y_range_pitch = np.arange(CONSTANTS.Y_MIDDLE_LINE1,
                                  CONSTANTS.Y_MIDDLE_LINE2 + square_meter_size,
                                  square_meter_size)

        for x in x_range_pitch:
            for y in y_range_pitch:
                # the player cannot shoot, when the ball is in the post --> the posts should be skipped
                if (x == 120) and (y == 36 or y == 44):
                    continue
                # debug
                # find the distance the ball has to travel to get from its current location to the location looked at
                ball_distance = DataManipulation.distanceObjectToPoint(x_shooting_player, y_shooting_player, x, y)
                # find the distance of the teammate, which is the closest to the current position looked at
                closest_teammate_x, closest_teammate_y, distance_closest_teammate, position_closest_teammate, name_closest_teammate = \
                    evaluationHelper.findClosestPlayer(dfTeammates, x, y)
                # find the distance of the opponent, which is the closest to the current position looked at
                # the closest opponent is only the goalkeeper, if and only if the keeper is the first on the ball
                closest_opponent_x, closest_opponent_y, distance_closest_opponent, position_opponent_teammate, name_closest_opponent = \
                    evaluationHelper.findClosestPlayer(dfOpponents, x, y)

                # check if the closest opponent is a goalkeeper,
                # if not everything's ok.
                if position_opponent_teammate == 'Goalkeeper':
                    # if he is a goalkeeper,
                    # check if the goalkeeper has the longer distance to the square than our team member
                    # if not (goalkeeper has shorter way) everything's ok
                    if distance_closest_opponent > distance_closest_teammate:
                        # if the opponent goalkeeper has the longer way than our team member,
                        # take goalkeeper out of the opponent dataframe and calculate again for another player of the opponent
                        dfOpponentsNoGK = dfOpponents.loc[dfOpponents['name_position'] != 'Goalkeeper']
                        dfOpponentsNoGK.reset_index(inplace=True)
                        closest_opponent_x, closest_opponent_y, distance_closest_opponent, position_opponent_teammate, name_closest_opponent = \
                            evaluationHelper.findClosestPlayer(dfOpponentsNoGK, x, y)

                # calculate the time (in seconds) it needs for...
                # ...the ball to arrive at the current looked at location
                time_ball = evaluationHelper.getTimeForDistance(ball_distance, CONSTANTS.BALL_SPEED)
                # ...the closest opponent to arrive at the looked at location
                time_opponent = evaluationHelper.getTimeForDistance(distance_closest_opponent, CONSTANTS.PLAYER_SPEED)
                # ...the closest teammate to arrive at the looked at location
                time_team_member = evaluationHelper.getTimeForDistance(distance_closest_teammate,
                                                                       CONSTANTS.PLAYER_SPEED)

                # calculate xG for current location, if xG is higher as the last calculated xG, save the value

                xG_for_current_location, xP_for_current_location = \
                evaluationHelper.xGFromAlternative(time_team_member,
                                                   time_opponent,
                                                   time_ball,
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
                    # if x_alternative == 0 and y_alternative == 0 then no other teammate is in the current frame
                    x_alternative[currentShot] = x
                    y_alternative[currentShot] = y
                    # create a list to save the player from the best alternative solution
                    alternative_player[currentShot] = name_closest_teammate
                    # add xPass
                    if xG_difference[currentShot] < 0:
                        shot_correct_decision[currentShot] = False
                    else:
                        shot_correct_decision[currentShot] = True


        print("progress bar of xG alternatives: ", currentShot, " / ", len(dfSeason) - 1, " | ", currentShot / (len(dfSeason) - 1) * 100,
              "%")

    dfSeason['xG_best_alternative'] = xG_best_alternative
    dfSeason['xG_Delta_decision_alternative'] = xG_difference
    dfSeason['shot_decision_correct'] = shot_correct_decision
    dfSeason['xP_best_alternative'] = xP_best_alternative
    dfSeason['x_best_alt'] = x_alternative
    dfSeason['y_best_alt'] = y_alternative
    dfSeason['player_name_alt'] = alternative_player

    attributes_added = 'xG_best_alternative', 'xG_Delta_decision_alternative', 'shot_decision_correct', \
        'xP_best_alternative', 'x_best_alt', 'y_best_alt', 'player_name_alt'
    return dfSeason, attributes_added
