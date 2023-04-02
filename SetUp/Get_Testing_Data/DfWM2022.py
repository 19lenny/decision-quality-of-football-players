from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values

"""
DfEM2020: prepare the dataset of EM2020, such it can be evaluated.
The dataset is manipulated, such that it only contains shots, and no other events.
Shots from penalties, free kicks and headers are not taken into account, since they distort the picture.
The dataset of the shot events is joined with the dataset of the according match.
Like this we have additional information about the game.
Additionally the dataset is manipulated, such that 4 additional rows are created (x, y, angle, distance).
Angle calculates the open angle from the striker to the goal.
Distance calculates the distance from the striker to the goal centre.
the manipulated dataset is saved in a JSON format.
"""

# 43,106 is the code of the EM 2020. This can be found in the excel overview "CompetitionOverview.xlsx"
dfMatchesWM22 = pd.DataFrame(sb.matches(43, 106))

# all matchID's WM22
matchIdWM22 = dfMatchesWM22.match_id.values.tolist()

# initialize df
dfShotWM22 = pd.DataFrame()

# this must be done for every event in every game,
# then we have a dataframe with all shots from every game from the WM22
counter = 0
for event in matchIdWM22:
    get_all_events_of_this_match = sb.events(event)
    # only keep the shots, in the rest we are not interested
    get_all_events_of_this_match = get_all_events_of_this_match.query("type == 'Shot'")
    dfShotWM22 = pd.concat([dfShotWM22, get_all_events_of_this_match])
    counter += 1
    print("nothing to worry - still working")
    print("progress bar to get all events at WM22: ", counter, " / ", len(matchIdWM22))

# set the key index for the join later
dfMatchesWM22.set_index("match_id")

# join Shots and Matches, therefore we know from every score the competition stage,
# the competition and additional information
dfWM22 = dfShotWM22.join(dfMatchesWM22.set_index('match_id'), on='match_id')
dfWM22.reset_index(drop=True, inplace=True)

# before we save the df, we want to add crucial information to the shot,
# with this information we can later calculate the xG
# therefore we calculate for every shot, the angle and the distance

# convert coordinates from list, to x and y entries
dfWM22 = DataManipulation.coordinates(dfWM22)
# add angle
dfWM22 = DataManipulation.angle(dfWM22)
# add angle in rad
dfWM22 = DataManipulation.angleInRadian(dfWM22)
# add distance
dfWM22 = DataManipulation.distancePlayerToGoal(dfWM22)
#add goal
dfWM22 = DataManipulation.addGoalBinary(dfWM22)
#add xGoal, calculated by me
dfWM22 = model_info.prediction(dfWM22)

# add the current score of this competition
dfWM22 = DataManipulation.score(dfWM22)
print("score is done")

# only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
# this way some time is saved in the next call
dfWM22 = dfWM22.query(
    "type == 'Shot' & shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
dfWM22.reset_index(drop=True, inplace=True)

# add the transfer value of every shooting player
dfWM22, attributes_added_TM = TM_values.transfermarketValue(dfCompetition=dfWM22, competition="WM22")
print("TM Value is added")

# calculates
# - the xG of the best alternative
# - the x and y coordinate of the best alternative
# - the difference of the shooting players decision and the decision of the best alternative
# - if the shooting player made the best decision
# - the xP of the pass that would be needed to go to the best alternative
dfWM22, attributes_added_xG = evaluate_decision.decisionEvaluation(dfWM22, "WM22")


# save only the needed columns
dfWM22 = dfWM22[
    ["x_coordinate", "y_coordinate", "shot_end_location", "shot_outcome", "angle", "angleInRadian", "distance_to_goal_centre",
     "shot_statsbomb_xg", "goal", "match_id", "shot_body_part", "period",
     "team", "play_pattern", "minute", "player", "shot_freeze_frame", "shot_type", "match_date", "competition",
     "season", "home_team", "away_team", "home_score", "away_score", "competition_stage",
     "xG", 'xG_best_alternative', 'xG_Delta_decision_alternative', 'shot_decision_correct',
        'xP_best_alternative', 'x_best_alt', 'y_best_alt', 'player_name_alt', 'value']]
#todo: these tasks
# other file, add all analyzing files to one file
# on the hypothesis folder only the hypothesis should happen and bedingungen für hypothesis
# DEBUG SCORE, CHECK IF THE SCORES ARE TRUE

# reset the index, so a new index is created
dfWM22.reset_index(drop=True, inplace=True)

# convert the dfWM22 to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
dfWM22.to_json(CONSTANTS.JSONWM2022)

print("i am finished with WM22")