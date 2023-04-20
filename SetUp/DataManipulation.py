from typing import List

import pandas as pd
import numpy as np
from statsbombpy import sb
from SetUp import CONSTANTS
import math
from scipy.stats import shapiro, kstest
import matplotlib.pyplot as plt
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
def angle(df):
    # Morales cesar a "A mathematics-based new penalty area in football: tackling diving", Journal of sports sciences
    # cosinussatz

    angleList = []
    bList = []
    cList = []
    for shot in range(len(df)):
        b = ((df["x_coordinate"][shot] - CONSTANTS.X_COORDINATE_POST1) ** 2 +
             (df["y_coordinate"][shot] - CONSTANTS.Y_COORDINATE_POST1) ** 2) ** 0.5
        bList.append(b)
        c = ((df["x_coordinate"][shot] - CONSTANTS.X_COORDINATE_POST2) ** 2 +
             (df["y_coordinate"][shot] - CONSTANTS.Y_COORDINATE_POST2) ** 2) ** 0.5
        cList.append(c)
        # if the ball is played to the post, then the vectors are 0 and a division by 0 happens.
        # we define the angles when playing to the post as 0, as we should not play the ball to the post
        if b == 0 or c == 0:
            angleList.append(0)
        else:
            angleList.append( np.rad2deg(np.arccos((df["b"] ** 2 + df["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                       / (2 * df["b"] * df["c"]))))
    df['b'] = bList
    df['c'] = cList
    df['angleDeg'] = angleList

    return df



# angle in radian
def angleInRadian(df):

    angleList = []
    bList = []
    cList = []
    for shot in range(len(df)):
        b = ((df["x_coordinate"][shot] - CONSTANTS.X_COORDINATE_POST1) ** 2 +
             (df["y_coordinate"][shot] - CONSTANTS.Y_COORDINATE_POST1) ** 2) ** 0.5
        bList.append(b)
        c = ((df["x_coordinate"][shot] - CONSTANTS.X_COORDINATE_POST2) ** 2 +
             (df["y_coordinate"][shot] - CONSTANTS.Y_COORDINATE_POST2) ** 2) ** 0.5
        cList.append(c)
        # if the ball is played to the post, then the vectors are 0 and a division by 0 happens.
        # we define the angles when playing to the post as 0, as we should not play the ball to the post
        if b == 0 or c == 0:
            angleList.append(0)
        else:
            angleList.append(np.arccos((df["b"] ** 2 + df["c"] ** 2 - CONSTANTS.GOAL_LENGTH ** 2)
                                       / (2 * df["b"] * df["c"])))
    df['b'] = bList
    df['c'] = cList
    df['angleInRadian'] = angleList

    return df


def angleInRadianFromObjectToPoints(x_object, y_object, x_point1, y_point1, x_point2, y_point2):
    b = ((x_object - x_point1) ** 2 + (y_object - y_point1) ** 2) ** 0.5
    c = ((x_object - x_point2) ** 2 + (y_object - y_point2) ** 2) ** 0.5
    a = ((x_point1 - x_point2) ** 2 + (y_point1 - y_point2) ** 2) ** 0.5
    if b == 0 or c == 0:
    # if the ball is played to the post, then the vectors are 0 and a division by 0 happens.
    # we define the angles when playing to the post as 0, as we should not play the ball to the post
        return 0
    angle_in_rad = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

    return angle_in_rad


# calculate distance and write it to the df
# return the adjusted df
def distancePlayerToGoal(df):
    # distance
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    df["distance_to_goal_centre"] = ((df["x_coordinate"] - CONSTANTS.X_COORDINATE_GOALCENTRE) ** 2 +
                                     (df["y_coordinate"] - CONSTANTS.Y_COORDINATE_GOALCENTRE) ** 2) ** 0.5
    return df


# calculate distance
# return the distance in yards
def distanceObjectToPoint(x_object, y_object, x_point, y_point):
    # pythagoras --> ((x1-x2)^2+(y1-y2)^2)^0.5
    distance = ((x_object - x_point) ** 2 + (y_object - y_point) ** 2) ** 0.5
    return distance


def addGoalBinary(dataframe):
    dataframe['goal'] = np.where(dataframe['shot_outcome'] == 'Goal', 1, 0)
    dataframe['goal'] = np.where(dataframe['type'] == "Own Goal Against", -1, dataframe['goal'])
    return dataframe

"""
isWinning determines if a team is currently (before the current shot decision) winning, drawing or loosing
if the team that takes the shot is winning, the function returns 1, is drawing returns 0, is loosing returns -1
"""
def isWinning(shooting_team, home_team, home_team_score, away_team_score):
    if shooting_team == home_team:
        if home_team_score > away_team_score:
            return 1
        elif home_team_score == away_team_score:
            return  0
        elif home_team_score < away_team_score:
            return -1
    else:
        if home_team_score > away_team_score:
            return -1
        elif home_team_score == away_team_score:
            return 0
        elif home_team_score < away_team_score:
            return 1

"""
calculates the score of every shot in the whole dataframe
the score is always the score before the actual shot happened
this is done like this because the previous result has influence on the player and his shot 
and NOT the score after the shot!
There are several columns added to the dataframe. They are explained here:

dfCurrentMatch['scoring_difference'] = scoring_difference:
            # determines the scoring difference between the two opponents
            # if it is 0 the result is a draw
            # if it is positive the home team is winning
            # if it is negative the away team is winning
dfCurrentMatch['home_score'] = score_home_team
            # this is the live score of the home_team
dfCurrentMatch['away_score'] = score_away_team:
            #this is the live score of the away team
dfCurrentMatch['score'] = scores:
            # scores determines if the current shooting team is before the current shot either winning, drawing or loosing
            # if it is 1 the shooting team is winning before taking the current shot
            # if it is 0 the shooting team is drawing before the current shot
            # if it is -1 the shooting team is loosing before the current shot
"""

def score(df):
    # first extract all match id of dataframe in a unique list
    match_id = df[["match_id"]].drop_duplicates()
    match_id = match_id.values.tolist()
    dfUpdated = pd.DataFrame()
    # the scores are seen from the home team perspective

    for match in range(len(match_id)):
        # set up for every match
        # get all shots that happened for the current match id,
        # sort all these shot according to minutes
        # 0 hast to be there since match id is a double list
        dfCurrentMatch = df.loc[df['match_id'] == match_id[match][0]].sort_values(by = ['minute', 'second'])

        # reset index to go through in the for loop
        dfCurrentMatch.reset_index(inplace=True)
        # create helper lists that should be filled
        position = 0
        # scores determines if the current shooting team is before the current shot either winning, drawing or loosing
        # if it is positive the shooting team is winning before taking the current shot
        # if it is 0 the shooting team is drawing before the current shot
        # if it is negative the shooting team is loosing before the current shot
        scores: List[int] = [0] * len(dfCurrentMatch)
        # determines the scoring difference between the two opponents
        # previous_overall_scoring_difference is the scoring difference between the two opponents,
        # if it is 0 the result is a draw
        # if it is positive the home team is winning
        # if it is negative the away team is winning
        scoring_difference: List[int] = [0] * len(dfCurrentMatch)
        # the score of the home team, before a shot is taken
        score_home_team: List[int] = [0] * len(dfCurrentMatch)
        # the score of the away team, before the shot is taken
        score_away_team: List[int] = [0] * len(dfCurrentMatch)

        # helper variables that calculate the scores

        previous_overall_scoring_difference = 0
        # these two variables show the live result during the shots
        # if the score in 67th minute is 2:1 in Germany vs Switzerland,
        # then the shot that is following after the 67th minute shows this result with
        # previous_home_team_score = 2, previous_away_team_score = 1
        previous_home_team_score = 0
        previous_away_team_score = 0

        # go through every shot in the current match (the shots are sorted by minute)
        for shot in range(len(dfCurrentMatch)):
            # who is the home team of the game
            home_team = dfCurrentMatch['home_team'][shot]
            # who is the away team of the game
            away_team = dfCurrentMatch['away_team'][shot]
            # which team fired the shot
            shooting_team = dfCurrentMatch['team'][shot]
            # did the current shot lead to a goal? then we have to adjust the score
            if dfCurrentMatch['goal'][shot] == 1:
                # home team scored
                if shooting_team == home_team:

                    # all the scores are updated with the last score in the game
                    # they are not updated with the new score, because the player made the decision to shoot, under the old score
                    # the next decision taken is influenced by the new result, BUT the shot that was taken to shoot the goal was taken influenced by the old score
                    scoring_difference[position] = previous_overall_scoring_difference
                    score_home_team[position] = previous_home_team_score
                    score_away_team[position] = previous_away_team_score
                    # scores evaluates
                    scores[position] = isWinning(shooting_team=shooting_team, home_team=home_team,
                                                 home_team_score=previous_home_team_score, away_team_score=previous_away_team_score)
                    # add the goal to the scoring line
                    # it is added to the dataframe with the next shot, because the next shot is influenced by the new score
                    previous_home_team_score += 1
                    previous_overall_scoring_difference = previous_home_team_score - previous_away_team_score

                # away team scores
                else:

                    #same as home team score
                    scoring_difference[position] = previous_overall_scoring_difference
                    score_home_team[position] = previous_home_team_score
                    score_away_team[position] = previous_away_team_score
                    scores[position] = isWinning(shooting_team=shooting_team, home_team=home_team,
                                              home_team_score=previous_home_team_score,
                                              away_team_score=previous_away_team_score)

                    previous_away_team_score += 1
                    previous_overall_scoring_difference = previous_home_team_score - previous_away_team_score
            #other possibility could be own goal
            elif dfCurrentMatch['goal'][shot] == -1:
                #check who produced the own goal, either home team or away team
                #the shooting team is the home team, therefore the home team scored the own goal
                if shooting_team == home_team:

                    # all the scores are updated with the last score in the game
                    # they are not updated with the new score, because the player made the decision to shoot, under the old score
                    # the next decision taken is influenced by the new result, BUT the shot that was taken to shoot the goal was taken influenced by the old score
                    scoring_difference[position] = previous_overall_scoring_difference
                    score_home_team[position] = previous_home_team_score
                    score_away_team[position] = previous_away_team_score
                    # scores evaluates
                    scores[position] = isWinning(shooting_team=shooting_team, home_team=home_team,
                                                 home_team_score=previous_home_team_score, away_team_score=previous_away_team_score)
                    # add the goal to the scoring line
                    # it is added to the dataframe with the next shot, because the next shot is influenced by the new score
                    previous_away_team_score += 1
                    previous_overall_scoring_difference = previous_home_team_score - previous_away_team_score

                # away team scores own goal
                else:

                    #same as home team score
                    scoring_difference[position] = previous_overall_scoring_difference
                    score_home_team[position] = previous_home_team_score
                    score_away_team[position] = previous_away_team_score
                    scores[position] = isWinning(shooting_team=shooting_team, home_team=home_team,
                                              home_team_score=previous_home_team_score,
                                              away_team_score=previous_away_team_score)

                    previous_home_team_score += 1
                    previous_overall_scoring_difference = previous_home_team_score - previous_away_team_score

            # no goal happened
            else:

                scoring_difference[position] = previous_overall_scoring_difference
                score_home_team[position] = previous_home_team_score
                score_away_team[position] = previous_away_team_score
                scores[position] = isWinning(shooting_team=shooting_team, home_team=home_team,
                                          home_team_score=previous_home_team_score,
                                          away_team_score=previous_away_team_score)
            position += 1

        dfCurrentMatch['scoring_difference'] = scoring_difference
        dfCurrentMatch['home_score'] = score_home_team
        dfCurrentMatch['away_score'] = score_away_team
        dfCurrentMatch['score'] = scores
        dfUpdated = pd.concat([dfUpdated, dfCurrentMatch])
    dfUpdated.reset_index(drop=True, inplace=True)
    return dfUpdated

"""
normal distibution is not mandatory.
Some researchers say the test is robust enough to work without the normal distribution:
https://statistikguru.de/spss/ungepaarter-t-test/normalverteilung-verletzt-4.html#:~:text=Simulationsstudien%20haben%20gezeigt%2C%20dass%20der,%2DU%2DTest%20genannt).
Kubinger, Rasch, und Moder (2009) gehen sogar noch einen Schritt weiter und empfehlen ab einer Stichprobengröße von 30
gar nicht erst die Normalverteilung zu überprüfen, dafür aber den t-Test für ungleiche Varianzen (auch Welch-Test genannt)
stattdessen zu interpretieren, was wir auf den nachfolgenden Seiten auch noch ausführlicher besprechen werden.
Die Alternative zu einem tTest wäre: Wilcoxon-Mann-Whitney-Test (auch Mann-Whitney-U-Test genannt)
"""
def check_normal_distribution(df):
    plt.hist(df[CONSTANTS.EVALUATION_VARIABLE], edgecolor='black', bins=20)
    plt.show()

    kolmo_val, p_val = shapiro(df[CONSTANTS.EVALUATION_VARIABLE])
    if p_val > 0.05:
        print("data is normal distributed")
        return True
    else:
        print("data is not normal distributed")
        return False

def tranf_normal_distribution(df):
    #first try to transform the data to a x_log
    x_log = pd.DataFrame()
    x_log[CONSTANTS.EVALUATION_VARIABLE] = np.log(abs(df[CONSTANTS.EVALUATION_VARIABLE])+0.0000001)
    normal_distr = check_normal_distribution(x_log)

    x_square = pd.DataFrame()
    x_square[CONSTANTS.EVALUATION_VARIABLE] = np.sqrt(abs(df[CONSTANTS.EVALUATION_VARIABLE]))
    normal_distr_square = check_normal_distribution(x_square)

    #cube root transformation
    x_cube = pd.DataFrame()
    x_cube[CONSTANTS.EVALUATION_VARIABLE] = np.cbrt(abs(df[CONSTANTS.EVALUATION_VARIABLE]))
    normal_distr_cube = check_normal_distribution(x_cube)

    if normal_distr:
        print("data is normal distributed when transformed to log")
        return True
    elif normal_distr_square:
        print("data is normal distributed when transformed with square root")
        return True
    elif normal_distr_cube:
        print("data is normal distributed when transformed with cube root")
        return True
    else:
        print("data is NOT normal distributed")
        return False
def log_penalty(df):
    penaltyList = []
    for shot in range(len(df)):
        # if the shot is equal to 0, then the penalty has to be limited
        # the reason for that is that log(0) is undefined,
        # we therefore limit the penalty to maximal -5 --> log(0.00001)
        if df['angleInRadian'][shot] < 0.000001:
            penaltyList.append(-np.log10(0.001))
        else:
            # else create a penalty
            #if df['match_id'][shot] == 266254 and df['minute'][shot] == 74:
            w = shot
            x = df['angleInRadian'][shot]
            y = np.log(df['angleInRadian'][shot])
            z = -np.log(df['angleInRadian'][shot])
            #(-) weil kleine Winkel führen zu negativen penalties, der penalty soll aber je höher desto schlimmer sein
            penaltyList.append(-np.log10(df['angleInRadian'][shot]))
    df['log_pen_angle'] = penaltyList
    return df
def log_penalty_for_single_values(angle):
    if angle < 0.00000001:
        return -np.log(0.001)
    else: return -np.log10(angle)